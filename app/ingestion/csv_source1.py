import csv
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from app.db import models
from app.schemas.unified import UnifiedRecordCreate


DATA_PATH = Path("data/source1.csv")


def read_csv1(last_external_id: int | None = None) -> list[dict]:
    rows: list[dict] = []
    if not DATA_PATH.exists():
        return rows
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ext_id = int(row["id"])
            if last_external_id is not None and ext_id <= last_external_id:
                continue
            rows.append(row)
    return rows


def store_raw_csv1(db: Session, rows: Iterable[dict]) -> list[int]:
    ids: list[int] = []
    for row in rows:
        ext_id = int(row["id"])
        raw = models.RawCSVRecord(external_id=ext_id, payload=row)
        db.add(raw)
        ids.append(ext_id)
    return ids


def transform_csv1_to_unified(rows: Iterable[dict]) -> list[UnifiedRecordCreate]:
    unified: list[UnifiedRecordCreate] = []
    for row in rows:
        unified.append(
            UnifiedRecordCreate(
                source="csv1",
                external_id=str(row["id"]),
                name=row.get("name", ""),
                value=int(row.get("value", 0)),
                timestamp=__import__("datetime").datetime.fromisoformat(row["timestamp"]),
            )
        )
    return unified
