from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.response import APIResponse
from app.exceptions.custom_exceptions import NotFoundException, ConflictException
from app.crud import user as user_crud
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate
# Crear un router para las rutas de usuarios
router = APIRouter(tags=["Users"], prefix="/users")
# Documentacion para los endpoints
responses = {
  "get_users": {
    status.HTTP_200_OK: {
      "description": "Usuarios encontrados",
      "content": {
        "application/json": {
          "example": {
            "status": "success",
            "message": "Usuarios encontrados",
            "data": [
              {
                "username": "user1",
                "email": "user1@example.com",
                "id": 1,
                "created_at": "2025-07-26T18:27:09"
              }
            ]
          }
        }
      }
    },
    status.HTTP_204_NO_CONTENT: {
      "description": "No se encontraron usuarios",
      "content": {
        "application/json": {
          "example": {
            "status": "no content",
            "message": "No se encontraron usuarios",
            "data": []
          }
        }
      }
    }
  },
  "get_user": {
    status.HTTP_200_OK: {
      "description": "Usuario encontrado",
      "content": {
        "application/json": {
          "example": {
            "status": "success",
            "message": "Usuario encontrado",
            "data": {
              "username": "user1",
              "email": "user1@example.com",
              "id": 1,
              "created_at": "2025-07-26T18:27:09"
            }
          }
        }
      }
    },
    status.HTTP_404_NOT_FOUND: {
      "description": "Usuario no encontrado",
      "content": {
        "application/json": {
          "example": {
            "status": "error",
            "message": "Usuario no encontrado",
            "data": None
          }
        }
      }
    }
  },
  "register_user": {
    status.HTTP_201_CREATED: {
      "description": "Usuario registrado exitosamente",
      "content": {
        "application/json": {
          "example": {
            "status": "created",
            "message": "Usuario registrado",
            "data": {
              "username": "user1",
              "email": "user1@example.com",
              "id": 1,
              "created_at": "2025-07-26T18:27:09"
            }
          }
        }
      }
    },
    status.HTTP_409_CONFLICT: {
      "description": "El usuario ya existe",
      "content": {
        "application/json": {
          "example": {
            "status": "error",
            "message": "El usuario ya existe",
            "data": None
          }
        }
      }
    }
  }
}
# Endpoint para obtener todos los usuarios
@router.get(
  "/",
  summary="Get All Users",
  description="Obtiene una lista de todos los usuarios registrados",
  response_model = APIResponse,
  responses=responses.get("get_users", {})  
)
def get_users(db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db=db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(APIResponse(status="success", message="Usuarios encontrados", data=users))
    ) if users else Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
# Endpoint para obtener un usuario por ID
@router.get(
  "/{user_id}",
  summary="Get User by ID",
  description="Obtiene un usuario por su ID",
  responses=responses.get("get_user", {})
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException(message="Usuario no encontrado")
    return JSONResponse(
    status_code=200,
        content=jsonable_encoder(APIResponse(status="success", message="Usuario encontrado", data=user))
    )
# Endpoint para registrar un nuevo usuario
@router.post(
  "/register",
  summary="Register User",
  description="Registra un nuevo usuario en el sistema",
  responses=responses.get("register_user", {})
)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    new_user = user_crud.create_user(data, db)
    if not new_user:
        raise ConflictException(message="El usuario ya existe")
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(APIResponse(status="created", message="Usuario registrado", data=new_user))
    )