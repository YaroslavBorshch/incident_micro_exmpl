from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.domain.models import Incident, IncidentStatus, IncidentSource
from src.domain.schemas import IncidentItemResponse, IncidentListResponse, ResponseIdDTO
from src.infrastructure.cache import cache_client
from src.services.incident_repository import IncidentRepository


class IncidentService:
    """сервис для работы с инцидентами"""

    def __init__(self, db: AsyncSession):
        self.repository = IncidentRepository(db)
        # self.kafka_producer = KafkaProducerService()

    async def create_incident(
        self,
        description: str,
        source: IncidentSource
    ) -> ResponseIdDTO:
        """создание инцидента"""

        incident = await self.repository.create(
            description=description,
            source=source
        )

        await self._send_to_kafka(incident)

        return ResponseIdDTO(id=incident.id)

    async def get_incident(self, incident_id: UUID) -> IncidentItemResponse | None:
        """Получить инцидент по ID."""

        # проверяем кеш
        cache_key = f"incident:{incident_id}"
        if settings.cache_enabled:
            cached = await cache_client.get(cache_key)
            if cached:
                return IncidentItemResponse.model_validate(cached)

        # Получаем из бд
        incident = await self.repository.get_by_id(incident_id)
        if not incident:
            return None

        response = IncidentItemResponse.model_validate(incident)

        # Сохраняем в кэш
        if settings.cache_enabled:
            await cache_client.set(
                cache_key,
                response.model_dump(mode='json'),
                ttl=settings.cache_incidents_ttl
            )

        return response

    async def get_incidents(
        self,
        status: Optional[IncidentStatus] = None,
        source: Optional[IncidentSource] = None,
        limit: int = 100,
        offset: int = 0
    ) -> IncidentListResponse:
        """список инцидентов"""

        # кэш списка скипаем из-за пагинации

        # Получаем из бд
        incidents, total = await self.repository.get_all(
            status=status,
            source=source,
            limit=limit,
            offset=offset
        )

        response = IncidentListResponse(
            incidents=[IncidentItemResponse.model_validate(inc) for inc in incidents],
            total=total
        )

        return response

    async def update_incident_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus
    ) -> bool:
        """Обновить статус инцидента."""

        incident = await self.repository.update_status(incident_id, new_status)
        if not incident:
            return False

        await self._invalidate_incident_cache(incident_id)

        await self._send_to_kafka(incident)

        return True


    async def _invalidate_incident_cache(self, incident_id: UUID):
        """инвалидировать кэш конкретного инцидента"""

        if not settings.cache_enabled:
            return

        cache_key = f"incident:{incident_id}"
        await cache_client.delete(cache_key)

    async def _send_to_kafka(self, incident: Incident):
        pass

