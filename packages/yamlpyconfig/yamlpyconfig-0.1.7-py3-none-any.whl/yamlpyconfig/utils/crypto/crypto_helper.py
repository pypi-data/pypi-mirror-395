from typing import Optional, Dict, Any, Self

from .crypto_algorithm import CryptoAlgorithm
from ...models import AlgorithmEnum
from .crypto_algorithm_factory import CryptoAlgorithmFactory


class CryptoHelper:
    """
    业务层使用的加解密工具：
    - 负责识别/封装 `{encrypted}` 前缀
    - 持有一个具体的 CryptoAlgorithm 策略
    """

    ENCRYPTED_PREFIX = "{encrypted}"

    def __init__(self, algorithm: CryptoAlgorithm):
        self._algorithm = algorithm

    @classmethod
    def from_algorithm_name(cls, name: AlgorithmEnum, **kwargs: Any) -> Self:
        """工厂式构造：通过算法名 + 参数创建 CryptoHelper"""
        algo = CryptoAlgorithmFactory.create(name, **kwargs)
        return cls(algo)

    @staticmethod
    def strip_prefix(value: str, prefix: str) -> Optional[str]:
        """如果以 prefix 开头，返回去掉前缀后的内容，否则返回 None"""
        if value.startswith(prefix):
            return value[len(prefix):]
        return None

    def encrypt_value(self, value: str, with_prefix: bool = True) -> str:
        """
        对传入的明文进行加密。
        - 默认加 `{encrypted}` 前缀；
        - 如果 value 已经是带前缀的密文，可以根据需要选择是否重复加密。
        """
        ciphertext = self._algorithm.encrypt(value)
        if with_prefix:
            return f"{self.ENCRYPTED_PREFIX}{ciphertext}"
        return ciphertext

    def decrypt_value(self, value: str) -> str:
        """
        对传入的值进行解密：
        - 如果以 `{encrypted}` 开头，则截取后面的内容进行解密；
        - 否则认为是明文，直接返回。
        """
        inner = self.strip_prefix(value, self.ENCRYPTED_PREFIX)
        if inner is None:
            # 不带前缀，当作明文返回
            return value
        return self._algorithm.decrypt(inner)

    @staticmethod
    def generate_keys(algorithm_name: AlgorithmEnum) -> Dict[str, str]:
        """统一的密钥生成入口"""
        algo_cls = CryptoAlgorithmFactory.get_algorithms_class(algorithm_name)
        if algo_cls is None:
            raise ValueError(f"Unsupported algorithm: {algorithm_name}")
        return algo_cls.generate_keys()

    def decrypt_config_value(self, config: dict[str, Any] | None):
        if config is None:
            return
        for k, v in config.items():
            if isinstance(v, str):
                config[k] = self.decrypt_value(v)
            elif isinstance(v, dict):
                self.decrypt_config_value(v)
