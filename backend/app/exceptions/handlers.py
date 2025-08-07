from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.utils.response import APIResponse
from app.exceptions.custom_exceptions import NotFoundException, DatabaseConnectionException, ConflictException, ValidationException

# Estructura para la excepción NotFoundException
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(APIResponse(status="error", message=exc.message, data=None))
    )
# Estructura para la excepción DatabaseConnectionException
def db_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(APIResponse(status="error", message=exc.message, data=None))
    )
# Estructura para la excepción ConflictException
def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder(APIResponse(status="error", message=exc.message, data=None))
    )
# Estructura para la excepción RequestValidationError
def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(APIResponse(status="error", message=exc.message, data=None))
    )