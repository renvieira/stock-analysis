from fastapi import APIRouter
from app.services.groq import GroqModel

from app.schemas.stocks import AIInput, AIOutput

stocks_router = APIRouter(prefix = "/api/v1/stocks", tags = ["stocks"])

groq = GroqModel()

@stocks_router.post("/analyze", response_model = AIOutput)
def analyze(ticker: AIInput):
    response = groq.get_response(ticker.ticker)
    return AIOutput(**response.model_dump()).model_dump()