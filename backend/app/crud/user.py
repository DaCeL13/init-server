from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.security import Hasher
from app.exceptions.custom_exceptions import ValidationException
from fastapi import HTTPException
# Funcion para crear un nuevo usuario
def create_user(user: UserCreate, db: Session):
    # Verificar si el usuario ya existe
    existing_user = get_user_by_username(user.username, db)
    if existing_user:
        return None
    # Hashear la contraseña antes de guardarla
    hashed_password = Hasher.get_password_hash(user.password)
    try:
        # Crear una instancia del modelo User
        db_user = User(username=user.username, email=user.email, password=hashed_password)
    except ValidationException as e:
        raise ValidationException(message="Error al crear el usuario. Formato de datos inválido.") from e
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    # Agregar el usuario a la sesión de la base de datos
    try:
        db.add(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
    db.refresh(db_user)
    return UserOut.model_validate(db_user)
# Funcion para obtener todos los usuarios
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    if not users:
        return []
    return [UserOut.model_validate(user) for user in users]
# Funcion para obtener usuario por ID
def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return UserOut.model_validate(user)
# Funcion para obtener usuario por nombre de usuario
def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return UserOut.model_validate(user)
# Funcion para actualizar un usuario
# def update_user(user_id: int, user: UserUpdate, db: Session):
#     db_user = get_user_by_id(user_id, db)
#     if not db_user:
#         return None
#     for key, value in user.model_dump().items():
#         setattr(db_user, key, value)
#     db.commit()
#     db.refresh(db_user)
#     return db_user