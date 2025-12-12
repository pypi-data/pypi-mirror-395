from __future__ import annotations
from typing import TypeVar, Any, Type

from pydantic import BaseModel
from pydantic.config import ConfigDict

T = TypeVar("T", bound="BaseConfigModel")

def hyphen_alias(field_name: str) -> str:
    """
    将字段名中的下划线转换为连字符
    例如: max_connections -> max-connections
    """
    return field_name.replace("_", "-")

class BaseConfigModel(BaseModel):
    """支持 - / _ key 兼容的配置基类"""
    model_config = ConfigDict(
        # 1. 自动为每个字段生成 alias，将 _ 替换为 -
        alias_generator=hyphen_alias,

        # 2. 允许通过字段原名（带下划线）填充，同时也允许通过 alias（带连字符）填充
        populate_by_name=True,

        # 3. (可选) 忽略掉输入字典中多余的字段，防止报错
        extra='ignore'
    )

    @classmethod
    def from_dict(cls: Type[T], data: Any) -> T:
        """
        封装转换方法，将字典转换为实体类
        """
        return cls.model_validate(data)
