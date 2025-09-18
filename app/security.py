from datetime import datetime, timedelta, timezone # Agregado timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from passlib.context import CryptContext # Importación para hashing de contraseñas

from . import models, schemas
from .database import SessionLocal
from .config import settings
from . import crud  

# Contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_key_header = APIKeyHeader(name="X-API-Key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Funciones para el Hashing de Contraseñas
def hash_password(password: str) -> str:
    """Hashea una contraseña para almacenarla de forma segura."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña en texto plano con su versión hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

## Funciones para JWT y Autenticación
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        device_id: str = payload.get("sub")
        if device_id is None:
            raise credentials_exception
        return device_id
    except JWTError:
        raise credentials_exception

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

## Función de Dependencia para obtener el usuario actual
def get_current_user_by_token(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    # Esta función puede ser útil para proteger rutas
    # Requiere que el token tenga el email del usuario en 'sub'
    user = crud.get_user_by_email(db, email=token)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user