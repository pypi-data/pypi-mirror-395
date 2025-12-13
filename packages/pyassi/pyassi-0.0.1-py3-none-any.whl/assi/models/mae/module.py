import torch
import torch.nn as nn
import torchaudio
from typing import Literal
import lightning as L
from assi.cli import run_cli


class PositionalEncoding(nn.Module):
    """
    Add positional encoding to input embeddings.

    This module learns positional information by adding a learnable parameter
    to the input embeddings, allowing the model to distinguish between different
    positions in the sequence.

    The operation is defined as:

    .. math::

        y = x + \text{pos_embed}

    where pos_embed is a learnable parameter.

    Parameters
    ----------
    number_of_patches : int
        Number of patches in the input sequence
    embed_dim : int
        Dimensionality of the embedding space
    """

    def __init__(self, number_of_patches: int, embed_dim: int):
        """
        Initialize the PositionalEncoding module.

        Args:
            number_of_patches: Number of patches in the input sequence
            embed_dim: Dimensionality of the embedding space
        """
        super().__init__()
        self.pos_embed = nn.Parameter(torch.rand(number_of_patches, embed_dim))

    def forward(self, x):
        return x + self.pos_embed


class PatchEmbedding(nn.Module):
    """
    Convert 2D spectrogram patches into embeddings.

    This module extracts patches from a 2D spectrogram (frequency, time) and
    converts them into embedding vectors that can be processed by the transformer.
    The process involves convolutional feature extraction followed by linear
    transformation to the desired embedding dimension.

    Parameters
    ----------
    num_channels : int
        Number of input channels (e.g., 1 for mono audio)
    patch_size_time : int
        Size of patches in the time dimension
    patch_size_freq : int
        Size of patches in the frequency dimension
    embed_dim : int
        Dimensionality of the output embedding space
    """

    def __init__(
        self,
        num_channels: int,
        patch_size_time: int,
        patch_size_freq: int,
        embed_dim: int,
    ):
        """
        Initialize the PatchEmbedding module.

        Args:
            num_channels: Number of input channels (e.g., 1 for mono audio)
            patch_size_time: Size of patches in the time dimension
            patch_size_freq: Size of patches in the frequency dimension
            embed_dim: Dimensionality of the output embedding space
        """
        super().__init__()
        inter_channels = 2 * embed_dim
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels=num_channels,
                out_channels=inter_channels,
                kernel_size=(patch_size_freq, patch_size_time),
                stride=(patch_size_freq, patch_size_time),
            ),
            nn.LeakyReLU(0.1),
            nn.BatchNorm2d(inter_channels),
        )
        self.lin = nn.Sequential(
            nn.Linear(inter_channels, inter_channels),
            nn.LeakyReLU(),
            nn.Linear(inter_channels, embed_dim),
            nn.LeakyReLU(),
        )

    def forward(self, x: torch.Tensor):
        # x shape: (B, C, F, T)
        # f := F//patch_size_freq, t := T//patch_size_time
        x = self.conv(x)  # (B, inter_channels, f, t)
        x = x.transpose(-1, -2)  # (B, inter_channels, t, f)
        x = x.flatten(-2)  # (B, inter_channels, t * f)
        x = x.transpose(-1, -2)  # (B, t * f, inter_channels)
        x = self.lin(x)  # (B, t * f, embed_dim)
        # embedding sequence corresponds to [(t_1, f_1), (t_1, f_2), ..., (t_1, f_N), (t_2, f_1), ...]
        return x


