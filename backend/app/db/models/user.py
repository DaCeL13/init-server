# app/db/models/user.py
from sqlalchemy import Column, String, DateTime, func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    # id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # ^^^ Este campo es heredado de la clase Base y no es necesario declararlo aquí.
    
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False) # Nota: Guarda el hash de la contraseña, no el texto plano
    # Delega la creación de la columna created_at a la clase Base con NOW() como valor por defecto
    created_at = Column(DateTime, server_default=func.now())