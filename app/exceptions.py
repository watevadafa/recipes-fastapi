from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.constants import MISSING_REQUIRED_FIELDS_ERROR


async def custom_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=MISSING_REQUIRED_FIELDS_ERROR
    )
