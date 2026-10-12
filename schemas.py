from pydantic import BaseModel, ConfigDict, Field

class CategoriaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=50)

class CategoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str

class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)
    concluida: bool = False
    categoria_id: int

class TarefaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)
    concluida: bool | None = None
    categoria_id: int | None = None

class TarefaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None
    concluida: bool
    categoria_id: int

class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    senha: str = Field(min_length=6, max_length=128)


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"