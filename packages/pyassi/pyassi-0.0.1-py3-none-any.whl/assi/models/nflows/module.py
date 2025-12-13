import torch
import torchaudio
import lightning as L
from omegaconf import OmegaConf
from assi.cli import run_cli

from nflows.flows.base import Flow
from nflows.distributions.normal import StandardNormal
from nflows.transforms.base import CompositeTransform
from nflows.transforms.autoregressive import MaskedAffineAutoregressiveTransform
from nflows.transforms.permutations import ReversePermutation
from nflows.transforms import BatchNorm


class NFLOWSModel(L.LightningModule):
    """Normalizing Flows model for acoustic anomaly detection"""

    def __init__(
        self,
        frame_length: int,
        channels: list[int] = [],
        num_layers: int = 3,
        transform_n_fft: int = 1024,
        transform_win_length: int = 1024,
        transform_hop_length: int = 512,
        transform_power: float = 2.0,
    ) -> None:
        super().__init__()

        self.frame_length = frame_length
        self.channels = tuple(channels)

        self.transform = torchaudio.transforms.Spectrogram(
            n_fft=transform_n_fft,
            win_length=transform_win_length,
            hop_length=transform_hop_length,
            power=transform_power,
            center=False,
        )

        freq_dim = transform_n_fft // 2 + 1
        windows = (self.frame_length - transform_n_fft) // transform_hop_length + 1
        self.features = windows * freq_dim * len(channels)

        base_dist = StandardNormal(shape=[self.features])
        base_dist._log_z = base_dist._log_z.to(torch.get_default_dtype())

        flow_transforms = []
        for _ in range(num_layers):
            flow_transforms.append(ReversePermutation(features=self.features))
            flow_transforms.append(
                MaskedAffineAutoregressiveTransform(
                    features=self.features, hidden_features=self.features * 2
                )
            )
            flow_transforms.append(BatchNorm(features=self.features))

        self.flow = Flow(
            transform=CompositeTransform(flow_transforms),
            distribution=base_dist,
        )

        self.save_hyperparameters()

    def forward(self, x: torch.Tensor):  # type: ignore[bad-override]
        # select channels
        x = x[..., self.channels, :, :]
        # flatten the tensor
        x = x.flatten(-3)
        # log scale
        x = torch.log(x + 1e-15)

        return self.flow.log_prob(inputs=x)

    def training_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x = self.transform(batch)
        x = self(x)
        loss = -x.mean()

        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )

        return loss

    def validation_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x = self.transform(batch)
        x = self(x)
        loss = -x.mean()

        self.log("val_loss", loss, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def predict_step(self, batch: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        x = self.transform(batch)
        x = self(x)
        loss = -x
        return loss


OmegaConf.register_new_resolver(
    "frame_length",
    lambda n_fft, hop_length, windows: n_fft + (windows - 1) * hop_length,
)


if __name__ == "__main__":
    run_cli(__file__, run=True)
