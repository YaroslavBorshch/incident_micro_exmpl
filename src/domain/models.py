import enum
import uuid
from datetime import datetime

from sqlalchemy import Text, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class BaseModel(Base):
    """Базовая модель"""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True
    )


class IncidentStatus(str, enum.Enum):
    """енам статусов"""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class IncidentSource(str, enum.Enum):
    """енам источников"""

    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    UNKNOWN = "unknown"


class Incident(BaseModel):
    """модель инцидента"""

    __tablename__ = "incidents"

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        index=True,
        comment="Описание инцидента"
    )
    # TODO: Enum(IncidentStatus), использовать Enum, просто лень с БД возиться сейчас)
    status: Mapped[str] = mapped_column(
        String(255),
        default=IncidentStatus.OPEN.value,
        nullable=False,
        index=True,
    )
    # TODO: аналогично Enum(IncidentSource)
    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        default=IncidentSource.UNKNOWN.value,
    )
