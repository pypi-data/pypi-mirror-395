import base64
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

from .SM4Algorithm import SM4Algorithm


class SM4AlgorithmHex(SM4Algorithm):
    """
    SM4 对称加密算法（默认 ECB 模式）
    key: 128-bit（16字节）Base64 字符串
    与SM4Algorithm的差异是，结果直接返回hex()字符串
    """
    def __init__(self, key_b64: str, mode: str = "ECB", iv_b64: str | None = None):
        super().__init__(key_b64, mode, iv_b64)

    # ---------------- 加密 ---------------- #
    def encrypt(self, plaintext: str) -> str:
        crypt = CryptSM4(SM4_ENCRYPT)
        crypt.set_key(self.key, SM4_ENCRYPT)

        if self.mode == "ECB":
            cipher_bytes = crypt.crypt_ecb(plaintext.encode("utf-8"))
        else:
            cipher_bytes = crypt.crypt_cbc(self.iv, plaintext.encode("utf-8"))

        return cipher_bytes.hex()

    # ---------------- 解密 ---------------- #
    def decrypt(self, ciphertext: str) -> str:
        crypt = CryptSM4(SM4_DECRYPT)
        crypt.set_key(self.key, SM4_DECRYPT)

        if self.mode == "ECB":
            plain_bytes = crypt.crypt_ecb(bytes.fromhex(ciphertext))
        else:
            plain_bytes = crypt.crypt_cbc(self.iv, bytes.fromhex(ciphertext))

        return plain_bytes.decode()

    # ---------------- 密钥生成 ---------------- #
    @classmethod
    def generate_keys(cls) -> dict:
        """
        生成 128bit SM4 密钥（Base64 字符串）
        若需要 CBC 模式，可额外生成16字节IV
        """
        return SM4Algorithm.generate_keys()
