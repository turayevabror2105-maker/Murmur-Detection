# Murmur Screen

Educational, non-diagnostic PCG murmur screening demo using a baseline log-mel feature pipeline with a lightweight classifier.

## Windows 11 Quick Start (click-by-click)

1. **Install Python 3.11**
   - Open Microsoft Store, search **Python 3.11**, click **Install**.
2. **Install Node.js LTS**
   - Visit https://nodejs.org and download the **LTS** installer.
3. **Open PowerShell**
   - Press **Start**, type **PowerShell**, open it.
4. **Navigate to the project**
   - `cd <path-to>/Murmur-Detection`
5. **Create a virtual environment**
   - `python -m venv .venv`
   - `.
   .venv\Scripts\activate`
6. **Install backend dependencies**
   - `pip install -r requirements.txt`
7. **Install frontend dependencies**
   - `cd frontend`
   - `npm install`
   - `cd ..`
8. **Generate demo WAV files**
   - `python scripts/generate_demo_data.py`
9. **Start everything (one command)**
   - `powershell -ExecutionPolicy Bypass -File windows_run.ps1`
10. **Open the app**
    - Frontend: http://localhost:5173
    - Backend API: http://localhost:8000/api

## Using the App

1. Go to **Upload**.
2. Drag & drop a WAV file or use the **Try Demo File** button.
3. Click **Run Analysis**.
4. View **Results**, **Quality**, **Triage**, **Risk**, **Reports**, and **History**.

## Demo Data

This repo avoids storing binary WAV files. Run `python scripts/generate_demo_data.py` to create demo WAVs in `app/data/demo/`.

## Backend Commands

- `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `python run_all.py` (train/eval/demo pipeline)

## Frontend Commands

- `cd frontend && npm run dev`
- `cd frontend && npm run test`

## Disclaimer

This software is for educational screening support only and does not provide medical diagnosis.
