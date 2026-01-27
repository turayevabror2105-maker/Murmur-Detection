$ErrorActionPreference = "Stop"

Write-Host "Starting backend..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Starting frontend..."
Start-Process -NoNewWindow -WorkingDirectory "frontend" -FilePath "npm" -ArgumentList "run dev"

Write-Host "Backend: http://localhost:8000/api"
Write-Host "Frontend: http://localhost:5173"
