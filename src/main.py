from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.api.routers import api_router
from src.core.logging import logger
from src.core.config import settings

app = FastAPI(title="MDM API", version="0.1.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.debug(exc.errors())
    detail = exc.errors() if settings.DEBUG else "Unprocessable Entity"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": detail},
    )


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
