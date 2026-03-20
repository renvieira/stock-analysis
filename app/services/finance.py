from yfinance import Ticker
import pandas as pd


class Finance:

    def __init__(self, ticker: str, period: str = "1y", interval: str = "1d"):
        self.ticker = ticker
        self.period = period
        self.interval = interval

    def get_history(self) -> pd.DataFrame:
        return Ticker(ticker=self.ticker).history(period=self.period, interval=self.interval)
    
    def __calc_rsi(self, delta: pd.Series, period: int = 14) -> float:
        gain = delta.copy()
        loss = delta.copy()

        gain[gain < 0] = 0
        loss[loss > 0] = 0
        loss = abs(loss)

        #Calculate exponential moving average of gains and losses
        avg_gain = gain.ewm(com=period-1, adjust=False).mean()
        avg_loss = loss.ewm(com=period-1, adjust=False).mean()

        #Calculate Relative Strength (RS)
        rs = avg_gain / avg_loss

        #Calculate Relative Strength Index (RSI)
        temp = 100 - (100 / (1 + rs))

        # Return last RSI value
        return float(temp.iloc[-1]) 

    def calc_statistics(self) -> dict:
        df = self.get_history()
        df['Return'] = df['Close'].pct_change()
        df['Diff'] = df['Close'].diff()

        #Estatisticas
        avg_return = df['Return'].mean()
        median_return = df['Return'].median()
        cumulative_return = df['Close'].iloc[-1]/df['Close'].iloc[0] -1
        max_price = df['Close'].max()
        min_price = df['Close'].min()
        avg_price = df['Close'].mean()
        median_price = df['Close'].median()
        curr_price = df['Close'].iloc[-1]
        volatility = df['Close'].std()
        last_rsi = self.__calc_rsi(delta=df['Diff'], period=14)

        return {
            "avg_return": avg_return,
            "median_return": median_return,
            "cumulative_return": cumulative_return,
            "max_price": max_price,
            "min_price": min_price,
            "avg_price": avg_price,
            "median_price": median_price,
            "curr_price": curr_price,
            "volatility": volatility,
            "last_rsi": last_rsi
        }

    def get_report(self) -> str:
        stock_statistics = self.calc_statistics()

        return f"""
Retorno diário médio: {stock_statistics.get('avg_return', 'N/A'):.4f}
Retorno mediano: {stock_statistics.get('median_return', 'N/A'):.4f}
Retorno acumulado: {stock_statistics.get('cumulative_return', 'N/A'):.4f}
Preço máximo: {stock_statistics.get('max_price', 'N/A'):.2f}
Preço mínimo: {stock_statistics.get('min_price', 'N/A'):.2f}
Preço médio: {stock_statistics.get('avg_price', 'N/A'):.2f}
Preço mediano: {stock_statistics.get('median_price', 'N/A'):.2f}
Preço atual: {stock_statistics.get('curr_price', 'N/A'):.2f}
Volatilidade: {stock_statistics.get('volatility', 'N/A'):.2f}
RSI atual: {stock_statistics.get('last_rsi', 'N/A'):.2f}
        """  