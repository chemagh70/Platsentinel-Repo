from datetime import datetime, timedelta

from app.configuracion import settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Autenticación"])

usuarios = {
    "admin": {"username": "admin", "password": "segura123"},
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = usuarios.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    payload = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + timedelta(minutes=settings.duracion_token)
    }
    token = jwt.encode(payload, settings.clave_jwt, algorithm=settings.algoritmo_jwt)
    return {"access_token": token, "token_type": "bearer"}
