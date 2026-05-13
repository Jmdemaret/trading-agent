import time
import schedule
from core.agent import TradingAgent
from notifications.telegram_bot import TelegramNotifier

from backend.config_manager import config_manager

def job():
    print("Démarrage du scan du marché...")
    agent = TradingAgent()

    # Le notifier charge désormais dynamiquement ses clés depuis config.json
    notifier = TelegramNotifier()

    # Liste dynamique d'actifs à surveiller
    portfolio = config_manager.get_portfolio()
    # On ajoute quelques gros tickers par défaut pour la découverte d'opportunités
    discovery_tickers = ["NVDA", "AMZN", "META", "BTC-USD"]

    # Fusion sans doublon
    tickers = list(set([item["ticker"] for item in portfolio] + discovery_tickers))

    for ticker in tickers:
        print(f"Analyse de {ticker}...")
        signal = agent.generate_signal(ticker)

        # On n'envoie une notification que s'il y a un mouvement fort conseillé
        if signal['action'] in ["STRONG BUY", "STRONG SELL", "BUY", "SELL"]:
            emoji = "🟢" if "BUY" in signal['action'] else "🔴"
            message = (f"{emoji} ALERTE EXPERT IA : {ticker}\n"
                       f"Action recommandée: {signal['action']} (Confiance: {signal['confidence']})\n"
                       f"Détails: {signal['reason']}")

            notifier.send_alert(message)
        else:
            print(f"{ticker} - Aucun signal fort détecté ({signal['action']}).")

    print("Scan terminé. En attente du prochain cycle...")

if __name__ == "__main__":
    print("Agent de Trading Expert IA démarré.")
    print("Exécution immédiate du premier scan...")
    job()

    # Planifier l'exécution toutes les heures (paramétrable)
    schedule.every(1).hours.do(job)

    print("Démon en cours : En attente de la prochaine planification...")
    while True:
        schedule.run_pending()
        time.sleep(60)
