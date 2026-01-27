import numpy as np
import librosa


def compute_mel_spectrogram(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    mel = librosa.feature.melspectrogram(
        y=samples,
        sr=sample_rate,
        n_fft=512,
        hop_length=256,
        n_mels=64,
        fmin=20,
        fmax=min(1000, sample_rate // 2),
        power=2.0,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    return mel_db
