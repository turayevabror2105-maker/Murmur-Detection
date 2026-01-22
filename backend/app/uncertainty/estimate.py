import numpy as np
import torch


def mc_dropout_uncertainty(model: torch.nn.Module, features: torch.Tensor, passes: int = 20) -> tuple[float, float]:
    model.train()
    probs = []
    with torch.no_grad():
        for _ in range(passes):
            logits = model(features)
            murmur_prob = torch.sigmoid(logits[0]).item()
            probs.append(murmur_prob)
    model.eval()
    probs_arr = np.array(probs, dtype=np.float32)
    mean_prob = float(np.mean(probs_arr))
    variance = float(np.var(probs_arr))
    uncertainty_score = min(1.0, variance * 10.0)
    return mean_prob, uncertainty_score
