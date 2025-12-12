from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: Optional[int] = None
    session_id: Optional[UUID] = None

    cli_version: str
    installation_method: str
    python_version: str
    os_platform: str

    repository_hash: Optional[str] = None

    action: str
    result: str
    duration_ms: Optional[int] = None

    parameters: Optional[Dict] = None

    error_type: Optional[str] = None
    error_message: Optional[str] = None


class TelemetryEventBatch(BaseModel):
    events: List[TelemetryEvent]
