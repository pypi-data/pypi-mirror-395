# app/routers/hero.py
from fastapi import HTTPException
from sqlmodel import Session, select
from ..model.models import Endereco, Pessoa
from ..model.dto import EnderecoCreate, EnderecoUpdate, EnderecoRead
from .generic import create_crud_router, Hooks

class enderecoHooks(Hooks[Endereco, EnderecoCreate, EnderecoUpdate]):
    def pre_create(self, payload: EnderecoCreate, session: Session) -> None:
        # se veio team_id, valida
        if payload.team_id is not None and payload.team_id != 0:
            if not session.get(Pessoa, payload.team_id):
                raise HTTPException(400, "team_id inválido")

    def pre_update(self, payload: EnderecoUpdate, session: Session, obj: Endereco) -> None:
        # se vai alterar team_id, valida
        if payload.team_id is not None:
            if payload.team_id != 0 and not session.get(Pessoa, payload.team_id):
                raise HTTPException(400, "team_id inválido")

router = create_crud_router(
    model=Endereco,
    create_schema=EnderecoCreate,
    update_schema=EnderecoUpdate,
    read_schema=EnderecoRead,
    prefix="/endereco",
    tags=["endereco"],
    hooks=enderecoHooks(),
)
