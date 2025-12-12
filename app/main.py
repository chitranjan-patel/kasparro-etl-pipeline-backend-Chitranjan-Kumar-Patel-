from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
from app.api.routes import data, health, stats


def create_app() -> FastAPI:
    app = FastAPI(title="Backend & ETL System", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(data.router)
    app.include_router(health.router)
    app.include_router(stats.router)

    @app.on_event("startup")
    def startup():
        """Create tables on app startup"""
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Warning: Could not create database tables: {e}")

    return app


app = create_app()
