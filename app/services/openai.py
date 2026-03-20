from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from typing import List

from app.ai.prompts.human_prompt import HUMAN_PROMPT
from app.ai.prompts.system_prompt import SYSTEM_PROMPT

from app.services.finance import Finance
from app.services.news import News

from app.ai.structured_outputs.ai_response import AIResponse

from app.core.settings import settings

class OpenAIModel:

    def __init__(self, model: str = "gpt-5.1", temperature: float = 0.1):
        self.model = ChatOpenAI(model=model, temperature=temperature, api_key=settings.GROQ_API_KEY).with_structured_output(AIResponse)

    def __get_messages(self, ticker: str) -> List[AnyMessage]:
        finance = Finance(ticker)
        news = News(ticker)
        stock_statistics = finance.get_report()
        stock_news = news.get_report()
        return [
            SystemMessage(content = SYSTEM_PROMPT.replace("{TICKER}", ticker)),
            HumanMessage(content = HUMAN_PROMPT.replace("{STOCK_STATISTICS}", stock_statistics).replace("{STOCK_NEWS}", stock_news))
        ]

    def get_response(self, ticker: str) -> AIResponse:
        return self.model.invoke(self.__get_messages(ticker))