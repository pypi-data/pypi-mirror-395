from typing import Any, Dict

from .crypto_algorithm import CryptoAlgorithm
from ...models import AlgorithmEnum


class CryptoAlgorithmFactory:
    """算法策略工厂 + 注册表"""

    _registry: Dict[str, type[CryptoAlgorithm]] = {}

    @classmethod
    def register(cls, name: str, algo_cls: type[CryptoAlgorithm]) -> None:
        cls._registry[name.lower()] = algo_cls

    @classmethod
    def create(cls, name: AlgorithmEnum, **kwargs: Any) -> CryptoAlgorithm:
        algo_cls = cls._registry.get(name.value.lower())
        if algo_cls is None:
            raise ValueError(f"Unsupported algorithm: {name}")
        return algo_cls(**kwargs)  # type: ignore[arg-type]

    @classmethod
    def get_algorithms_class(cls, name: AlgorithmEnum):
        algo_cls = cls._registry.get(name.value.lower())
        return algo_cls

    @classmethod
    def list_algorithms(cls) -> list[str]:
        return list(cls._registry.keys())
