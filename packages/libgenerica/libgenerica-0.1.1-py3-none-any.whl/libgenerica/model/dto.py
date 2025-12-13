from .models import EnderecoBase, PessoaBase
from typing import  List, Optional
from sqlmodel import Field



class PessoaCreate(PessoaBase):
    pass

class PessoaPublic(PessoaBase):
    id: int
    model_config = {"from_attributes": True}

class PessoaWithenderecos(PessoaPublic):
    heroes: List["EnderecoPublic"] = []
    model_config = {"from_attributes": True}

class PessoaCreate(PessoaBase):
    pass

class PessoaRead(PessoaBase):
    id: int

class PessoaUpdate(PessoaBase):
    name: Optional[str] = None


class EnderecoCreate(EnderecoBase):
    team_id: Optional[int] = None  # permite já criar vinculado a um time

class EnderecoUpdate(EnderecoBase):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    secret_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=200)
    
class EnderecoPublic(EnderecoBase):
    id: int
    model_config = {"from_attributes": True}

class EnderecoRead(EnderecoBase):
    id: int
    team_id: Optional[int] = None
