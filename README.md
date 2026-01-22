# Murmur Screening Demo (Educational Only)

> **Important:** This project is a screening and educational demo only. It does **not** diagnose disease, provide treatment, or replace a clinician. Always consult a qualified healthcare professional for any health concern.

## Quick Start (Windows + Docker Desktop)

1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/
   - Ensure WSL2 is enabled (Docker Desktop will prompt you).
2. **Open PowerShell** and navigate to this folder:
   ```powershell
   cd path\to\Murmur-Detection
   ```
3. **Run the app** (this builds everything inside Docker):
   ```powershell
   docker compose up --build
   ```
4. Open these URLs:
   - Frontend UI: http://localhost:5173
   - API docs: http://localhost:8000/docs

## What This Demo Does

- Upload a heart sound **WAV** file
- Requires **patient ID** and **auscultation site** dropdown
- Produces a **non-diagnostic screening** result:
  - Murmur probability + calibrated probability
  - Systolic vs diastolic timing (S1–S2 vs S2–next S1 only)
  - Recording quality score + retake suggestion
  - Uncertainty estimation (MC-dropout)
  - Screening concern level (low/moderate/high)
  - Visualizations: waveform, mel-spectrogram, timeline, explainability heatmap
- Stores every analysis in **local SQLite** history
- Export JSON + printable summary

## Demo WAV Files

This repo avoids storing binary files. You can generate synthetic demo WAVs locally:
```bash
python scripts/generate_demo_wavs.py
```
Files will be created under:
```
backend/data/demo_wavs/
```
These are synthetic tones generated for demo purposes only.

## Optional Dataset Download (For Exploration)

You can download open datasets if you want to experiment with training:
```bash
python scripts/download_dataset.py
```
This downloads PhysioNet/CinC 2016 heart sound data (license: see https://physionet.org/content/challenge-2016/1.0.0/).

## Safety Disclaimers (Read Carefully)

- This tool is **not** a diagnostic device.
- It does **not** name diseases or provide treatment.
- Use only for learning, screening, and technical exploration.
- Recording quality can greatly impact results.

## Docker-Only Workflow (Recommended)

The frontend installs inside Docker. This avoids local Node/npm issues:
```bash
docker compose up --build
```

## NPM 403 Forbidden Troubleshooting

If `npm install` fails with a 403 error:
```bash
npm config set registry https://registry.npmjs.org/
npm config delete proxy
npm config delete https-proxy
npm config set strict-ssl true
```
If your network blocks npm, **use the Docker-only workflow** or a VPN.

## Alternative (pnpm) Install

If you prefer pnpm:
```bash
corepack enable
pnpm install --dir frontend
pnpm --dir frontend dev
```

## API Endpoints

- `GET /api/health`
- `POST /api/predict` (multipart form: `file`, `auscultation_site`, `patient_id`, optional `visit_label`)
- `GET /api/history?patient_id=...`
- `GET /api/history/{request_id}`
- `DELETE /api/history/{request_id}`

## Deployment Guide (Optional)

### Backend (Render)
1. Create a new **Web Service** on Render.
2. Set the root to `backend`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Set `DATABASE_URL` in Render environment variables (use Render's SQLite alternative or external Postgres).
6. Enable CORS by setting `VITE_API_URL` in the frontend to your Render URL.

### Frontend (Vercel)
1. Import the repo in Vercel.
2. Set the root to `frontend`.
3. Build command: `npm run build`
4. Output directory: `dist`
5. Add env var: `VITE_API_URL=https://your-render-backend.onrender.com`

## Troubleshooting

- **Docker not running**: Open Docker Desktop and start it.
- **Port already in use**: Stop other services on 5173/8000 or change ports in `docker-compose.yml`.
- **File upload errors**: Ensure WAV format and at least 1 second duration.
- **CORS errors**: Confirm `VITE_API_URL` points to your backend URL.

## Tests (Backend)

From the repo root:
```bash
cd backend
pytest
```

## License Notes

- PhysioNet/CinC 2016 dataset: https://physionet.org/content/challenge-2016/1.0.0/
- This repo is a demo only and is not cleared for clinical use.
