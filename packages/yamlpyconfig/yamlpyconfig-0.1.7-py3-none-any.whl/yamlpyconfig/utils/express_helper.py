import os
import re
from typing import Optional, Any


class ExpressionHelper:
    """
    表达式处理类，用于解析字符串中的环境变量占位符。
    """
    @staticmethod
    def _resolve_env_placeholder(s: str) -> Optional[str]:
        """
        解析字符串，匹配 ${key[:default_value]} 格式的占位符。
        如果环境变量存在，则返回其值；
        如果不存在且有默认值，则返回默认值；
        如果两者都不存在，则返回 None。
        """
        # 匹配形如 ${key} 或 ${key:default_value}
        pattern = re.compile(r"^\$\{([^:}]+)(?::(.*))?\}$")
        match = pattern.match(s.strip())
        if not match:
            return s  # 非占位符格式，原样返回（也可以返回 None 看你需求）

        key, default = match.groups()
        return os.getenv(key, default)

    @staticmethod
    def resolve_config(config: dict[str, Any]):
        """
        解析字符串中的所有环境变量占位符。
        """
        for key, value in config.items():
            if isinstance(value, str):
                resolved_value = ExpressionHelper._resolve_env_placeholder(value)
                if resolved_value is not None:
                    config[key] = resolved_value
            elif isinstance(value, dict):
                ExpressionHelper.resolve_config(value)

