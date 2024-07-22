import bcrypt
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi.security import OAuth2PasswordBearer
from ..config import settings
from datetime import datetime, timedelta
import jwt 
from jwt.exceptions import DecodeError, ExpiredSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_reset_token(email: str, expires_delta: timedelta):
    """
    Genera un token JWT para restablecimiento de contraseña con el email y tiempo de expiración especificados.
    """
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_reset_token(token: str):
    """
    Verifica y decodifica el token JWT de restablecimiento de contraseña para obtener el email asociado.
    """
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = decoded_token.get("sub")
        if email is None:
            raise JWTError("Invalid token")
        return email
    except ExpiredSignatureError:
        # El token ha expirado
        return None
    except JWTError:
        # El token es inválido
        return None