from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.endpoints import exercises, stats, workouts
from app.core import exception_handlers as handlers
from app.core.security_headers import SecurityHeadersMiddleware

app = FastAPI(title="Workout Log API")

app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(StarletteHTTPException, handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
app.add_exception_handler(Exception, handlers.generic_exception_handler)

app.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/")
def root():
    return {"message": "Workout Log API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Workout Log API"}
