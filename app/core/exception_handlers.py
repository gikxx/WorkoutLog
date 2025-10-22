from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import problem


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return problem(status=exc.status_code, title="Error", detail=exc.detail)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return problem(
        status=422,
        title="Validation Error",
        detail="Invalid request parameters",
        extras={"errors": exc.errors()},
    )
