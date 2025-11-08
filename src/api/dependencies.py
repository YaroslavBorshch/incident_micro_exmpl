from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.infrastructure.security import verify_x_access_key as verify_key
from src.services.incident_service import IncidentService


async def verify_x_access_key(
    x_access_key: str = Header(..., alias="X-Access-Key")
) -> str:
    """Проверка X-Access-Key заголовка для аутентификации."""

    if not x_access_key or not verify_key(x_access_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Access-Key",
            headers={"WWW-Authenticate": "X-Access-Key"},
        )

    return x_access_key


async def get_incident_service(
    db: AsyncSession = Depends(get_db)
) -> IncidentService:
    """Di зависимость для сервиса инцидентов"""

    return IncidentService(db)
