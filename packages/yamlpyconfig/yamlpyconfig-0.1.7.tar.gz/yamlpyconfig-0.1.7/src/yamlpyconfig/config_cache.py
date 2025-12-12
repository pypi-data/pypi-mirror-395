import copy
from threading import RLock
from types import MappingProxyType
from typing import Dict, Any, Optional, Mapping, List, Iterator, Tuple

from yamlpyconfig.models import NacosConfigCacheItem
from yamlpyconfig.utils import ConfigMerge
from yamlpyconfig.utils.crypto import CryptoHelper


class ConfigCache:
    """
    负责缓存本地配置 + Nacos 多个 dataId 的配置，并合并成最终配置。
    - 写路径：加锁 + 重建 merged_config（copy-on-write）
    - 读路径：读只读快照，不加锁（或极短锁）
    """

    def __init__(self, base_config: Optional[Dict[str, Any]] = None, crypto_helper: CryptoHelper = None,
                 config_merge_list:bool = False) -> None:
        self._config_merge_list = config_merge_list
        self._lock = RLock()
        # 对外暴露的最终配置快照（不可变）
        self._merged_config: Mapping[str, Any] = MappingProxyType({})
        self._base_config: dict[str, Any] = {}
        self._crypto_helper: CryptoHelper|None = crypto_helper
        self._order: List[str] = []  # imports 顺序
        self._items: Dict[str, NacosConfigCacheItem] = {}
        self.set_base_config(base_config)


    def set_base_config(self, base_config: Dict[str, Any]) -> None:
        """更新本地基础配置，并重建 merged_config。"""
        with self._lock:
            self._base_config = dict(base_config or {})
            if self._crypto_helper:
                self._crypto_helper.decrypt_config_value(self._base_config)
            self._rebuild_merged_unlocked()

    def set_config(self, data_id: str, config: Optional[Dict[str, Any]]) -> None:
        """
        设置/更新某个 dataId 的配置。
        - 若 data_id 不存在，则追加到顺序末尾；
        - 若已存在，仅更新对应的 config。
        """
        with self._lock:
            if self._crypto_helper:
                self._crypto_helper.decrypt_config_value(config)
            if data_id not in self._items:
                self._order.append(data_id)
                self._items[data_id] = NacosConfigCacheItem(data_id=data_id, config=config)
            else:
                # pydantic v2: 可以直接更新属性，也可以 model_copy(update=...)
                item = self._items[data_id]
                item.config = config

            self._rebuild_merged_unlocked()

    def _rebuild_merged_unlocked(self) -> None:
        """
        在锁内重建 merged_config。
        合并策略（浅合并）：
        1. 先拷贝 base_config；
        2. 按 _order 顺序应用每个 dataId 的 config，后者覆盖前者同名 key。
        """
        merged: Dict[str, Any] = copy.deepcopy(self._base_config)

        for data_id in self._order:
            item = self._items.get(data_id)
            if not item or not item.config:
                continue
            cfg = item.config
            if not isinstance(cfg, dict):
                # 若配置不是 dict（比如 yaml 顶层不是映射），可以选择跳过或抛错
                continue
            ConfigMerge.deep_merge(merged, cfg, self._config_merge_list)

        # copy-on-write: 用新的 dict 替换旧引用，并加只读包装
        self._merged_config = MappingProxyType(merged)

    def get_nacos_configs(self) -> Iterator[Tuple[str, Optional[Dict[str, Any]]]]:
        """
        按 imports 顺序依次返回 (dataId, config) 的只读快照。
        为了避免在长时间迭代时持有锁，这里使用“快照”：
        - 在锁内复制 _order 和 _items 的当前状态；
        - 解锁后再遍历快照。
        """
        with self._lock:
            order_snapshot = tuple(self._order)
            items_snapshot = {k: v.config for k, v in self._items.items()}

        for data_id in order_snapshot:
            yield data_id, items_snapshot.get(data_id)

    def get_config(self) -> Mapping[str, Any]:
        """
        返回最终合并后的配置快照（只读 Mapping）。
        注意：返回的是只读的 mappingproxy，对外修改会抛异常。
        """

        return self._merged_config
