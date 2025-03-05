from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from .logger import logger

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )
