from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class CryptoAlgorithm(ABC):
    """加解密算法策略接口"""

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """明文 -> 密文（不含 {encrypted} 前缀）"""
        ...

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """密文 -> 明文（不含 {encrypted} 前缀）"""
        ...

    @classmethod
    @abstractmethod
    def generate_keys(cls) -> Dict[str, str]:
        """
        生成该算法所需密钥。
        对称算法：{"key": "..."}；
        非对称算法：{"public_key": "...", "private_key": "..."}。
        """
        ...
