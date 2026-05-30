import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

# Clave para firmar los JWT
SECRET_KEY = os.getenv("JWT_SECRET", "clave-secreta-porthos-hace-la-mejor-hamburguesa")
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = int(os.getenv("JWT_EXPIRACION_MIN", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)

def hashear(contrasena: str) -> str:
    return pwd_context.hash(contrasena)

def verificar_contrasena(plana: str, hasheada: str) -> bool:
    return pwd_context.verify(plana, hasheada)

def crear_token(usuario: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    payload = {"sub": usuario, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    """Dependencia que valida el token JWT y devuelve el usuario. Sin token válido -> 401."""
    no_autorizado = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o ausente",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credenciales is None:
        raise no_autorizado
    try:
        payload = jwt.decode(credenciales.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise no_autorizado

    usuario = payload.get("sub")
    if not usuario:
        raise no_autorizado
    return usuario
