import importlib.util
import logging
from typing import Optional

from .models import AlgorithmEnum
from yamlpyconfig.config_cache import ConfigCache
from yamlpyconfig.local_manage.local_config_manager import LocalConfigManager
from yamlpyconfig.models import NacosConfig
from yamlpyconfig.utils.crypto.crypto_algorithm_factory import CryptoAlgorithmFactory
from .utils.crypto import CryptoHelper

logger = logging.getLogger(__name__)
class ConfigManager:
    """
    ConfigManager is a singleton class that manages the configuration of the application.
    It provides methods to get and set configuration values.
    """
    def __init__(self, config_dir: Optional[str] = None,
                 crypto_algorithm: Optional[AlgorithmEnum] = None, key: Optional[str] = None,
                 base_profile: Optional[str]=None, extend_profiles: Optional[str]=None,
                 config_merge_list: bool=False):
        """

        :param config_dir: 本地配置文件的根目录，包含application.yaml和application-{profile}.yaml的目录
        :param crypto_algorithm: 如果配置文件中包含{encrypted}加密数据，可以配置加密算法，用来解密
        :param key: 如果是sm2则传递私钥，如果是sm4则传递对称密钥
        :param base_profile: 指定profile，如果指定其优先级高于APP_PROFILE环境变量以及application.yaml中的profile配置
        :param extend_profiles: 支持多个以`,`分割的配置加载，将会和`application.yaml`或`application-<profile>.yaml`中的`extend-profiles`配置合并，两种模式：
                                * `file:<full_yaml_config_file_path>`: 直接加载`file:`后的具体配置，不存在将报错
                                * `extend_profile`: 将加载`config_dir / application-<extend_profile>.yaml`的配置文件
                                越靠后优先级越高，其优先级高于`application.yaml`和`application-<profile>.yaml`
        :param config_merge_list: 是否将配置中的列表进行合并，默认False，如果为True，则将列表进行合并
        """
        self._config_merge_list = config_merge_list
        self._local_config_manager = LocalConfigManager(config_dir, base_profile, extend_profiles)
        self._base_config = self._local_config_manager.config
        self._crypto_helper = None
        if crypto_algorithm and key:
            crypto_algorithm = CryptoAlgorithmFactory.create(crypto_algorithm, key_b64=key)
            self._crypto_helper = CryptoHelper(crypto_algorithm)
        self._cache = ConfigCache(base_config=self._base_config, crypto_helper=self._crypto_helper)
        self._nacos_manager = None

    @property
    def crypto_helper(self) -> Optional[CryptoHelper]:
        return self._crypto_helper

    @property
    def base_profile(self):
        return self._local_config_manager.base_profile

    async def start(self):
        if self._nacos_manager is None:
            try:
                nacos_config: NacosConfig = NacosConfig.load_nacos_config(self._cache.get_config())
                if not nacos_config:
                    return
                if not importlib.util.find_spec("v2.nacos"):
                    return
                from yamlpyconfig.nacos_manage.nacos_config_manager import NacosConfigManager
                self._nacos_manager = NacosConfigManager(nacos_config, cache=self._cache)
                await self._nacos_manager.start()
            except Exception as e:
                logger.error(f"Failed to connect to Nacos: {e}", exc_info=True)

    async def __aenter__(self):
        await self.start()
        return self

    async def stop(self):
        if self._nacos_manager:
            await self._nacos_manager.stop()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    def get_config(self):
        return self._cache.get_config()