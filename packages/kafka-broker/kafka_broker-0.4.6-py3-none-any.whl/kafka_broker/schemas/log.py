from typing import Any
import uuid
from pydantic import BaseModel

from kafka_broker.enums import EventStatus


class LogSchema(BaseModel):
    job_id: uuid.UUID | None = None
    correlation_id: uuid.UUID
    status: EventStatus = EventStatus.ONGOING
    level: int
    module: str
    message: str
    store: dict[str, Any] | None = None
    sequence: list[int] | None = None
