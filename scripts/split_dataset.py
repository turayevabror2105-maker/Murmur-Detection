from __future__ import annotations

from pathlib import Path
import random


def main():
    data_dir = Path("app/data/demo")
    files = list(data_dir.glob("*.wav"))
    if not files:
        raise SystemExit("No WAV files found. Run generate_demo_data.py first.")
    random.shuffle(files)
    split = int(0.8 * len(files))
    train = files[:split]
    val = files[split:]
    print("Train:")
    for f in train:
        print(f"  {f.name}")
    print("Validation:")
    for f in val:
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
