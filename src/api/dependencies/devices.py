from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services.devices import DeviceService
from src.infrastructure.db.dependencies import get_async_session


async def get_device_service(
    session: AsyncSession = Depends(get_async_session),
) -> DeviceService:
    return DeviceService(session=session)
