import base64
from gmssl import sm2, func

from ..crypto_algorithm import CryptoAlgorithm


class SM2Algorithm(CryptoAlgorithm):
    """
    SM2 非对称加密算法
    public_key_b64:  Base64(HEX public key)
    private_key_b64: Base64(HEX private key)
    """

    def __init__(self, key_b64: str | None, public_key_b64: str | None = None):
        self.private_key_hex = base64.b64decode(key_b64).decode() if key_b64 else None
        self.public_key_hex = base64.b64decode(public_key_b64).decode() if public_key_b64 else None

        # 如果私钥存在但公钥不存在 → 自动推导
        if self.private_key_hex and not self.public_key_hex:
            sm2_crypt = sm2.CryptSM2(private_key=self.private_key_hex, public_key="")

            self.public_key_hex = sm2_crypt._kg(int(self.private_key_hex, 16), sm2_crypt.ecc_table["g"])

        self.sm2_crypt = sm2.CryptSM2(
            private_key=self.private_key_hex,
            public_key=self.public_key_hex
        )

    # ---------------- 加密（必须公钥） ---------------- #
    def encrypt(self, plaintext: str) -> str:
        if not self.public_key_hex:
            raise ValueError("SM2 encryption requires public_key")

        # encrypt 返回 bytes
        cipher_bytes: bytes = self.sm2_crypt.encrypt(plaintext.encode("utf-8"))
        # 统一封装成 Base64 字符串返回
        return base64.b64encode(cipher_bytes).decode("ascii")

    # ---------------- 解密（必须私钥） ---------------- #
    def decrypt(self, ciphertext: str) -> str:
        if not self.private_key_hex:
            raise ValueError("SM2 decryption requires private_key")

        # Base64 → bytes
        cipher_bytes: bytes = base64.b64decode(ciphertext)
        plain_bytes: bytes = self.sm2_crypt.decrypt(cipher_bytes)
        return plain_bytes.decode("utf-8")

    # ---------------- 密钥生成 ---------------- #
    @classmethod
    def generate_keys(cls) -> dict:
        """
        返回 Base64(HEX) 的公私钥
        """
        private_key_hex = func.random_hex(64)  # 256bit
        sm2_crypt = sm2.CryptSM2(private_key=private_key_hex, public_key="")

        public_key_hex = sm2_crypt._kg(int(private_key_hex, 16), sm2_crypt.ecc_table["g"])

        return {
            "private_key": base64.b64encode(private_key_hex.encode()).decode("utf-8"),
            "public_key": base64.b64encode(public_key_hex.encode()).decode("utf-8"),
        }
