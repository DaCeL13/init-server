from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr

# Esta clase sirve como base para todos los modelos de SQLAlchemy.
class Base(DeclarativeBase):
    # Definición de la columna ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()