from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.core.enums import DeviceStatus, DeviceType, Command


class DeviceFilterSchema(BaseModel):
    status: Optional[DeviceStatus] = None
    device_type: Optional[DeviceType] = None


class DeviceResponseSchema(BaseModel):
    device_name: str
    device_type: DeviceType
    status: DeviceStatus
    last_seen: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S") if v else None
        }


class DeviceCreateSchema(BaseModel):
    device_name: str
    device_type: DeviceType


class DeviceUpdateSchema(BaseModel):
    device_name: Optional[str]
    device_type: Optional[DeviceType]


class DeviceCommandSchema(BaseModel):
    command: Command


class DeviceCommandResponseSchema(BaseModel):
    message: str
    device: DeviceResponseSchema

    class Config:
        from_attributes = True
