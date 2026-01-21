from __future__ import annotations

from pathlib import Path

from app.utils import read_wav_bytes


def main():
    data_dir = Path("app/data/demo")
    if not data_dir.exists():
        raise SystemExit("Demo data directory not found. Run generate_demo_data.py first.")
    for wav_path in data_dir.glob("*.wav"):
        content = wav_path.read_bytes()
        sr, audio = read_wav_bytes(content)
        print(f"{wav_path.name}: {sr}Hz, {audio.shape[0]} samples")


if __name__ == "__main__":
    main()
