# Agent Expert en Trading

Ce projet propose un agent expert en trading propulsé par l'IA. Il analyse le marché, trouve des opportunités d'investissement, vous envoie des notifications (ex: Telegram), et fournit un tableau de bord pour suivre votre portefeuille.

## Fonctionnalités

1. **Analyse de marché**: Utilise les données financières (Yahoo Finance) et l'analyse de sentiment (TextBlob).
2. **Notifications**: Envoie des propositions d'investissement en temps réel.
3. **Tableau de bord de portefeuille**: Suivi des performances et recommandations révolutionnaires (Streamlit).

## Structure
- `core/`: Logique de l'agent de trading (récupération de données, analyse, génération de signaux).
- `notifications/`: Gestionnaire d'alertes Telegram.
- `app/`: Dashboard de suivi du portefeuille Streamlit.
- `main.py`: Point d'entrée pour lancer le bot de génération de signaux.

## Installation

```bash
pip install -r requirements.txt
```

## Démarrer le Dashboard

```bash
streamlit run app/dashboard.py
```

## Démarrer l'Agent

```bash
python main.py
```
