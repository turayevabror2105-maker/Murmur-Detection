import torch
from torch import nn


class MurmurNet(nn.Module):
    def __init__(self, input_dim: int = 128, hidden_dim: int = 64, dropout_p: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_p),
            nn.Linear(hidden_dim, 2),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.net(features)


def build_demo_model(seed: int = 42) -> MurmurNet:
    torch.manual_seed(seed)
    model = MurmurNet()
    return model
