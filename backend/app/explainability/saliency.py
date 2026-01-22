import numpy as np
import torch


def saliency_heatmap(model: torch.nn.Module, mel_db: np.ndarray) -> np.ndarray:
    model.eval()
    mel_tensor = torch.tensor(mel_db, dtype=torch.float32, requires_grad=True)
    features = torch.cat([mel_tensor.mean(dim=1), mel_tensor.std(dim=1)], dim=0)
    logits = model(features)
    murmur_logit = logits[0]
    murmur_logit.backward()
    grads = mel_tensor.grad.detach().abs().numpy()
    heatmap = grads / (np.max(grads) + 1e-6)
    return heatmap
