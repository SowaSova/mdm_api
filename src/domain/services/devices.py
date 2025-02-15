import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.websocket.manager import ConnectionManager
from src.domain.exceptions.devices import DeviceOfflineException
from src.core.exceptions import DatabaseErrorException, NotFoundException
from src.domain.schemas.devices import (
    DeviceCommandResponseSchema,
)
from src.core.constants import COMMAND_STATUS_MAPPING
from src.core.enums import Command, DeviceStatus
from src.core.services import CustomService
from src.domain.repositories.devices import DeviceRepository
from src.core.logging import logger


class DeviceService(CustomService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repository = DeviceRepository

    async def add(self, **kwargs):
        try:
            return await self.repository.create(self.session, **kwargs)
        except Exception as e:
            logger.error(f"Failed to create device: {e}")
            raise DatabaseErrorException

    async def find_all(self, **kwargs):
        try:
            return await self.repository.get_all(self.session, **kwargs)
        except Exception as e:
            logger.error(f"Failed to get devices: {e}")
            raise DatabaseErrorException

    async def find_one(self, device_id: str):
        try:
            device = await self.repository.get_by_id(
                self.session, device_id=device_id
            )
            if not device:
                logger.error(f"Device {device_id} not found")
                raise DatabaseErrorException
            return device
        except Exception as e:
            logger.error(f"Failed to get device: {e}")
            raise DatabaseErrorException

    async def update(self, device_id: str, **kwargs):
        try:
            updated_device = await self.repository.update_by_id(
                self.session, device_id, **kwargs
            )
            return updated_device
        except Exception as e:
            logger.error(f"Failed to update device: {e}")
            raise DatabaseErrorException

    async def delete(self, device_id: str):
        return await self.repository.delete(self.session, device_id=device_id)

    async def execute_command(
        self, device_id: str, v: Command
    ) -> DeviceCommandResponseSchema:
        device = await self.repository.get_by_id(
            self.session, device_id=device_id
        )
        if not device:
            logger.error(f"Device {device_id} not found")
            raise DatabaseErrorException
        if device.status == DeviceStatus.OFFLINE:
            logger.error(f"Device {device_id} is offline")
            raise DeviceOfflineException
        if v not in COMMAND_STATUS_MAPPING:
            logger.error(f"Некорректная команда: {v}")
            raise NotFoundException
        new_status = COMMAND_STATUS_MAPPING[v]
        try:
            updated_device = await self.repository.update_by_id(
                self.session, device_id, status=new_status
            )
            logger.info(
                f"Command'{v.value}' with {device_id} succeeded. New status: {updated_device.status}"
            )
        except Exception as e:
            logger.error(f"Failed to update device {device_id}: {e}")
            raise DatabaseErrorException
        return DeviceCommandResponseSchema(
            message=f"Command'{v.value}' with id {device_id} succeeded.",
            device=updated_device,
        )

    async def prepare_command(
        self, device_id: str, v: Command
    ) -> DeviceCommandResponseSchema:
        device = await self.repository.get_by_id(
            self.session, device_id=device_id
        )
        if not device:
            logger.error(f"Device {device_id} not found")
            raise NotFoundException
        logger.info(f"Command '{v.value}' for device {device_id} prepared.")
        return DeviceCommandResponseSchema(
            message=f"Command '{v.value}' for device {device_id} prepared.",
            device=device,
        )

    async def simulate_command_execution(
        self, device_id: str, cmd: Command, manager: ConnectionManager
    ):
        await asyncio.sleep(5)  # Симуляция выполнения команды
        new_status = COMMAND_STATUS_MAPPING.get(cmd)
        if new_status:
            updated_device = await self.repository.update_by_id(
                self.session, device_id, status=new_status
            )
            logger.info(
                f"Command '{cmd.value}' for device {device_id} executed. New status: {updated_device.status}"
            )
            await manager.broadcast(
                f"Device {device_id} status changed to {updated_device.status}"
            )
