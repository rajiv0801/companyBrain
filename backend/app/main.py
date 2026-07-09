from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/")
def root():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "Connected ✅",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }