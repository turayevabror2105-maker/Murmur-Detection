import os
import wave

import numpy as np


def write_wav(path: str, freq: float, sr: int = 2000, dur: float = 4.0, amp: float = 0.3) -> None:
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    signal = amp * np.sin(2 * np.pi * freq * t)
    signal += 0.05 * np.sin(2 * np.pi * 2 * freq * t)
    pcm = (signal * 32767).astype(np.int16)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def main() -> None:
    out_dir = os.path.join('backend', 'data', 'demo_wavs')
    os.makedirs(out_dir, exist_ok=True)
    write_wav(os.path.join(out_dir, 'demo_aortic.wav'), freq=180)
    write_wav(os.path.join(out_dir, 'demo_pulmonic.wav'), freq=160)
    write_wav(os.path.join(out_dir, 'demo_mitral.wav'), freq=140)
    print('Demo WAVs generated in backend/data/demo_wavs')


if __name__ == '__main__':
    main()
