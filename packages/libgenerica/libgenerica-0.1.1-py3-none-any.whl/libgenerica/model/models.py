# app/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ---------- PESSOA ----------
class PessoaBase(SQLModel):

    name: str = Field(min_length=2, max_length=120)
    idade: int = Field(default=None, ge=0, le=150)
    email: str = Field(max_length=100, index=True)

class Pessoa(PessoaBase, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # back_populates liga Team <-> Hero
    enderecos: List["Endereco"] = Relationship(back_populates="pessoa")


# ---------- Endereco ----------
class EnderecoBase(SQLModel):
    name: str = Field(min_length=2, max_length=120)#caso a pessoa tenha mais de um endereco
    logradouro: str = Field(max_length=255)
    numero: str = Field(max_length=20)
    estado: str = Field(max_length=50)
    cidade: str = Field(max_length=100)
    bairro: str = Field(max_length=100)

class Endereco(EnderecoBase, table=True):
    
    Endereco_id: Optional[int] = Field(default=None, foreign_key="pessoa.id")
    pessoa: Optional[Pessoa] = Relationship(back_populates="enderecos")
    id: Optional[int] = Field(default=None, primary_key=True)