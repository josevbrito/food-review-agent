from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="FoodReview Insights Agent API",
    version="1.0.0",
    description="Backend powered by LangGraph & Llama 3"
)

# --- CONFIGURAÇÃO DE CORS ---
# Lista de origens permitidas
origins = [
    "http://localhost:3000",                    # Para testes locais
    "https://josevbrito.com",                   # Meu domínio oficial
    "https://www.josevbrito.com",               # Meu domínio com www
    "https://portfolio-sys-brito.vercel.app"    # Domínio padrão da Vercel (Backup)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Usa a lista específica em vez de ["*"]
    allow_credentials=True,     # Permissão de cookies/headers de autenticação se necessário
    allow_methods=["*"],        # Permissão de GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # Permissão de todos os headers
)

# Rotas
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "agent": "FoodReview Brain Online"}

@app.get("/")
def root():
    return {"message": "API is running. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    # Ajuste para rodar localmente se precisar
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)