from fastapi import FastAPI
from .util.database import get_session
from .controller.endereco import router as endereco_router
from .controller.pessoa import router as pessoa_router
from .util.database import init_db  

app = FastAPI(title="atividade 05 - mvc generics endereco e pessoa")

init_db()

#heroes iram virar enderecos 
app.include_router(endereco_router)

#teams iram virar pessoas
app.include_router(pessoa_router)

@app.get("/")
def health():
    return {"status": "ok"}
