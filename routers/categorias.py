from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencias import usuario_atual

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post(
    "",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(usuario_atual)],
)
def criar_categoria(dados: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    existente = db.scalar(select(models.Categoria).where(models.Categoria.nome == dados.nome))
    if existente:
        raise HTTPException(status_code=409, detail="Já existe uma categoria com esse nome.")
    categoria = models.Categoria(nome=dados.nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.get("", response_model=list[schemas.CategoriaRead])
def listar_categorias(db: Session = Depends(get_db)):
    return db.scalars(select(models.Categoria).order_by(models.Categoria.nome)).all()