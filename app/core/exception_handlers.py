from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import problem


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return problem(
        status=exc.status_code,
        title="HTTP Error",
        detail=exc.detail,
        instance=request.url.path,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return problem(
        status=422,
        title="Validation Failed",
        detail="One or more validation errors occurred",
        instance=request.url.path,
        extras={"errors": exc.errors()},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return problem(
        status=500,
        title="Internal Server Error",
        detail="An unexpected error occurred",
        instance=request.url.path,
    )
