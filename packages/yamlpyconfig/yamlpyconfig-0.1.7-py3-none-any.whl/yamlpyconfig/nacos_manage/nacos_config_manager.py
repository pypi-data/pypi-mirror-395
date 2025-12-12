# ========================
# 3. NacosConfigManager：连接/初始化/监听
# ========================
from __future__ import annotations

import asyncio
import logging
from asyncio import TaskGroup, Task
from typing import Optional, Any, Dict, Iterator, Tuple, Mapping

import yaml
from v2.nacos import ClientConfigBuilder, GRPCConfig, NacosConfigService, ConfigParam

from yamlpyconfig.config_cache import ConfigCache
from yamlpyconfig.models import NacosConfig

logger = logging.getLogger(__name__)
class NacosConfigManager:
    """
    负责：
    1. 用 NacosConfig 初始化 NacosClient；
    2. 根据 imports 顺序拉取初始配置并填充 ConfigCache；
    3. 若 auto_refresh=True，则为每个 dataId 注册监听器，在配置变更时更新 Cache。
    """

    def __init__(
        self,
        nacos_config: NacosConfig,
        cache: Optional[ConfigCache],
    ) -> None:
        self._cfg = nacos_config
        self._group = nacos_config.group or "DEFAULT_GROUP"
        self._cache = cache
        self._client: Optional[NacosConfigService] = None

    async def start(self):
        if self._client is None:
            # 初始化 Nacos 客户端
            self._client = await self._create_client(self._cfg)
            # 初始化配置
            await self._init_import_configs()
            # 如果需要自动刷新，则注册监听
            if self._cfg.auto_refresh:
                await self._register_listeners()


    async def stop(self):
        if self._client:
            await self._client.shutdown()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    @staticmethod
    async def _create_client(cfg: NacosConfig) -> NacosConfigService:
        """
        创建 NacosClient。
        nacos-sdk-python 2.x 的参数名可能略有出入，可按实际 SDK 文档调整。
        """
        kwargs: Dict[str, Any] = {}
        if cfg.namespace:
            kwargs["namespace"] = cfg.namespace
        if cfg.username and cfg.password:
            kwargs["username"] = cfg.username
            kwargs["password"] = cfg.password
        if cfg.access_key and cfg.secret_key:
            kwargs["ak"] = cfg.access_key
            kwargs["sk"] = cfg.secret_key
        if cfg.endpoint:
            kwargs["endpoint"] = cfg.endpoint

        client_config = (ClientConfigBuilder()
                         .server_address(cfg.server_addr)
                         .username(cfg.username)
                         .password(cfg.password)
                         .namespace_id(cfg.namespace)
                         .access_key(cfg.access_key)
                         .secret_key(cfg.secret_key)
                         .log_level("INFO")
                         .grpc_config(GRPCConfig(grpc_timeout=5000))
                         .build())
        while True:
            try:
                config_client = await NacosConfigService.create_config_service(client_config)
                return config_client
            except Exception as e:
                logger.error(f"Nacos client init failed: {e}", exc_info=True)
                await asyncio.sleep(1)

    # ---------- 配置解析 & 初始化 ----------

    @staticmethod
    def _parse_yaml_config(content: Optional[str]) -> Dict[str, Any]:
        """
        解析 YAML 文本为 dict。
        - 若 content 为空或解析失败，则返回空 dict。
        - 若顶层不是 dict，则也返回空 dict（避免后续 merged.update 出问题）。
        """
        if not content:
            return {}
        try:
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            # 这里按需选择：可以记录日志，或者抛自定义异常
            return {}

    async def _init_import_configs(self) -> None:
        """
        初始化加载所有 imports 中的 dataId 配置到 Cache。
        """
        imports = self._cfg.imports or []
        tasks: dict[str, Task] = {}
        async with TaskGroup() as tg:
            for item in imports:
                data_id = item.data_id
                task = tg.create_task(self._get_data_id_config(data_id))
                tasks[data_id] = task
        for item in imports:
            data_id = item.data_id
            raw = tasks[data_id].result()
            cfg_dict = self._parse_yaml_config(raw)
            await asyncio.to_thread(self._cache.set_config, data_id, cfg_dict)

    async def _get_data_id_config(self, data_id: str):
        while True:
            try:
                return await self._client.get_config(ConfigParam(data_id=data_id, group=self._group))
            except Exception as e:
                logger.error(f"Failed to get config for dataId: {data_id}: {e!r}", exc_info=True)
                await asyncio.sleep(1)

    # ---------- 监听配置变更 ----------

    async def _register_listeners(self) -> None:
        """
        为每个 imports.dataId 注册监听器。
        注意：具体监听 API 可能是 add_config_watcher 或 add_listener，
        这里用伪代码形式，使用时按实际 SDK 调整。
        """
        imports = self._cfg.imports or []
        async with TaskGroup() as tg:
            for item in imports:
                data_id = item.data_id
                tg.create_task(self._register_single_listener(data_id))

    async def _register_single_listener(self, data_id: str) -> None:
        group = self._group

        async def _on_change(tenant, data_id, group, content) -> None:
            """
            Nacos 配置变化时的回调。
            只做两件事：
            1. 解析 YAML；
            2. 更新 Cache。
            """
            cfg_dict = None
            if content:
                cfg_dict = self._parse_yaml_config(content)
            await asyncio.to_thread(self._cache.set_config, data_id, cfg_dict)

        # 这里根据 nacos-sdk-python 的实际接口调用
        # 官方 SDK 大致有类似 API：
        #   client.add_config_watcher(data_id, group, callback)
        # 或者：
        #   client.add_listener(data_id, group, callback)
        #
        # 假设使用 add_config_watcher：
        try:
            await self._client.add_listener(data_id, group, _on_change)  # 伪代码
        except Exception as e:
            logger.error(f"Failed to register Nacos listener (data_id={data_id}, group={group}): {e!r}", exc_info=True)

    # ---------- 对外访问接口 ----------

    @property
    def cache(self) -> ConfigCache:
        """暴露底层 Cache 对象（只读访问配置，写操作也可以）。"""
        return self._cache

    def get_config(self) -> Mapping[str, Any]:
        """获取合并后的最终配置快照（只读）。"""
        return self._cache.get_config()

    def get_nacos_configs(self) -> Iterator[Tuple[str, Optional[Dict[str, Any]]]]:
        """按 imports 顺序返回 (dataId, config)。"""
        return self._cache.get_nacos_configs()