from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Enum
from src.core.enums import DeviceStatus, DeviceType

from src.infrastructure.db.meta import BaseDBModel


class Device(BaseDBModel):
    __tablename__ = "devices"

    device_name = Column(String, nullable=False)
    device_type = Column(
        Enum(
            DeviceType,
            values_callable=lambda x: [e.value for e in x],
            name="device_type_enum",
        ),
        nullable=False,
    )
    status = Column(
        Enum(
            DeviceStatus,
            values_callable=lambda x: [e.value for e in x],
            name="device_status_enum",
        ),
        nullable=False,
        default=DeviceStatus.ACTIVE.value,
    )
    last_seen = Column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc),
    )
