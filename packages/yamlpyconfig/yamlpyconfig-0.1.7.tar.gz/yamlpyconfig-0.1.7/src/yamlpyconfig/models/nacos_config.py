from typing import Optional, Any
from typing import Self

from pydantic import Field, field_validator

from .base_config_model import BaseConfigModel


class ImportConfigItem(BaseConfigModel):
    """Single import configuration item."""
    data_id: str = Field(..., description="Import data_id, e.g., 'gateway.yaml'")

    @field_validator("data_id")
    def validate_source(cls, v):
        if not v or ('yaml' not in v and 'yml' not in v):
            raise ValueError("data_id must be in format 'name.yaml', e.g., 'gateway.yaml'")
        return v

class NacosConfig(BaseConfigModel):
    """Nacos configuration model."""
    server_addr: str = Field(..., description="Nacos server address")
    namespace: Optional[str] = Field(None, description="Nacos namespace")
    group: Optional[str] = Field("DEFAULT_GROUP", description="Nacos group")
    username: Optional[str] = Field(None, description="Nacos username")
    password: Optional[str] = Field(None, description="Nacos password")
    access_key: Optional[str] = Field(None, description="Nacos access key")
    secret_key: Optional[str] = Field(None, description="Nacos secret key")
    endpoint: Optional[str] = Field(None, description="Nacos endpoint for ACM")
    auto_refresh: bool = Field(True, description="Whether to auto refresh config")
    imports: Optional[list[ImportConfigItem]] = Field(None, description="List of import configurations")

    @classmethod
    def load_nacos_config(cls, config: dict[str, Any]) -> Optional[Self]:
        """Load Nacos configuration from a dict."""
        if "config-sources" in config and "nacos" in config["config-sources"]:
            return NacosConfig.model_validate(config["config-sources"]["nacos"])
        return None


