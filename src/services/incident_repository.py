from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Incident, IncidentStatus, IncidentSource


class IncidentRepository:
    """Репозиторий для работы с инцидентами в БД."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, description: str, source: IncidentSource) -> Incident:
        """создать новый инцидент"""

        incident = Incident(description=description, source=source)
        self.db.add(incident)
        await self.db.flush()
        return incident

    async def get_by_id(self, incident_id: UUID) -> Optional[Incident]:
        """получить инцидент по id"""

        result = await self.db.scalar(
            select(Incident).where(Incident.id == incident_id)
        )
        return result

    def _apply_filters(
        self,
        query,
        status: IncidentStatus | None = None,
        source: IncidentSource | None = None
    ):
        """Применить фильтры к запросу."""

        if status:
            query = query.where(Incident.status == status.value)
        if source:
            query = query.where(Incident.source == source.value)
        return query

    async def get_all(
        self,
        status: IncidentStatus | None = None,
        source: IncidentSource | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Incident], int]:
        """список инцидентов с фильтрами"""

        query = select(Incident)
        query = self._apply_filters(query, status, source)
        query = query.order_by(Incident.created_at.desc())
        query = query.limit(limit).offset(offset)

        count_query = select(func.count(Incident.id))
        count_query = self._apply_filters(count_query, status, source)

        incidents_result = await self.db.scalars(query)
        total = await self.db.scalar(count_query) or 0

        return list(incidents_result.all()), total

    async def update_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus
    ) -> Optional[Incident]:
        """обновить статус"""

        incident = await self.get_by_id(incident_id)
        if not incident:
            return None

        incident.status = new_status
        await self.db.flush()
        return incident

