from pydantic import BaseModel, Field
from typing import Literal, List

class AIResponse(BaseModel):
    cot: str = Field(description="cadeia de pensamento interna utilizada para chegar no resultado final (detalhada, com todos os pensamentos)")
    ticker: str = Field(description="string representando o ticker (exemplo: AAPL)")
    action: Literal['HOLD', 'BUY', 'SELL'] = Field(description="string representando 3 possíveis ações: 'HOLD', 'BUY', 'SELL'")
    confidence: float = Field(ge = 0, le = 1, description="float entre 0 e 1 representando a confiança na ação sugerida")
    reasoning: str = Field(description="string com o raciocínio para chegar na ação sugerida para ser apresentado ao usuário (com linguagem técnica)")
    risks: List[str] = Field(description="lista de strings com os riscos associados àquela ação e com links que podem complementar a explicação")
    opportunities: List[str] = Field(description="lista de strings com as oportunidades associadas àquela ação e com links que podem complementar a explicação")