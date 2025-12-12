from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import latency_tracker, get_request_meta
from app.db.session import get_db
from app.db import models

router = APIRouter(tags=["data"])


@router.get("/data")
def get_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    source: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    with latency_tracker() as latency:
        request_id = get_request_meta()

        query = db.query(models.UnifiedRecord)
        if source:
            query = query.filter(models.UnifiedRecord.source == source.lower())

        total = query.count()
        items = (
            query.order_by(models.UnifiedRecord.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        data = [
            {
                "id": item.id,
                "source": item.source,
                "external_id": item.external_id,
                "name": item.name,
                "value": item.value,
                "timestamp": item.timestamp,
            }
            for item in items
        ]

        return {
            "data": data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
            },
            "meta": {
                "request_id": request_id,
                "api_latency_ms": latency(),
            },
        }
