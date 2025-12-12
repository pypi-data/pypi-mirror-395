# Exception Core Package

A comprehensive exception handling package for FastAPI applications that provides standardized error responses and exception handling.

## Features

- Pre-defined HTTP exceptions for common error scenarios
- Dynamic error creation for custom scenarios
- Standardized error response format
- Request validation error handling

## Installation

```bash
pip install abs-exception-core
```

## Usage

### 1. Import and Register Exception Handlers

```python
from fastapi import FastAPI
from abs_exception_core.exception_handlers import (
    request_validation_exception_handler,
    global_exception_handler,
    # ... other handlers
)

app = FastAPI()

# Register exception handlers
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
```

### 2. Using Pre-defined Exceptions

```python
from abs_exception_core.exceptions import (
    NotFoundError,
    ValidationError,
    AuthError,
    GenericHttpError,
    # ... other exceptions
)

# Example usage in a route
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if not item_exists(item_id):
        raise NotFoundError(detail="Item not found")
    
    if not has_permission():
        raise AuthError(detail="Insufficient permissions")
```

### 3. Using Generic Error

The `GenericHttpError` class allows you to create custom HTTP exceptions with any status code:

```python
# Create a custom error with status code 418
error = GenericHttpError(
    status_code=418,
    detail="I'm a teapot",
    headers={"X-Custom-Header": "value"}
)

# Create a custom error with just status code and message
error = GenericHttpError(
    status_code=451,
    detail="Unavailable For Legal Reasons"
)

# Create a custom error with just status code
error = GenericHttpError(status_code=402)
```

### Available Exceptions

- `DuplicatedError` (409 Conflict)
- `AuthError` (403 Forbidden)
- `NotFoundError` (404 Not Found)
- `ValidationError` (422 Unprocessable Entity)
- `PermissionDeniedError` (403 Forbidden)
- `UnauthorizedError` (401 Unauthorized)
- `BadRequestError` (400 Bad Request)
- `ConflictError` (409 Conflict)
- `InternalServerError` (500 Internal Server Error)
- `RateLimitExceededError` (429 Too Many Requests)
- `ServiceUnavailableError` (503 Service Unavailable)
- `GenericHttpError` (Custom Status Code) - For creating custom HTTP exceptions

### Error Response Format

All errors follow a standardized format:

```json
{
    "message": "Error message",
    "error": "Detailed error description",
    "type": "ErrorType",
    "details": {
        "path": "/api/endpoint",
        "method": "GET"
    },
    "errors": [
        {
            "field": "field_name",
            "message": "Validation message",
            "type": "error_type",
            "input_value": "invalid_value"
        }
    ]
}
```

## Best Practices

1. Use the most specific exception type that matches your error scenario
2. For custom status codes or scenarios not covered by standard exceptions, use `GenericHttpError`
3. Provide meaningful error details to help clients understand and resolve issues
4. Use custom headers sparingly and only when they provide additional value
5. Follow the standardized error response format for consistency

## License

This project is licensed under the MIT License - see the LICENSE file for details.
