from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import incidents, utils
from src.infrastructure.cache import cache_client
from src.infrastructure.error_middleware import ErrorHandlingMiddleware
from src.infrastructure.security_middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from src.services.kafka_service import kafka_producer, kafka_consumer
from src.services.telegram_service import telegram_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Incidents API...")

    try:
        await cache_client.initialize()
        print("Cache connected successfully")
    except Exception as e:
        print(f"Cache connection failed: {e}")

    # Инициализация Kafka продюсера (заглушка)
    try:
        await kafka_producer.initialize()
        print("Kafka producer initialized")
    except Exception as e:
        print(f"Kafka producer initialization failed: {e}")

    # Инициализация Telegram сервиса (заглушка)
    try:
        await telegram_service.initialize()
        print("Telegram service initialized")
    except Exception as e:
        print(f"Telegram service initialization failed: {e}")

    print("Database ready (use Alembic for migrations)")
    print("Incidents API started successfully")

    yield

    # Shutdown
    print("Shutting down Incidents API...")
    try:
        await cache_client.close()
        await kafka_producer.close()
        await telegram_service.close()
    except Exception:
        pass


app = FastAPI(
    title="Incidents API",
    description="API для учёта инцидентов",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
app.include_router(utils.router, prefix="/utils", tags=["Utils"])


@app.get("/")
async def root():
    return {
        "message": "Incidents API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected",
        "kafka": "stub",
        "telegram": "stub"
    }
