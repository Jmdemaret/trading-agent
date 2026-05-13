import time
import schedule
from core.agent import TradingAgent
from notifications.telegram_bot import TelegramNotifier

def job():
    print("Démarrage du scan du marché...")
    agent = TradingAgent()
    notifier = TelegramNotifier()

    # Liste d'actifs à surveiller (pourrait être dynamique ou liée à la BDD de l'utilisateur)
    tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

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

    # Planifier l'exécution (par exemple toutes les 4 heures)
    # schedule.every(4).hours.do(job)

    # Pour le test on peut le mettre toutes les minutes
    # schedule.every(1).minutes.do(job)

    # print("En attente de la prochaine planification...")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
