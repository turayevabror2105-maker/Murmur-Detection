from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io.wavfile import write

from app.ml.synthetic import generate_synthetic_pcg


def main():
    out_dir = Path("app/data/demo")
    out_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(3):
        audio = generate_synthetic_pcg(sr=2000, duration=6.0, murmur=idx % 2 == 0)
        path = out_dir / f"demo_{idx + 1}.wav"
        write(path, 2000, (audio * 32767).astype(np.int16))
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
