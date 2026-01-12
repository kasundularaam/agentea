from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    service_name: str
    is_enabled: bool
    is_healthy: bool
    status_message: str = Field(..., description="ENABLED or DISABLED")
    last_error: Optional[str] = None
    disabled_at: Optional[datetime] = None
    checked_at: datetime = Field(default_factory=datetime.now)
