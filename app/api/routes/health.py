from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, Any]:
    # DB connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "UP"
    except Exception:  # noqa: BLE001
        db_status = "DOWN"

    etl_status = None
    if db_status == "UP":
        try:
            last_run = (
                db.query(models.EtlRun)
                .order_by(models.EtlRun.finished_at.desc())
                .first()
            )

            if last_run:
                etl_status = {
                    "last_status": last_run.status,
                    "last_source": last_run.source,
                    "last_finished_at": last_run.finished_at,
                    "last_records_processed": last_run.records_processed,
                }
        except Exception:  # noqa: BLE001
            pass

    return {
        "status": "OK" if db_status == "UP" else "DEGRADED",
        "database": db_status,
        "etl_last_run": etl_status,
    }
