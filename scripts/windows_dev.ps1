$ErrorActionPreference = "Stop"

if (-not (Test-Path "backend\.venv")) {
  python -m venv backend\.venv
}

backend\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend\requirements.txt

if (-not (Test-Path "frontend\node_modules")) {
  corepack enable | Out-Null
  npm install --prefix frontend
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
