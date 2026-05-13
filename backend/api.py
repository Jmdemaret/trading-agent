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

# Modèle de données fictif de portefeuille
PORTFOLIO_DB = [
    {"ticker": "AAPL", "quantity": 50, "buyPrice": 150.0},
    {"ticker": "MSFT", "quantity": 30, "buyPrice": 300.0},
    {"ticker": "TSLA", "quantity": 20, "buyPrice": 200.0},
    {"ticker": "GOOGL", "quantity": 40, "buyPrice": 120.0}
]

@app.get("/api/portfolio")
def get_portfolio():
    return {"portfolio": PORTFOLIO_DB}

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
