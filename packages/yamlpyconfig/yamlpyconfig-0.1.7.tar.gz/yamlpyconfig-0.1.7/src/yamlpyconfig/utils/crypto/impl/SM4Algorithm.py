import base64
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

from ..crypto_algorithm import CryptoAlgorithm


class SM4Algorithm(CryptoAlgorithm):
    """
    SM4 对称加密算法（默认 ECB 模式）
    key: 128-bit（16字节）Base64 字符串
    """
    def __init__(self, key_b64: str, mode: str = "ECB", iv_b64: str | None = None):
        self.key = base64.b64decode(key_b64)
        self.mode = mode.upper()
        self.iv = base64.b64decode(iv_b64) if iv_b64 else None

        if len(self.key) != 16:
            raise ValueError("SM4 key must be 16 bytes (128-bit).")

        if self.mode not in ("ECB", "CBC"):
            raise ValueError("SM4 mode must be ECB or CBC")

        if self.mode == "CBC" and self.iv is None:
            raise ValueError("CBC mode requires iv")

    # ---------------- 加密 ---------------- #
    def encrypt(self, plaintext: str) -> str:
        crypt = CryptSM4()
        crypt.set_key(self.key, SM4_ENCRYPT)

        if self.mode == "ECB":
            cipher_bytes = crypt.crypt_ecb(plaintext.encode("utf-8"))
        else:
            cipher_bytes = crypt.crypt_cbc(self.iv, plaintext.encode("utf-8"))

        return base64.b64encode(cipher_bytes).decode("utf-8")

    # ---------------- 解密 ---------------- #
    def decrypt(self, ciphertext: str) -> str:
        crypt = CryptSM4()
        crypt.set_key(self.key, SM4_DECRYPT)

        cipher_bytes = base64.b64decode(ciphertext)

        if self.mode == "ECB":
            plain_bytes = crypt.crypt_ecb(cipher_bytes)
        else:
            plain_bytes = crypt.crypt_cbc(self.iv, cipher_bytes)

        return plain_bytes.decode()

    # ---------------- 密钥生成 ---------------- #
    @classmethod
    def generate_keys(cls) -> dict:
        """
        生成 128bit SM4 密钥（Base64 字符串）
        若需要 CBC 模式，可额外生成16字节IV
        """
        import os
        key = os.urandom(16)
        iv = os.urandom(16)

        return {
            "key": base64.b64encode(key).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
        }
