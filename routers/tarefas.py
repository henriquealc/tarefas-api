from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencias import usuario_atual

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


def obter_tarefa_ou_404(tarefa_id: int, db: Session) -> models.Tarefa:
    tarefa = db.get(models.Tarefa, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return tarefa


@router.post(
    "",
    response_model=schemas.TarefaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(usuario_atual)],
)
def criar_tarefa(dados: schemas.TarefaCreate, db: Session = Depends(get_db)):
    categoria = db.get(models.Categoria, dados.categoria_id)
    if categoria is None:
        raise HTTPException(status_code=400, detail="A categoria informada não existe.")
    tarefa = models.Tarefa(
        titulo=dados.titulo,
        descricao=dados.descricao,
        concluida=dados.concluida,
        categoria_id=dados.categoria_id,
    )
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.get("", response_model=list[schemas.TarefaRead])
def listar_tarefas(
    concluida: bool | None = None,
    categoria_id: int | None = None,
    db: Session = Depends(get_db),
):
    consulta = select(models.Tarefa)
    if concluida is not None:
        consulta = consulta.where(models.Tarefa.concluida == concluida)
    if categoria_id is not None:
        consulta = consulta.where(models.Tarefa.categoria_id == categoria_id)
    return db.scalars(consulta.order_by(models.Tarefa.id)).all()


@router.get("/{tarefa_id}", response_model=schemas.TarefaRead)
def consultar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    return obter_tarefa_ou_404(tarefa_id, db)


@router.patch(
    "/{tarefa_id}",
    response_model=schemas.TarefaRead,
    dependencies=[Depends(usuario_atual)],
)
def atualizar_tarefa(tarefa_id: int, dados: schemas.TarefaUpdate, db: Session = Depends(get_db)):
    tarefa = obter_tarefa_ou_404(tarefa_id, db)
    campos = dados.model_dump(exclude_unset=True)
    for campo in ("titulo", "concluida", "categoria_id"):
        if campo in campos and campos[campo] is None:
            raise HTTPException(status_code=400, detail=f"O campo '{campo}' não pode ser nulo.")
    if "categoria_id" in campos and db.get(models.Categoria, campos["categoria_id"]) is None:
        raise HTTPException(status_code=400, detail="A categoria informada não existe.")
    for campo, valor in campos.items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete(
    "/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(usuario_atual)],
)
def excluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = obter_tarefa_ou_404(tarefa_id, db)
    db.delete(tarefa)
    db.commit()