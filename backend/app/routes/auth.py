from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import UserCreate, User, Email
from ..utils.db import users_collection
from ..utils.auth import verify_password, get_password_hash, create_access_token, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from ..config import settings  # Asegúrate de importar settings desde el archivo correcto
from ..utils.mail import send_reset_password_email  # Importa la función para enviar correo
from datetime import datetime, timedelta
from ..utils.auth import create_reset_token, verify_reset_token
import logging


router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    await users_collection.insert_one(user_dict)
    return User(**user_dict)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": create_access_token(data={"sub": user["email"]}), "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    token: str

@router.post("/validate-token")
async def validate_token(token_data: TokenData):
    token = token_data.token
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        # You can add additional validation here if needed
        return {"valid": True}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ForgotPasswordResponse(BaseModel):
    message: str

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(email: Email):
    logger.info("Mensaje informativo")
    logger.info(f"Received request to reset password for email: {email.email}")
    user = await users_collection.find_one({"email": email.email})
    if user:
        # Generar token de restablecimiento de contraseña
        expires_delta = timedelta(hours=1)  # Ejemplo: el token expira en 1 hora
        reset_token = create_reset_token(email.email, expires_delta)
        logger.info(f"Reset token generated for email: {email.email}")
        
        # Enviar email con el token
        send_reset_password_email(email.email, reset_token)
        return {"message": "Password reset instructions sent to your email"}

    raise HTTPException(status_code=404, detail="User not found")

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    email = verify_reset_token(request.token)
    if email:
        # Actualizar la contraseña en la base de datos
        hashed_password = get_password_hash(request.new_password)
        await users_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
        return {"message": "Password reset successfully"}

    raise HTTPException(status_code=400, detail="Invalid or expired token")