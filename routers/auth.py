from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
import security
from database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registro", response_model=schemas.UsuarioRead, status_code=status.HTTP_201_CREATED)
def registrar(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.scalar(select(models.Usuario).where(models.Usuario.username == dados.username))
    if existente:
        raise HTTPException(status_code=409, detail="Nome de usuário já está em uso.")
    usuario = models.Usuario(
        username=dados.username,
        senha_hash=security.gerar_hash(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=schemas.Token)
def login(formulario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.scalar(select(models.Usuario).where(models.Usuario.username == formulario.username))
    if usuario is None or not security.verificar_senha(formulario.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": security.criar_token(usuario.username), "token_type": "bearer"}