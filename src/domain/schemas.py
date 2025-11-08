import uuid

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List
from uuid import UUID

from src.domain.models import IncidentStatus, IncidentSource


class BaseRequestDTO(BaseModel):
    """базовый запрос"""

    pass


class BaseResponseDTO(BaseModel):
    """базовый ответ"""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ResponseMsgDTO(BaseResponseDTO):
    """ответ сообщением"""

    message: str


class ResponseIdDTO(BaseResponseDTO):
    """ответ айдишником"""

    id: uuid.UUID


class IncidentCreate(BaseRequestDTO):
    """запрос на создание инцидента"""

    description: str | None = Field(
        None, min_length=1, description="Описание инцидента"
    )
    source: IncidentSource | None = Field(
        IncidentSource.UNKNOWN.value, description="Источник инцидента"
    )
    status: IncidentStatus | None = Field(
        IncidentStatus.OPEN.value, description="Статус инцидента"
    )


class IncidentStatusUpdate(BaseRequestDTO):
    """запрос на обновление статуса инцидента"""

    status: IncidentStatus = Field(..., description="Новый статус инцидента")


class IncidentItemResponse(BaseResponseDTO):
    """ответ с данными инцидента"""

    id: UUID
    description: str | None
    status: IncidentStatus | None
    source: IncidentSource | None
    created_at: datetime
    updated_at: datetime


class IncidentListResponse(BaseResponseDTO):
    """ответ со списком инцидентов"""

    # TODO:: в список обычно более короткую версию удобно передавать, нежели подробную
    incidents: List[IncidentItemResponse]
    total: int
