# Agent Expert en Trading (Fullstack: FastAPI + React)

Ce projet propose un agent expert en trading propulsé par l'IA. Il analyse le marché, trouve des opportunités d'investissement, peut envoyer des notifications, et fournit un tableau de bord React interactif pour suivre votre portefeuille.

## Architecture
- `core/` : Logique de l'agent de trading (récupération de données yfinance, analyse sentimentale).
- `notifications/` : Gestionnaire d'alertes Telegram.
- `backend/` : Serveur FastAPI exposant les capacités de l'agent via une API REST.
- `frontend/` : Application web Node.js/React (Vite) affichant le dashboard de suivi.

## Prérequis
- Python 3.9+
- Node.js 18+

## 1. Lancer le Backend (Python/FastAPI)

```bash
# Mettre à jour pip (recommandé, surtout sur Windows)
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur d'API (port 8000 par défaut)
python backend/api.py
# (Ou utiliser: uvicorn backend.api:app --reload)
```

## 2. Lancer le Frontend (Node.js/React)

Ouvrez un nouveau terminal :

```bash
cd frontend
npm install
npm run dev
```

L'interface web sera accessible à l'adresse indiquée par Vite (généralement `http://localhost:5173`).

## 3. Lancer l'application facilement sous Windows

Si vous êtes sous Windows, vous pouvez simplement double-cliquer sur le fichier `start.bat` à la racine du projet.
Il ouvrira automatiquement deux terminaux : un pour lancer l'API Python et un pour le frontend React.

### ⚠️ Dépannage: Erreur `ECONNREFUSED 127.0.0.1:8000`
Si vous voyez cette erreur dans le terminal de Vite (frontend), **cela signifie que votre Backend Python n'est pas allumé.**
Assurez-vous d'avoir exécuté la commande de l'étape 1 (`python backend/api.py`), ou utilisez simplement le script `start.bat`.

## 4. (Optionnel) Script de Notification Standalone

Vous pouvez toujours exécuter le démon d'analyse en arrière-plan qui enverra des alertes Telegram :
```bash
python main.py
```
