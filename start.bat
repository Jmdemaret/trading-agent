@echo off
echo Lancement du Backend FastAPI...
start cmd /k "python backend\api.py"

echo Lancement du Frontend React...
start cmd /k "cd frontend && npm run dev"

echo L'application demarre. Gardez les deux fenetres ouvertes.
