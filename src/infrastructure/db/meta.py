import uuid
from datetime import datetime, timezone

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import UUID, DateTime

from src.infrastructure.db.orm import Base


class BaseDBModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
    )
