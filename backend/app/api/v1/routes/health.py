from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.utils.response import APIResponse
from app.exceptions.custom_exceptions import DatabaseConnectionException
# Crear un router para las rutas de testeo de salud
router = APIRouter(tags=["Health"], prefix="/health")
# Endpoint para verificar el estado del sistema
@router.get(
    "/", summary="Check System Health",
    description="Verifica el estado del sistema y devuelve un mensaje de éxito.",
    responses={
        status.HTTP_200_OK: {
            "description": "Sistema operativo y servidor funcionando correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "message": "Sistema operativo y servidor funcionando correctamente",
                        "data": None
                    }
                }
            }
        }
    }
)
def check_health():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(APIResponse(status="ok", message="Sistema operativo y servidor funcionando correctamente"))
    )   
# Endpoint para verificar la conexión a la base de datos
@router.get(
    "/db", summary="Check Database Connection",
    description="Verifica la conexión a la base de datos y devuelve un mensaje de éxito o error.",
    responses={
        status.HTTP_200_OK: {
            "description": "Conexión a la base de datos exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "message": "Conexión a la base de datos exitosa",
                        "data": None
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error al conectar con la base de datos",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Error al conectar con la base de datos",
                        "data": None
                    }
                }
            }
        }
    }
)
def check_database():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(APIResponse(status="ok", message="Conexión a la base de datos exitosa"))
        )
    except SQLAlchemyError as e:
        raise DatabaseConnectionException() from e
    finally:
        db.close()
