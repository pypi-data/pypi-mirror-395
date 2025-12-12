import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any

from yamlpyconfig.utils import ExpressionHelper
from yamlpyconfig.local_manage import LocalConfigLoader
from yamlpyconfig.utils import ConfigMerge

logger = logging.getLogger(__name__)

class LocalConfigManager:
    """
    Local configuration manager.
    默认获取 config_dir / application.yaml 以及 config_dir / application-{profile}.yaml 的本地文件配置。
    其中 profile 的获取逻辑是：
    1. 首先获取APP_PROFILE作为环境变量的值，如果存在返回
    2. 然后获取SPRING_PROFILES_ACTIVE座位环境变量的值，如果存在返回
    3. 最后获取application.yaml配置文件中的profile的配置，如果存在则返回
    如果以上三处都未获取到有效的profile，则不再尝试获取application-{profile}.yaml的配置。
    """

    def __init__(self, config_dir: Optional[str] = None,
                 base_profile: Optional[str] = None, extend_profiles: Optional[str] = None,
                 config_merge_list:bool = False):
        """
        Initialize local config manager.

        Args:
            config_dir: Directory containing config files. Defaults to current working directory.
        """
        self._config_merge_list = config_merge_list
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self._base_profile = base_profile
        self._extend_profiles = []
        if extend_profiles:
            self._extend_profiles = [profile.strip() for profile in extend_profiles.split(",") if profile.strip()]
        self._local_config_loader = LocalConfigLoader(self.config_dir)
        self._config = self._load_config()

    @property
    def base_profile(self):
        return self._base_profile

    @property
    def config(self):
        return self._config

    def _load_config(self) -> Dict[str, Any]:
            """Load local configuration.

            Args:
                profile: Profile to load. Defaults to None.

            Returns:
                A dictionary with the loaded configuration.
            """
            config: dict[str, Any] = self._local_config_loader.load_local_yaml("application")
            ExpressionHelper.resolve_config(config)
            if not self._base_profile:
                self._base_profile = self._detect_profile(config)
            if self._base_profile:
                logger.info(f"Using profile: {self._base_profile}")
                config_profile = self._local_config_loader.load_local_yaml(f"application-{self._base_profile}")
                ConfigMerge.deep_merge(config, config_profile, self._config_merge_list)
            if "extend-profiles" in config:
                extend_profiles_from_config = config["extend-profiles"]
                extend_profiles_list = [profile.strip() for profile in extend_profiles_from_config.split(",") if profile.strip()]
                self._extend_profiles = extend_profiles_list + self._extend_profiles
            self._add_extend_profiles_config(config)
            ExpressionHelper.resolve_config(config)
            return config

    @staticmethod
    def _detect_profile(config) -> Optional[str]:
        """Detect profile from environment or config files."""
        # Check environment variable
        env_profile = os.getenv('APP_PROFILE', os.getenv('SPRING_PROFILES_ACTIVE'))
        if env_profile:
            return env_profile
        # Try to extract from local loader
        if "profile" in config:
            return config["profile"]
        return None


    def _add_extend_profiles_config(self, config):
        """
        Add extends profiles config to config cache.
        """
        for extend_profile in self._extend_profiles:
            if extend_profile.startswith("file:"):
                extend_profile_config = self._local_config_loader.load_local_yaml_from_path(Path(extend_profile[5:]))
            else:
                extend_profile_config = self._local_config_loader.load_local_yaml(f"application-{extend_profile}")
            ConfigMerge.deep_merge(config, extend_profile_config, self._config_merge_list)
