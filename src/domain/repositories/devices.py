from src.core.repositories import SQLAlchemyRepository
from src.domain.models.devices import Device
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from src.core.logging import logger
from src.core.exceptions import DatabaseErrorException


class DeviceRepository(SQLAlchemyRepository):
    model = Device

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        new_device = cls.model(**kwargs)
        session.add(new_device)
        await session.commit()
        return new_device

    @classmethod
    async def get_all(cls, session: AsyncSession, **kwargs):
        query = select(cls.model)
        try:
            if "status" in kwargs and kwargs["status"]:
                query = query.where(cls.model.status == kwargs["status"])
            if "device_type" in kwargs and kwargs["device_type"]:
                query = query.where(
                    cls.model.device_type == kwargs["device_type"]
                )
        except Exception as e:
            logger.error("Ошибка в применении фильтров: {}", e)
            raise DatabaseErrorException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка в применении фильтров",
            )

        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, device_id: str):
        q = select(cls.model).where(cls.model.id == device_id)
        result = await session.execute(q)
        return result.scalar_one_or_none()

    @classmethod
    async def update_by_id(
        cls, session: AsyncSession, device_id: str, **kwargs
    ):
        obj = await cls.get_by_id(session, device_id)
        if not obj:
            return
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def delete(cls, session: AsyncSession, device_id: str):
        q = delete(cls.model).where(cls.model.id == device_id)
        await session.execute(q)
        await session.commit()
