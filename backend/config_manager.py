import json
import os

CONFIG_FILE = "config.json"

import datetime

DEFAULT_CONFIG = {
    "telegram": {
        "token": "",
        "chat_id": ""
    },
    "portfolio": [
        {"ticker": "AAPL", "quantity": 50, "buyPrice": 150.0},
        {"ticker": "MSFT", "quantity": 30, "buyPrice": 300.0}
    ],
    "transactions": []
}

class ConfigManager:
    def __init__(self):
        self._load()

    def _load(self):
        if not os.path.exists(CONFIG_FILE):
            self.config = DEFAULT_CONFIG.copy()
            self.save()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)

        # Assurer que les clés existent
        if "telegram" not in self.config:
            self.config["telegram"] = {"token": "", "chat_id": ""}
        if "portfolio" not in self.config:
            self.config["portfolio"] = []
        if "transactions" not in self.config:
            self.config["transactions"] = []

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_portfolio(self):
        return self.config.get("portfolio", [])

    def add_to_portfolio(self, item):
        self.config["portfolio"].append(item)
        self.save()

    def remove_from_portfolio(self, ticker):
        self.config["portfolio"] = [i for i in self.config["portfolio"] if i["ticker"] != ticker]
        self.save()

    def get_transactions(self):
        return self.config.get("transactions", [])

    def add_transaction(self, type_action, ticker, quantity, price, date=None):
        if date is None:
            date = datetime.datetime.now().isoformat()

        transaction = {
            "id": len(self.config["transactions"]) + 1,
            "date": date,
            "type": type_action,
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "total": quantity * price
        }
        self.config["transactions"].append(transaction)

        # Mettre à jour le portfolio automatiquement
        portfolio = self.config["portfolio"]
        existing = next((item for item in portfolio if item["ticker"] == ticker), None)

        if type_action == "BUY":
            if existing:
                # Moyenne pondérée du prix d'achat
                total_cost = (existing["quantity"] * existing["buyPrice"]) + (quantity * price)
                existing["quantity"] += quantity
                existing["buyPrice"] = total_cost / existing["quantity"]
            else:
                self.config["portfolio"].append({"ticker": ticker, "quantity": quantity, "buyPrice": price})

        elif type_action == "SELL":
            if existing:
                existing["quantity"] -= quantity
                if existing["quantity"] <= 0:
                    self.config["portfolio"] = [i for i in self.config["portfolio"] if i["ticker"] != ticker]

        self.save()
        return transaction

    def get_telegram_config(self):
        return self.config.get("telegram", {})

    def set_telegram_config(self, token, chat_id):
        self.config["telegram"]["token"] = token
        self.config["telegram"]["chat_id"] = chat_id
        self.save()

config_manager = ConfigManager()
