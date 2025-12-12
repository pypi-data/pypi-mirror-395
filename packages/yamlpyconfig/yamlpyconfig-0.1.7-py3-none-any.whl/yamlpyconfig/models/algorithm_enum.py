from enum import Enum


class AlgorithmEnum(str, Enum):
    SM2 = "sm2"
    SM4 = "sm4"
    SM4_HEX = "sm4_hex"
