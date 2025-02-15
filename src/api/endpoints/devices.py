from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.dependencies.ws import get_manager
from src.infrastructure.websocket.manager import ConnectionManager
from src.api.dependencies.devices import get_device_service

from src.domain.services.devices import DeviceService
from src.domain.schemas.devices import (
    DeviceResponseSchema,
    DeviceFilterSchema,
    DeviceCreateSchema,
    DeviceUpdateSchema,
    DeviceCommandSchema,
    DeviceCommandResponseSchema,
)

router = APIRouter(prefix="/devices", tags=["Device"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_device(
    device: DeviceCreateSchema,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponseSchema:
    return await service.add(**device.model_dump())


@router.get("/", status_code=status.HTTP_200_OK)
async def get_devices(
    filter_by: DeviceFilterSchema = Depends(),
    service: DeviceService = Depends(get_device_service),
) -> List[DeviceResponseSchema]:
    return await service.find_all(**filter_by.model_dump())


@router.get("/{device_id}", status_code=status.HTTP_200_OK)
async def get_device(
    device_id: str,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponseSchema:
    return await service.find_one(device_id=device_id)


@router.put("/{device_id}", status_code=status.HTTP_200_OK)
async def update_device(
    device_id: str,
    data: DeviceUpdateSchema,
    service: DeviceService = Depends(get_device_service),
) -> DeviceResponseSchema:
    return await service.update(device_id=device_id, **data.model_dump())


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    service: DeviceService = Depends(get_device_service),
) -> None:
    return await service.delete(device_id=device_id)


@router.post("/{device_id}/command", status_code=status.HTTP_200_OK)
async def update_device_status(
    device_id: str,
    command: DeviceCommandSchema,
    service: DeviceService = Depends(get_device_service),
    manager: ConnectionManager = Depends(get_manager),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> DeviceCommandResponseSchema:
    response = await service.prepare_command(
        device_id=device_id, v=command.command
    )
    background_tasks.add_task(
        service.simulate_command_execution, device_id, command.command, manager
    )
    return response
