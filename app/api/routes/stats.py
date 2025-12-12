from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models

router = APIRouter(tags=["stats"])


@router.get("/stats")
def stats(db: Session = Depends(get_db)) -> dict[str, Any]:
    sub = (
        db.query(
            models.EtlRun.source,
            func.count(models.EtlRun.id).label("total_runs"),
            func.coalesce(func.sum(models.EtlRun.records_processed), 0).label("total_processed"),
            func.max(
                func.nullif(
                    func.case((models.EtlRun.status == "SUCCESS", models.EtlRun.finished_at)),
                    None,
                )
            ).label("last_success"),
            func.max(
                func.nullif(
                    func.case((models.EtlRun.status == "FAILURE", models.EtlRun.finished_at)),
                    None,
                )
            ).label("last_failure"),
        )
        .group_by(models.EtlRun.source)
        .all()
    )

    data: list[dict[str, Any]] = []
    for row in sub:
        data.append(
            {
                "source": row.source,
                "total_runs": row.total_runs,
                "total_processed": int(row.total_processed or 0),
                "last_success": row.last_success,
                "last_failure": row.last_failure,
            }
        )
    return {"stats": data}
