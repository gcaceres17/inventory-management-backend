from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas
from ..utils import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from ..config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.Usuario)
def register(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(usuario.password)
        db_usuario = models.Usuario(nombre=usuario.nombre, email=usuario.email, hashed_password=hashed_password)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")

@router.post("/login")
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    try:
        db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
        if not db_usuario or not verify_password(usuario.password, db_usuario.hashed_password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_usuario.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")
    