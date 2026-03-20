import requests
import json
from app.core.settings import settings

class News:

    def __init__ (self, ticker: str, time_period: str = "last_month", engine: str = "google"):
        self.ticker = ticker
        self.time_period = time_period
        self.engine = engine
        self.URL = "https://www.searchapi.io/api/v1/search"

    def __get_organic_results(self) -> list:
        params = {
        "engine": self.engine,
        "q": f"{self.ticker} stock news",
        "api_key": settings.SEARCH_API_KEY,
        "time_period": self.time_period
        }

        response = requests.get(self.URL, params=params)
        return json.loads(response.text).get("organic_results", [])
    
    def get_report(self) -> str:
        STOCK_NEWS = f"Notícias sobre {self.ticker}\n"
        organic_results = self.__get_organic_results()
        for noticia in organic_results:
            position = noticia.get('position', 'Não encontrado')
            link = noticia.get('link', 'Não encontrado')
            source = noticia.get('source', 'Não encontrado')
            snippet = noticia.get('snippet', 'Não encontrado')
            STOCK_NEWS += f"""
            Posição das pesquisa: {position}
            Link: {link}
            Fonte: {source}
            Trecho: {snippet}
            """
        return STOCK_NEWS