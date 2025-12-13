import torch
from torch import nn
import torchaudio
import lightning as L
from assi.cli import run_cli
from torch.nn.functional import mse_loss


class AENet(nn.Module):
    """DCASE Challenge baseline autoencoder

    From https://github.com/nttcslab/dcase2023_task2_baseline_ae
    """

    def __init__(self, input_dim):
        super(AENet, self).__init__()
        self.input_dim = input_dim

        self.encoder = nn.Sequential(
            nn.Linear(self.input_dim, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 8),
            nn.BatchNorm1d(8, momentum=0.01, eps=1e-03),
            nn.ReLU(),
        )

        self.decoder = nn.Sequential(
            nn.Linear(8, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.BatchNorm1d(128, momentum=0.01, eps=1e-03),
            nn.ReLU(),
            nn.Linear(128, self.input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z), z


class AEModel(L.LightningModule):
    def __init__(
        self,
        channels: list[int],
        input_dim: int,
        transform_n_fft: int = 1024,
        transform_hop_length: int = 512,
        transform_power: float = 2.0,
    ):
        super().__init__()
        self.channels = channels
        self.input_dim = input_dim

        self.transform = torchaudio.transforms.MelSpectrogram(
            n_fft=transform_n_fft,
            hop_length=transform_hop_length,
            power=transform_power,
            center=False,
        )
        self.ae = AENet(input_dim=input_dim)
        self.loss_fn = nn.MSELoss()
        self.save_hyperparameters()

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        return self.ae(x)

    def transform_batch(self, batch):
        batch = self.transform(batch[:, self.channels])
        return batch.flatten(start_dim=1)

    def training_step(self, batch: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        x_prepared = self.transform_batch(batch)
        x_decoded, z = self(x_prepared)
        loss = self.loss_fn(x_decoded, x_prepared)
        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )
        return loss

    def validation_step(self, batch: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        x_prepared = self.transform_batch(batch)
        x_decoded, z = self(x_prepared)
        loss = self.loss_fn(x_decoded, x_prepared)
        self.log("val_loss", loss, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def predict_step(self, batch: torch.Tensor) -> torch.Tensor:  # type: ignore[bad-override]
        x_prepared = self.transform_batch(batch)
        x_decoded, z = self(x_prepared)
        loss = mse_loss(x_decoded, x_prepared, reduction="none").mean(dim=1)
        return loss


if __name__ == "__main__":
    run_cli(__file__, run=True)
