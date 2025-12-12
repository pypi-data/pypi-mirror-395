from typing import Any, Dict, List, Optional
import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .exceptions import (
    AuthError,
    DuplicatedError,
    NotFoundError,
    PermissionDeniedError,
    UnauthorizedError,
    ValidationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    RateLimitExceededError,
    ServiceUnavailableError,
    GenericHttpError
)

logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    message: str,
    error: str,
    error_type: str,
    details: Optional[Any] = None,
    errors: Optional[List[Dict[str, Any]]] = None
) -> JSONResponse:
    """
    Create a standardized error response format
    """
    response_content = {
        "status_code": status_code or 500,
        "message": message,
        "error": error,
        "type": error_type,
    }

    if details:
        response_content["details"] = details
    if errors:
        response_content["errors"] = errors

    return JSONResponse(
        status_code=status_code or 500,
        content=response_content,
    )


def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request validation error: {exc.errors()}")

    errors = [
        {
            "field": ".".join(str(x) for x in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
            "input_value": err.get("input", None),
        }
        for err in exc.errors()
    ]

    return create_error_response(
        status_code=422,
        message="Request validation failed",
        error="Invalid request data",
        error_type="RequestValidationError",
        errors=errors,
    )


def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {exc}")
    return create_error_response(
        status_code=500,
        message="An unexpected error occurred",
        error=str(exc),
        error_type=exc.__class__.__name__,
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def duplicated_error_handler(request: Request, exc: DuplicatedError):

    return create_error_response(
        status_code=409,
        message="Duplicate entry found",
        error=str(exc.detail),
        error_type="DuplicatedError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def auth_error_handler(request: Request, exc: AuthError):

    return create_error_response(
        status_code=403,
        message="Authentication failed",
        error=str(exc.detail),
        error_type="AuthError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def not_found_error_handler(request: Request, exc: NotFoundError):
    logger.error(f"Not found error: {exc.detail}")
    return create_error_response(
        status_code=404,
        message="Resource not found",
        error=str(exc.detail),
        error_type="NotFoundError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def validation_error_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error: {exc.detail}")
    return create_error_response(
        status_code=422,
        message="Validation failed",
        error=str(exc.detail),
        error_type="ValidationError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def permission_denied_error_handler(request: Request, exc: PermissionDeniedError):

    return create_error_response(
        status_code=403,
        message="Permission denied",
        error=str(exc.detail),
        error_type="PermissionDeniedError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def unauthorized_error_handler(request: Request, exc: UnauthorizedError):

    return create_error_response(
        status_code=401,
        message="Unauthorized access",
        error=str(exc.detail),
        error_type="UnauthorizedError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )

def bad_request_error_handler(request: Request, exc: BadRequestError):
    return create_error_response(
        status_code=400,
        message="Bad request",
        error=str(exc.detail),
        error_type="BadRequestError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def conflict_error_handler(request: Request, exc: ConflictError):
    return create_error_response(
        status_code=409,
        message="Conflict occurred",
        error=str(exc.detail),
        error_type="ConflictError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def internal_server_error_handler(request: Request, exc: InternalServerError):
    logger.error(f"Internal server error: {exc.detail}")
    return create_error_response(
        status_code=500,
        message="Internal server error",
        error=str(exc.detail),
        error_type="InternalServerError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceededError):
    return create_error_response(
        status_code=429,
        message="Rate limit exceeded",
        error=str(exc.detail),
        error_type="RateLimitExceededError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )


def service_unavailable_handler(request: Request, exc: ServiceUnavailableError):
    return create_error_response(
        status_code=503,
        message="Service is currently unavailable",
        error=str(exc.detail),
        error_type="ServiceUnavailableError",
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )

def generic_http_error_handler(request: Request, exc: GenericHttpError):
    return create_error_response(
        status_code=exc.status_code,
        message=exc.message,
        error=str(exc.detail),
        error_type=exc.error_type,
        details={
            "path": request.url.path,
            "method": request.method,
        },
    )