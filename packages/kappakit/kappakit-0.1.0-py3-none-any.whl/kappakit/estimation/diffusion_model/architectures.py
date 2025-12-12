import math
import torch
import torch.nn as nn
from transformers import PretrainedConfig, PreTrainedModel

class ResidualBlock(torch.nn.Module):
    def __init__(self, module):
        super().__init__()
        self.module = module
    def forward(self, inputs):
        return self.module(inputs) + inputs

# Sinusoidal timestep embedding
def timestep_embedding(timesteps: torch.Tensor, dim: int, max_period: int = 10_000) -> torch.Tensor:
    half = dim // 2
    device = timesteps.device
    freqs = torch.exp(-math.log(max_period) * torch.arange(half, device=device) / max(half, 1))
    args = timesteps[:, None] * freqs[None]
    emb = torch.cat([torch.cos(args), torch.sin(args)], dim=-1)
    if dim % 2 == 1:
        emb = torch.nn.functional.pad(emb, (0, 1))
    return emb

class FCNConfig(PretrainedConfig):
    model_type = "fcn"
    def __init__(
        self,
        input_dim: int = 3,
        output_dim: int = 3,
        num_layers: int = 5,
        width: int = 256,
        dropout: float = 0.0,
        time_emb_dim: int = 128,   # concat size
        max_time: int = 1000,      # divide raw steps by this
        data_mean=None,
        data_std=None,
        **kwargs,
    ):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.width = width
        self.dropout = dropout
        self.time_emb_dim = time_emb_dim
        self.max_time = max_time
        self.data_mean = data_mean
        self.data_std  = data_std
        super().__init__(**kwargs)

class FullyConnectedNetwork(PreTrainedModel):
    config_class = FCNConfig

    def __init__(self, config):
        super().__init__(config)
        Drop = lambda: (nn.Dropout(config.dropout) if (getattr(config, "dropout", 0.0) or 0.0) > 0 else nn.Identity())

        # First layer now includes LayerNorm on [x, t_emb]
        in_dim = config.input_dim + config.time_emb_dim
        self.first_layer = nn.Sequential(
            nn.LayerNorm(in_dim),                 # <-- added
            nn.Linear(in_dim, config.width),
            nn.ReLU(),
            Drop(),
            nn.Linear(config.width, config.width),
        )

        # Residual trunk
        blocks = []
        for _ in range(config.num_layers - 2):
            blocks.append(
                ResidualBlock(
                    nn.Sequential(
                        nn.Linear(config.width, config.width),
                        nn.ReLU(),
                        Drop(),
                    )
                )
            )
        blocks += [Drop(), nn.Linear(config.width, config.output_dim)]
        self.fc_layers = nn.Sequential(*blocks)

        # Normalization stats
        self.data_mean = torch.Tensor(config.data_mean)
        self.data_std = torch.Tensor(config.data_std)

    def normalize(self, x: torch.Tensor) -> torch.Tensor:
        return (x - self.data_mean.to(x.device)) / (self.data_std.to(x.device) + 1e-6)

    def denormalize(self, x: torch.Tensor) -> torch.Tensor:
        return x * self.data_std.to(x.device) + self.data_mean.to(x.device)

    def forward(self, x, timesteps=None, return_dict=None):
        if len(x.shape) > 2:
            x = x.squeeze()

        x = self.normalize(x)

        if timesteps is not None:
            if timesteps.dim() == 0:
                timesteps = timesteps[None]
            if timesteps.numel() == 1 and x.shape[0] > 1:
                timesteps = timesteps.expand(x.shape[0])
            t = timesteps.to(dtype=torch.float32).view(-1) / float(self.config.max_time)
            t_emb = timestep_embedding(t, dim=self.config.time_emb_dim).to(dtype=x.dtype)
        else:
            t_emb = torch.zeros(x.shape[0], self.config.time_emb_dim, device=x.device, dtype=x.dtype)

        x = torch.cat([x, t_emb], dim=-1)   # (B, input_dim + time_emb_dim)
        x = self.first_layer(x)
        x = self.fc_layers(x)
        # x = self.denormalize(x)
        return x