class PatchDecoder(nn.Module):
    """
    Decode embedded patches back into a spectrogram.

    This module reverses the patch embedding process by transforming embedded
    patch representations back into the original spectrogram format. It uses
    linear layers followed by convolutional operations to reconstruct the
    frequency-time representation from the embedding space.

    Parameters
    ----------
    num_channels : int
        Number of output channels in the reconstructed spectrogram
    patch_num_freq : int
        Number of patches in the frequency dimension
    patch_num_time : int
        Number of patches in the time dimension
    embed_dim : int
        Dimensionality of the input embedding space
    patch_size_time : int
        Size of patches in the time dimension
    patch_size_freq : int
        Size of patches in the frequency dimension
    """

    def __init__(
        self,
        num_channels: int,
        patch_num_freq: int,
        patch_num_time: int,
        embed_dim: int,
        patch_size_time: int,
        patch_size_freq: int,
    ):
        """
        Initialize the PatchDecoder module.

        Args:
            num_channels: Number of output channels in the reconstructed spectrogram
            patch_num_freq: Number of patches in the frequency dimension
            patch_num_time: Number of patches in the time dimension
            embed_dim: Dimensionality of the input embedding space
            patch_size_time: Size of patches in the time dimension
            patch_size_freq: Size of patches in the frequency dimension
        """
        super().__init__()
        self.num_channels = num_channels
        self.patch_size_time = patch_size_time
        self.patch_size_freq = patch_size_freq
        self.patch_num_freq = patch_num_freq
        self.patch_num_time = patch_num_time

        self.lin1 = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.LeakyReLU(),
            nn.Linear(embed_dim, embed_dim),
            nn.LeakyReLU(),
        )

        inter_channels = max(
            embed_dim, num_channels * patch_size_time * patch_size_freq // 2
        )
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels=embed_dim,
                out_channels=inter_channels,
                kernel_size=1,
                padding=0,
                stride=1,
            ),
            nn.LeakyReLU(),
            nn.Conv2d(
                in_channels=inter_channels,
                out_channels=num_channels * patch_size_time * patch_size_freq,
                kernel_size=1,
                padding=0,
                stride=1,
            ),
        )

    def forward(self, x: torch.Tensor):
        # x shape: (B, number_of_patches, embed_dim)
        x = self.lin1(x)  # (B, number_of_patches, embed_dim)
        x = x.transpose(-1, -2)  # (B, embed_dim, number_of_patches)
        x = x.reshape(
            *x.shape[:-1], self.patch_num_time, self.patch_num_freq
        )  # (B, embed_dim, t, f)
        x = x.transpose(-1, -2)  # (B, embed_dim, f, t)

        x = self.conv(x)  # (B, C * patch_num_time * patch_num_freq, f, t)

        x = x.reshape(
            *x.shape[:-3],
            self.num_channels,
            self.patch_size_freq,
            self.patch_size_time,
            self.patch_num_freq,
            self.patch_num_time,
        )  # (B, C, patch_size_freq, patch_size_time, f, t)

        _axes = range(len(x.shape[:-4]))
        x = x.permute(
            *_axes, -2, -4, -1, -3
        )  # (B, C, f, patch_size_freq, t, patch_size_time)

        x = x.reshape(
            *x.shape[:-4],
            self.patch_size_freq * self.patch_num_freq,
            self.patch_size_time * self.patch_num_time,
        )  # (B, C, F, T)
        return x


