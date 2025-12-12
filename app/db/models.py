from sqlalchemy import Column, Integer, String, DateTime, JSON, UniqueConstraint
from sqlalchemy.sql import func
from app.db.session import Base


class RawAPIRecord(Base):
    __tablename__ = "raw_api_records"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True)
    payload = Column(JSON, nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())


class RawCSVRecord(Base):
    __tablename__ = "raw_csv_records"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True)
    payload = Column(JSON, nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())


class RawCSV2Record(Base):
    __tablename__ = "raw_csv2_records"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True)
    payload = Column(JSON, nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())


class UnifiedRecord(Base):
    __tablename__ = "unified_records"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # api / csv1 / csv2
    external_id = Column(String, index=True)
    name = Column(String, nullable=True)
    value = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uix_source_external"),
    )


class Checkpoint(Base):
    __tablename__ = "checkpoints"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, unique=True, index=True)
    last_external_id = Column(Integer, nullable=True)
    last_run_at = Column(DateTime(timezone=True))


class EtlRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    status = Column(String, index=True)  # SUCCESS / FAILURE
    records_processed = Column(Integer, default=0)
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
