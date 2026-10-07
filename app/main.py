from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .exceptions import (
    general_exception_handler,
    validation_exception_handler
)

from .routers import (
    activity,
    dashboard,
    reports,
    templates
)


app = FastAPI(
    title="Reports Management API",
    description=(
        "FastAPI backend for Reports Dashboard "
        "and Report Activity Management"
    ),
    version="1.0.0"
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


app.include_router(
    dashboard.router
)

app.include_router(
    reports.router
)

app.include_router(
    activity.router
)

app.include_router(
    templates.router
)


@app.get("/")
def root():
    return {
        "success": True,
        "data": {
            "application": "Reports Management API",
            "version": "1.0.0"
        },
        "message": "API is running"
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "data": {
            "status": "healthy"
        },
        "message": "Service is healthy"
    }