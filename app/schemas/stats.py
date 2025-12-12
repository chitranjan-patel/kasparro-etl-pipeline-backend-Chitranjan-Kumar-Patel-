from datetime import datetime
from pydantic import BaseModel


class EtlStats(BaseModel):
    source: str
    total_runs: int
    total_processed: int
    last_success: datetime | None = None
    last_failure: datetime | None = None
