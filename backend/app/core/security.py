from passlib.context import CryptContext
# Creamos un contexto de hashing que especificamos que use Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        # Verifica si la contraseña en texto plano coincide con el hash almacenado.
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        # Retorna el hash de la contraseña usando Bcrypt.
        return pwd_context.hash(password)