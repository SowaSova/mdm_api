from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "NOT_FOUND"


class DatabaseErrorException(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "DATABASE_ERROR"


class NotEnoughRightsException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "NOT_ENOUGH_RIGHTS"


class PageNotFoundException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "PAGE_NOT_FOUND"
