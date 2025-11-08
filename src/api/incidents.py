from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_incident_service, verify_x_access_key
from src.domain.models import IncidentSource, IncidentStatus
from src.domain.schemas import (
    IncidentCreate,
    IncidentItemResponse,
    IncidentStatusUpdate,
    IncidentListResponse,
    ResponseIdDTO,
    ResponseMsgDTO,
)
from src.services.incident_service import IncidentService

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseIdDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Создать инцидент",
)
async def create_incident(
    incident_data: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
    _: str = Depends(verify_x_access_key),
) -> ResponseIdDTO:
    """создание инцидента"""

    response = await service.create_incident(
        description=incident_data.description, source=incident_data.source
    )
    return response


@router.get(
    "/",
    response_model=IncidentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить список инцидентов",
)
async def get_incidents(
    status: IncidentStatus | None = Query(
        None, description="Фильтр по статусу инцидента"
    ),
    source: IncidentSource | None = Query(
        None, description="Фильтр по источнику инцидента"
    ),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    service: IncidentService = Depends(get_incident_service),
    _: str = Depends(verify_x_access_key),
) -> IncidentListResponse:
    """список инцидентов"""

    return await service.get_incidents(
        status=status,
        source=source,
        limit=limit,
        offset=offset
    )

@router.get(
    "/{incident_id}",
    response_model=IncidentItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить инцидент по ID",
)
async def get_incident(
    incident_id: UUID,
    service: IncidentService = Depends(get_incident_service),
    _: str = Depends(verify_x_access_key),
) -> IncidentItemResponse:
    """Получить инцидент по ID."""

    incident = await service.get_incident(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    return incident


@router.patch(
    "/{incident_id}/status",
    response_model=ResponseMsgDTO,
    status_code=status.HTTP_200_OK,
    summary="Обновить статус инцидента",
)
async def update_incident_status(
    incident_id: UUID,
    update_data: IncidentStatusUpdate,
    service: IncidentService = Depends(get_incident_service),
    _: str = Depends(verify_x_access_key),
) -> ResponseMsgDTO:
    """Обновить статус инцидента по ID."""

    updated = await service.update_incident_status(
        incident_id=incident_id,
        new_status=update_data.status
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    return ResponseMsgDTO(message="Incident status updated")
