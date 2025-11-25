from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent import FoodReviewAgent

router = APIRouter()

agent_instance = FoodReviewAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal para conversar com o Agente.
    """
    try:
        print(f"📩 Recebido: {request.message}")
        ai_response = agent_instance.chat(request.message)
        return ChatResponse(response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))