class MAEModel(L.LightningModule):
    """
    Masked Autoencoder for Spectrogram Reconstruction.

    This model implements a masked autoencoder architecture for reconstructing
    spectrograms from audio signals. It uses a transformer-based encoder-decoder
    structure with patch-based processing of spectrogram inputs.

    As an input, it takes tensor of shape `(B, C, T)`, where `B` is batch size, `C` is number of channels, and `T` is time frames.
    And return two tensors:

        batch = ...  # (B, C, t)
        x = model.transform_batch(batch)  # (B, C, F, T)
        mask_indices = model.generate_mask_indices()
        x, y = model(x, mask_indices)  # (B, C, [F], [T]), (B, C, [F], [T])
        mask = model.generate_mask(mask_indices)  # ([F], [T])
        loss_on_hidden_patches = model.loss_fn(x[..., mask], y[..., mask])
        loss_on_all_patches = model.loss_fn(x, y)

    where `[x]` in shape means truncated shape to match number of patches, their length and shape of original tensor:

        [F] = model.patch_num_freq * model.patch_size_freq
        [T] = model.patch_num_time * model.patch_size_time

    """

    def __init__(
        self,
        frame_length: int,
        channels: list[int],
        patch_size_time: int,
        patch_size_freq: int,
        embed_dim: int,
        encoder_nhead: int,
        encoder_dim_feedforward: int,
        encoder_num_layers: int,
        decoder_nhead: int,
        decoder_dim_feedforward: int,
        decoder_num_layers: int,
        mask_ratio=0.75,
        mask_strategy: Literal["unstructured", "time", "freq"] = "unstructured",
        transform_n_fft: int = 512,
        transform_hop_length: int = 64,
        transform_power: float = 2.0,
    ):
        """
        Initialize the MAE model for spectrogram reconstruction.

        Parameters
        ----------
        frame_length : int
            Length of the audio frame in samples
        channels : list[int]
            List of channel indices to use from the input
        patch_size_time : int
            Size of patches in the time dimension
        patch_size_freq : int
            Size of patches in the frequency dimension
        embed_dim : int
            Dimensionality of the embedding space
        encoder_nhead : int
            Number of attention heads in the encoder
        encoder_dim_feedforward : int
            Dimensionality of the feedforward network in the encoder
        encoder_num_layers : int
            Number of encoder layers
        decoder_nhead : int
            Number of attention heads in the decoder
        decoder_dim_feedforward : int
            Dimensionality of the feedforward network in the decoder
        decoder_num_layers : int
            Number of decoder layers
        mask_ratio : float, default=0.75
            Ratio of patches to mask during training
        mask_strategy : Literal["unstructured", "time", "freq"], default="unstructured"
            Strategy for masking patches ('unstructured', 'time', or 'freq')
        transform_n_fft : int, default=512
            Size of FFT for spectrogram computation
        transform_hop_length : int, default=64
            Hop length for spectrogram computation
        transform_power : float, default=2.0
            Exponent for power spectrogram (1 for magnitude, 2 for power)
        """
        super().__init__()
        self.channels = channels
        self.patch_size_time = patch_size_time
        self.patch_size_freq = patch_size_freq
        self.embed_dim = embed_dim
        self.mask_ratio = mask_ratio
        self.mask_strategy = mask_strategy

        # Calculate number of frequency bins and time windows from audio parameters
        freq_bins_num = transform_n_fft // 2 + 1
        windows_num = (frame_length - transform_n_fft) // transform_hop_length + 1

        # Calculate number of patches in each dimension
        self.patch_num_freq = freq_bins_num // patch_size_freq
        self.patch_num_time = windows_num // patch_size_time
        self.number_of_patches = self.patch_num_freq * self.patch_num_time

        # Initialize patch embedding module
        self.patch_embed = PatchEmbedding(
            num_channels=len(channels),
            patch_size_time=patch_size_time,
            patch_size_freq=patch_size_freq,
            embed_dim=embed_dim,
        )

        # Initialize spectrogram transform
        self.transform = torchaudio.transforms.Spectrogram(
            n_fft=transform_n_fft,
            win_length=transform_n_fft,
            hop_length=transform_hop_length,
            power=transform_power,
            center=False,
        )

        # Initialize positional encodings for encoder and decoder
        self.positional_encoding1 = PositionalEncoding(
            number_of_patches=self.number_of_patches,
            embed_dim=self.embed_dim,
        )

        self.positional_encoding2 = PositionalEncoding(
            number_of_patches=self.number_of_patches,
            embed_dim=self.embed_dim,
        )

        # Initialize transformer encoder
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=encoder_nhead,
                dim_feedforward=encoder_dim_feedforward,
                batch_first=True,
            ),
            num_layers=encoder_num_layers,
        )

        # Learnable mask token for masked patches
        self.mask_token = torch.nn.Parameter(torch.rand(embed_dim))

        # Initialize transformer decoder
        self.decoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=decoder_nhead,
                dim_feedforward=decoder_dim_feedforward,
                batch_first=True,
            ),
            num_layers=decoder_num_layers,
        )

        # Initialize patch decoder module
        self.patch_de_embed = PatchDecoder(
            num_channels=len(channels),
            patch_num_freq=self.patch_num_freq,
            patch_num_time=self.patch_num_time,
            embed_dim=self.embed_dim,
            patch_size_freq=self.patch_size_freq,
            patch_size_time=self.patch_size_time,
        )

        # Loss function for reconstruction
        self.loss_fn = nn.MSELoss()

        # Save hyperparameters for logging and checkpointing
        self.save_hyperparameters()

    def generate_mask_indices(self) -> torch.Tensor:
        """
        Generate indices of patches to be masked based on the selected strategy.

        This method implements three masking strategies:

        - 'unstructured': randomly selects individual patches to mask
        - 'time': masks entire time steps (columns of patches)
        - 'freq': masks entire frequency bands (rows of patches)

        Returns
        -------
        torch.Tensor
            A tensor containing the indices of patches to be masked

        Raises
        ------
        ValueError
            If an unknown mask strategy is specified
        """
        if self.mask_strategy == "unstructured":
            # Randomly select individual patches to mask
            num_mask = int(self.number_of_patches * self.mask_ratio)
            rand_indices = torch.randperm(self.number_of_patches)
            mask_indices = rand_indices[:num_mask]

        elif self.mask_strategy == "time":
            # Mask entire time steps (columns of patches)
            num_mask = int(self.patch_num_time * self.mask_ratio)
            # Create a 2D grid of patch indices
            all_indices = torch.arange(self.number_of_patches).reshape(
                self.patch_num_time, self.patch_num_freq
            )
            # Randomly select which time steps to mask
            rand_indices = torch.randperm(self.patch_num_time)
            # Get indices of all patches in the selected time steps
            mask_indices = all_indices[rand_indices[:num_mask]].flatten()

        elif self.mask_strategy == "freq":
            # Mask entire frequency bands (rows of patches)
            num_mask = int(self.patch_num_freq * self.mask_ratio)
            # Create a 2D grid of patch indices
            all_indices = torch.arange(self.number_of_patches).reshape(
                self.patch_num_time, self.patch_num_freq
            )
            # Randomly select which frequency bands to mask
            rand_indices = torch.randperm(self.patch_num_freq)
            # Get indices of all patches in the selected frequency bands
            mask_indices = all_indices[:, rand_indices[:num_mask]].flatten()

        else:
            raise ValueError("Unknown mask strategy")

        return mask_indices

    def generate_mask(self, mask_indices: torch.Tensor):
        """
        Generate a boolean mask from patch indices.

        This method creates a boolean mask tensor from the given patch indices,
        which can be used to index into spectrogram tensors to select masked regions.

        Should be used with `generate_mask_indices`:

            mask_indices = model.generate_mask_indices()
            x, y = model(x, mask_indices)
            mask = model.generate_mask(mask_indices)
            x[..., mask]

        Parameters
        ----------
        mask_indices : torch.Tensor
            Indices of patches to be masked

        Returns
        -------
        torch.Tensor
            Boolean mask tensor of shape (F, T) where F and T are the number of
            frequency bins and time frames respectively
        """
        mask = torch.zeros((self.number_of_patches), dtype=torch.bool)
        mask[mask_indices] = True
        mask = mask.reshape(self.patch_num_time, self.patch_num_freq)
        mask = mask.transpose(-1, -2)
        mask = mask.repeat_interleave(repeats=self.patch_size_time, dim=1)
        mask = mask.repeat_interleave(repeats=self.patch_size_freq, dim=0)
        return mask

    def forward(  # type: ignore[bad-override]
        self, x: torch.Tensor, mask_indices: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass of the MAE model.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape (B, C, F, T) where B is batch size, C is number of channels,
            F is number of frequency bins, and T is number of time frames
        mask_indices : torch.Tensor
            Indices of patches to be masked (not used in this implementation as
            mask indices are generated internally)

        Returns
        -------
        tuple[torch.Tensor, torch.Tensor]
            A tuple containing (original_spectrogram, reconstructed_spectrogram) where both tensors
            have shape (B, C, F, T) after cropping to the valid dimensions
        """
        # --- Patch embedding ---
        patches = self.patch_embed(x)  # (B, number_of_patches, embed_dim)
        *_, number_of_patches, embed_dim = patches.shape
        assert embed_dim == self.embed_dim
        assert number_of_patches == self.number_of_patches

        # --- Positional encoding ---
        patches = self.positional_encoding1(patches)

        # --- Masking ---
        # Generate mask indices based on the configured strategy
        mask_indices = self.generate_mask_indices()
        # Create a boolean mask for the patches
        mask_slice = torch.zeros(number_of_patches, dtype=torch.bool)
        mask_slice[mask_indices] = True

        # ---- Encode visible patches ----
        # Extract only the visible (unmasked) patches
        patches_visible = patches[..., ~mask_slice, :]
        # Encode the visible patches using the transformer encoder
        encoded = self.encoder(patches_visible)

        # ---- Add mask tokens ----
        # Create a tensor to hold the encoded patches and mask tokens
        encoded_with_mask_tokens = torch.empty_like(patches)
        # Place the encoded visible patches in their original positions
        encoded_with_mask_tokens[..., ~mask_slice, :] = encoded
        # Fill the masked positions with the learnable mask token
        encoded_with_mask_tokens[..., mask_slice, :] = self.mask_token

        # ---- Decode to reconstruct all patches ----
        # Add positional encoding to the combined representation
        encoded_with_mask_tokens = self.positional_encoding2(encoded_with_mask_tokens)
        # Decode the combined representation to reconstruct all patches
        decoded = self.decoder(
            encoded_with_mask_tokens
        )  # (B, number_of_patches, embed_dim)
        # Convert the decoded embeddings back to spectrogram format
        y = self.patch_de_embed(decoded)  # (B, C, F, T)

        # Crop the output to match the valid dimensions after spectrogram transformation
        freq_bin_size = self.patch_num_freq * self.patch_size_freq
        windows_size = self.patch_num_time * self.patch_size_time

        return x[..., :freq_bin_size, :windows_size], y

    def transform_batch(self, batch):
        """
        Transform a batch of audio data into log-scaled spectrograms.

        This method extracts the specified channels from the input batch,
        computes the spectrogram using the configured transform, and applies
        a log scaling to compress the dynamic range.

        Example
        -------

            x = model.transform_batch(batch)  # x ~ log(1e-15 + STFT(batch, channels=model.channels))

        Parameters
        ----------
        batch : torch.Tensor
            Input tensor of shape (B, C, frame_length) where B is batch size,
            C is number of channels, and frame_length is the length of the audio frame

        Returns
        -------
        torch.Tensor
            Log-scaled spectrogram tensor of shape (B, C, F, T) where F is number of frequency bins
            and T is number of time frames
        """
        batch = batch[..., self.channels, :]  # (B, C, frame_length)
        batch = self.transform(batch)  # (B, C, F, T)
        batch = torch.log(batch + 1e-15)
        return batch

    def training_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x = self.transform_batch(batch)
        mask_indices = self.generate_mask_indices()
        x, y = self(x, mask_indices)
        mask = self.generate_mask(mask_indices)
        loss_on_hidden_patches = self.loss_fn(x[..., mask], y[..., mask])
        loss_on_all_patches = self.loss_fn(x, y)

        self.log(
            "train_loss",
            loss_on_hidden_patches,
            on_step=True,
            on_epoch=True,
            prog_bar=True,
            logger=True,
        )
        self.log(
            "train_full_loss",
            loss_on_all_patches,
            on_epoch=True,
            logger=True,
        )

        return loss_on_hidden_patches

    def validation_step(self, batch, batch_idx):  # type: ignore[bad-override]
        x = self.transform_batch(batch)
        mask_indices = self.generate_mask_indices()
        x, y = self(x, mask_indices)
        mask = self.generate_mask(mask_indices)
        loss_on_hidden_patches = self.loss_fn(x[..., mask], y[..., mask])
        loss_on_all_patches = self.loss_fn(x, y)

        self.log(
            "val_loss",
            loss_on_hidden_patches,
            on_epoch=True,
            prog_bar=True,
            logger=True,
        )
        self.log(
            "val_full_loss",
            loss_on_all_patches,
            on_epoch=True,
            logger=True,
        )

        return loss_on_hidden_patches


if __name__ == "__main__":
    run_cli(__file__, run=True)
