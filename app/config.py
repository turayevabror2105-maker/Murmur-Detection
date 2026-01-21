from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
DEMO_DIR = DATA_DIR / "demo"
UPLOAD_DIR = BASE_DIR / "artifacts" / "uploads"
RUNS_DIR = BASE_DIR / "artifacts" / "runs"
MODEL_DIR = BASE_DIR / "artifacts"
DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"
MAX_UPLOAD_MB = 20

MODEL_PATH = MODEL_DIR / "model.pkl"
CALIBRATOR_PATH = MODEL_DIR / "calibrator.pkl"
CONFIG_PATH = MODEL_DIR / "config.json"
