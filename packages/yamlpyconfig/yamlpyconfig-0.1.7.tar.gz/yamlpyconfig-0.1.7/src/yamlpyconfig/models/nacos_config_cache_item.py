from typing import Optional, Any

from pydantic import BaseModel, Field


class NacosConfigCacheItem(BaseModel):
    """Single Nacos configuration cache item."""
    data_id: str = Field(..., description="nacos data ID")
    config: Optional[dict[str, Any]] = Field(None, description="nacos configuration")