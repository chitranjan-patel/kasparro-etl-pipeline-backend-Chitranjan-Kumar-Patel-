from datetime import datetime
import time

from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine, Base
from app.db import models
from app.ingestion.api_source import fetch_api_data, store_raw_api, transform_api_to_unified
from app.ingestion.csv_source1 import read_csv1, store_raw_csv1, transform_csv1_to_unified
from app.ingestion.csv_source2 import read_csv2, store_raw_csv2, transform_csv2_to_unified


SOURCES = ("api", "csv1", "csv2")


def get_checkpoint(db: Session, source: str) -> int | None:
    cp = db.query(models.Checkpoint).filter_by(source=source).first()
    return cp.last_external_id if cp else None


def update_checkpoint(db: Session, source: str, last_external_id: int | None):
    cp = db.query(models.Checkpoint).filter_by(source=source).first()
    now = datetime.utcnow()
    if cp is None:
        cp = models.Checkpoint(source=source, last_external_id=last_external_id, last_run_at=now)
        db.add(cp)
    else:
        cp.last_external_id = last_external_id
        cp.last_run_at = now


def upsert_unified_records(db: Session, unified):
    for rec in unified:
        existing = (
            db.query(models.UnifiedRecord)
            .filter_by(source=rec.source, external_id=rec.external_id)
            .first()
        )
        if existing:
            existing.name = rec.name
            existing.value = rec.value
            existing.timestamp = rec.timestamp
        else:
            db.add(
                models.UnifiedRecord(
                    source=rec.source,
                    external_id=rec.external_id,
                    name=rec.name,
                    value=rec.value,
                    timestamp=rec.timestamp,
                )
            )


def run_for_source(db: Session, source: str):
    run = models.EtlRun(source=source, status="RUNNING", records_processed=0)
    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        last_external_id = get_checkpoint(db, source)
        if source == "api":
            data = fetch_api_data(last_external_id)
            raw_ids = store_raw_api(db, data)
            unified = transform_api_to_unified(data)
        elif source == "csv1":
            rows = read_csv1(last_external_id)
            raw_ids = store_raw_csv1(db, rows)
            unified = transform_csv1_to_unified(rows)
        elif source == "csv2":
            rows = read_csv2(last_external_id)
            raw_ids = store_raw_csv2(db, rows)
            unified = transform_csv2_to_unified(rows)
        else:
            raise ValueError(f"Unknown source {source}")

        upsert_unified_records(db, unified)
        new_last_id = max(raw_ids) if raw_ids else last_external_id
        update_checkpoint(db, source, new_last_id)

        run.status = "SUCCESS"
        run.records_processed = len(unified)
        run.finished_at = datetime.utcnow()
        db.commit()
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        run.status = "FAILURE"
        run.error_message = str(exc)
        run.finished_at = datetime.utcnow()
        db.commit()
        raise


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for source in SOURCES:
            run_for_source(db, source)
    finally:
        db.close()


if __name__ == "__main__":
    # simple one-shot run; Docker etl service will execute this
    main()
