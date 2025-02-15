from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DeviceOfflineException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = "DEVICE_UNAVAILABLE"
