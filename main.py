from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import Base, engine
from routers import auth, categorias, tarefas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tarefas", version="1.0.0")

ORIGENS_PERMITIDAS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(tarefas.router)


@app.get("/")
def raiz():
    return {"mensagem": "API de Tarefas funcionando"}