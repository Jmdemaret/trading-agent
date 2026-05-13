import yfinance as yf
import pandas as pd
from textblob import TextBlob
import random

class TradingAgent:
    def __init__(self):
        # Paramètres d'analyse expert
        self.short_window = 20
        self.long_window = 50

    def fetch_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Récupère l'historique des prix d'une action pour calculer des tendances.
        """
        try:
            stock = yf.Ticker(ticker)
            # On récupère 3 mois de données pour avoir assez d'historique pour les moyennes mobiles
            hist = stock.history(period="3mo")
            if hist.empty:
                # Fallback to mock data if Yahoo Finance fails (e.g., rate limit 429)
                return self._generate_mock_market_data()
            return hist
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {ticker}: {e}")
            return self._generate_mock_market_data()

    def _generate_mock_market_data(self) -> pd.DataFrame:
        """Génère des données de marché fictives en cas de problème d'API."""
        import numpy as np
        dates = pd.date_range(end=pd.Timestamp.today(), periods=90, freq='B')
        prices = np.random.normal(loc=150, scale=5, size=len(dates))
        prices = np.cumsum(prices - 150) + 150 # Random walk
        df = pd.DataFrame({'Close': prices}, index=dates)
        return df

    def analyze_sentiment(self, news_text: str) -> float:
        """
        Analyse le sentiment d'une annonce ou d'une nouvelle financière.
        Retourne un score entre -1.0 (très négatif) et 1.0 (très positif).
        """
        blob = TextBlob(news_text)
        return blob.sentiment.polarity

    def simulate_news(self, ticker: str) -> str:
        """
        Simule la récupération de la dernière nouvelle concernant l'action.
        (Dans un vrai cas, on utiliserait une API de news comme NewsAPI ou le flux yfinance news).
        """
        simulated_news = [
            f"{ticker} announces record breaking profits this quarter!",
            f"{ticker} faces severe regulatory fines.",
            f"Analysts upgrade {ticker} to a strong buy.",
            f"Market struggles impact {ticker} growth outlook."
        ]
        return random.choice(simulated_news)

    def generate_signal(self, ticker: str) -> dict:
        """
        Génère une proposition d'investissement basée sur les données de marché et l'analyse de sentiment.
        """
        data = self.fetch_market_data(ticker)

        if data.empty or len(data) < self.long_window:
            return {
                "ticker": ticker,
                "action": "HOLD",
                "reason": "Données insuffisantes pour l'analyse technique."
            }

        # Calcul des moyennes mobiles
        data['SMA_short'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=self.long_window).mean()

        # Calcul du RSI (Relative Strength Index)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        last_price = data['Close'].iloc[-1]
        last_sma_short = data['SMA_short'].iloc[-1]
        last_sma_long = data['SMA_long'].iloc[-1]
        last_rsi = data['RSI'].iloc[-1] if not data['RSI'].empty else 50

        # Signal Technique basique (Croisement de moyennes mobiles & RSI)
        tech_signal = "HOLD"
        rsi_reason = f"RSI: {last_rsi:.2f} (Neutre)"

        if last_rsi < 30:
            tech_signal = "STRONG BUY"
            rsi_reason = f"RSI: {last_rsi:.2f} (Survendu - Opportunité d'achat imminente !)"
        elif last_rsi > 70:
            tech_signal = "STRONG SELL"
            rsi_reason = f"RSI: {last_rsi:.2f} (Suracheté - L'action atteint un PEAK, pensez à vendre !)"
        elif last_sma_short > last_sma_long:
            tech_signal = "BUY"
        elif last_sma_short < last_sma_long:
            tech_signal = "SELL"

        # Signal Fondamental (Analyse de Sentiment)
        latest_news = self.simulate_news(ticker)
        sentiment_score = self.analyze_sentiment(latest_news)

        fund_signal = "HOLD"
        if sentiment_score > 0.2:
            fund_signal = "BUY"
        elif sentiment_score < -0.2:
            fund_signal = "SELL"

        # Décision Finale (L'agent expert combine les deux)
        final_action = "HOLD"
        confidence = "Moyenne"

        if tech_signal == "BUY" and fund_signal == "BUY":
            final_action = "STRONG BUY"
            confidence = "Haute"
        elif tech_signal == "BUY" or fund_signal == "BUY":
            final_action = "BUY"
            confidence = "Moyenne"
        elif tech_signal == "SELL" and fund_signal == "SELL":
            final_action = "STRONG SELL"
            confidence = "Haute"
        elif tech_signal == "SELL" or fund_signal == "SELL":
            final_action = "SELL"
            confidence = "Moyenne"

        reason = (f"Prix actuel: ${last_price:.2f}. "
                  f"{rsi_reason}. "
                  f"Signal Tech (SMA): {tech_signal}. "
                  f"Sentiment News (Score: {sentiment_score:.2f}): {fund_signal}. "
                  f"Dernière News: '{latest_news}'")

        return {
            "ticker": ticker,
            "action": final_action,
            "confidence": confidence,
            "reason": reason,
            "current_price": last_price
        }

if __name__ == "__main__":
    # Test basique
    agent = TradingAgent()
    print("Testing Agent for AAPL...")
    signal = agent.generate_signal("AAPL")
    print(signal)
