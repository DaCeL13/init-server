from fastapi import FastAPI, APIRouter, Form
from fastapi.responses import RedirectResponse
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import health, user
from app.exceptions.custom_exceptions import NotFoundException, DatabaseConnectionException, ConflictException
from app.exceptions.handlers import not_found_exception_handler, db_connection_exception_handler, conflict_exception_handler
# Metadatos para la documentación de OpenAPI
tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints para verificar el estado del sistema y la base de datos",
    },
    {
        "name": "Users",
        "description": "Operaciones relacionadas con usuarios: registro, login, perfil",
    },
]
# Crear la instancia de FastAPI
app = FastAPI(title="Initial Server API", version="1.0.0", openapi_tags=tags_metadata)
# Configurar los manejadores de excepciones
app.add_exception_handler(DatabaseConnectionException, db_connection_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)
# Crear un router para las rutas de la API
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health.router)
v1_router.include_router(user.router)
# Registrar el router health en la aplicación principal
app.include_router(v1_router)
# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirección desde raíz
@app.get("/", include_in_schema=False)
def redirect_to_health():
    return RedirectResponse(url="/api/v1/health/", status_code=301)