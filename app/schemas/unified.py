from datetime import datetime
from pydantic import BaseModel, validator


class UnifiedRecordCreate(BaseModel):
    source: str
    external_id: str
    name: str | None = None
    value: int | None = None
    timestamp: datetime

    @validator("source")
    def source_lower(cls, v: str) -> str:
        return v.lower()
