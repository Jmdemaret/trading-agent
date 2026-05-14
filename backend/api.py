import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ajouter la racine pour importer core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.agent import TradingAgent

app = FastAPI(title="AI Trading API")

# Activer CORS pour permettre au frontend React de communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod, mettre l'URL du front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = TradingAgent()

from backend.config_manager import config_manager
import yfinance as yf

class PortfolioItem(BaseModel):
    ticker: str
    quantity: float
    buyPrice: float

class TransactionItem(BaseModel):
    type: str # "BUY" or "SELL"
    ticker: str
    quantity: float
    price: float

class TelegramSettings(BaseModel):
    token: str
    chat_id: str

@app.get("/api/portfolio")
def get_portfolio():
    return {"portfolio": config_manager.get_portfolio()}

@app.post("/api/portfolio")
def add_portfolio_item(item: PortfolioItem):
    config_manager.add_to_portfolio(item.dict())
    return {"status": "success", "portfolio": config_manager.get_portfolio()}

@app.delete("/api/portfolio/{ticker}")
def remove_portfolio_item(ticker: str):
    config_manager.remove_from_portfolio(ticker)
    return {"status": "success", "portfolio": config_manager.get_portfolio()}

@app.get("/api/chart/{ticker}")
def get_chart_data(ticker: str, period: str = "1mo"):
    try:
        stock = yf.Ticker(ticker)
        # Period valid strings: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": "Aucune donnée trouvée"}

        data = []
        for date, row in hist.iterrows():
            data.append({
                "x": date.strftime('%Y-%m-%d'),
                "y": [round(row['Open'], 2), round(row['High'], 2), round(row['Low'], 2), round(row['Close'], 2)],
                "volume": int(row['Volume'])
            })

        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/transactions")
def get_transactions():
    return {"transactions": config_manager.get_transactions()}

@app.post("/api/transactions")
def add_transaction(item: TransactionItem):
    transaction = config_manager.add_transaction(
        type_action=item.type,
        ticker=item.ticker,
        quantity=item.quantity,
        price=item.price
    )
    return {"status": "success", "transaction": transaction, "portfolio": config_manager.get_portfolio()}

@app.get("/api/portfolio/live")
def get_portfolio_live():
    portfolio = config_manager.get_portfolio()
    live_data = []

    for item in portfolio:
        ticker = item["ticker"]
        try:
            stock = yf.Ticker(ticker)
            # Récupérer les données du jour et du jour précédent pour le changement
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_percent = ((current_price - prev_price) / prev_price) * 100
            else:
                current_price = item["buyPrice"]
                change_percent = 0.0

        except Exception:
            current_price = item["buyPrice"]
            change_percent = 0.0

        live_data.append({
            "ticker": ticker,
            "quantity": item["quantity"],
            "buyPrice": item["buyPrice"],
            "currentPrice": current_price,
            "changePercent": change_percent,
            "totalValue": current_price * item["quantity"],
            "profit": (current_price - item["buyPrice"]) * item["quantity"]
        })

    return {"live_portfolio": live_data}

@app.get("/api/settings")
def get_settings():
    return config_manager.get_telegram_config()

@app.post("/api/settings")
def update_settings(settings: TelegramSettings):
    config_manager.set_telegram_config(settings.token, settings.chat_id)
    return {"status": "success"}

@app.get("/api/analyze/{ticker}")
def analyze_ticker(ticker: str):
    try:
        signal = agent.generate_signal(ticker)
        return {"signal": signal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rebalance")
def get_rebalance_prediction():
    # Simulation des données "révolutionnaires"
    current_allocation = [
        {"name": "AAPL", "value": 35},
        {"name": "MSFT", "value": 30},
        {"name": "TSLA", "value": 15},
        {"name": "GOOGL", "value": 20}
    ]
    recommended_allocation = [
        {"name": "AAPL", "value": 20},
        {"name": "MSFT", "value": 40},
        {"name": "TSLA", "value": 5},
        {"name": "GOOGL", "value": 35}
    ]
    return {
        "current": current_allocation,
        "recommended": recommended_allocation,
        "reasoning": "L'IA recommande d'augmenter votre exposition sur MSFT et GOOGL en raison de signaux fondamentaux forts sur l'IA générative, tout en réduisant TSLA à cause d'une analyse de sentiment négative récente."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
