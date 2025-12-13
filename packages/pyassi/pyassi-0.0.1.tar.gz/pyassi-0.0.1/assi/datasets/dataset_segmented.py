import lightning as L
import torchaudio
import psutil
import torch
import pandas as pd
from assi.datastorage import DataStorage
from pathlib import Path, PurePosixPath


class SegmentedDataset(torch.utils.data.Dataset):
    """Dataset for audio data segmented into frames"""

    def __init__(
        self,
        datatable: pd.DataFrame,
        frame_length: int,
        use_cache: bool = False,
    ):
        """Constructor

        Parameters
        ----------
        datatable : pd.DataFrame
            Data table containing file paths and frame offsets for segments
        frame_length : int
            Length of each audio segment in samples
        use_cache : bool, optional
            Whether to cache audio files in memory, by default False

        Raises
        ------
        MemoryError
            If caching is enabled but there is not enough available memory
        """
        super().__init__()

        assert "file_path" in datatable.columns
        assert "frame_offset" in datatable.columns
        self.datatable = datatable

        self.frame_length = frame_length

        self.use_cache = use_cache
        self._cache = {}

        if not self.use_cache:
            return

        # calculate bytes required for cache
        cache_bytes_required = 0
        for file_path in self.datatable["file_path"].unique():
            info = torchaudio.info(file_path)
            cache_bytes_required += (
                info.num_frames * info.num_channels * 4
            )  # frames * channels * 4 bytes (float32)

        # log required and available bytes
        bytes_available = psutil.virtual_memory().available
        if cache_bytes_required > bytes_available and self.use_cache:
            raise MemoryError(
                f"Cache requires {cache_bytes_required / 1e9:.2f} GB, but only {bytes_available / 1e9:.2f} GB available"
            )
        else:
            print(
                f"Estimated cache size: {cache_bytes_required / 1e9:.2f} GB, available: {bytes_available / 1e9:.2f} GB"
            )

        # load files in to the cache
        for file_path in self.datatable["file_path"].unique():
            raw_signal, _ = torchaudio.load(uri=file_path)
            raw_signal.share_memory_()
            self._cache[file_path] = raw_signal

    def __len__(self) -> int:
        return len(self.datatable)

    def __getitem__(self, index) -> torch.Tensor:
        item = self.datatable.iloc[index]
        file_path = item["file_path"]

        if self.use_cache and file_path in self._cache:
            raw_signal = self._cache[file_path]

            signal = raw_signal[
                ...,
                item["frame_offset"] : item["frame_offset"] + self.frame_length,
            ]
        else:
            signal, sr = torchaudio.load(
                uri=file_path,
                frame_offset=item["frame_offset"],
                num_frames=self.frame_length,
            )

        return signal


def _splitted_datatable_generator(
    dataset_base_folder: Path,
    metadata: pd.DataFrame,
    frame_length: int,
    frame_hop: int,
    preserved_columns: bool | list[str] = False,
):
    """Yield sliding-window frame segments for each entry in a metadata table.

    Parameters
    ----------
    dataset_base_folder : Path
        Base folder for resolving audio file paths.
    metadata : pd.DataFrame
        Table describing audio files; must contain ``rel_file_path_posix`` and ``num_frames``.
    frame_length : int
        Length of each frame segment.
    frame_hop : int
        Hop size between segments.
    preserved_columns : bool or list[str], optional
        Metadata fields to include in each yielded row:
        - True: include all columns
        - False: include none
        - list[str]: include selected columns

    Yields
    ------
    dict
        A row containing selected metadata, full file path, and ``frame_offset``.

    """

    for _, row in metadata.iterrows():
        frame_offset = 0

        while frame_offset + frame_length <= row["num_frames"]:
            if preserved_columns is True:
                new_row = row.to_dict()
            else:
                if preserved_columns is False:
                    new_row = {}
                elif isinstance(preserved_columns, list):
                    new_row = {column: row[column] for column in preserved_columns}
                else:
                    raise ValueError

            new_row["file_path"] = str(
                dataset_base_folder
                / Path(PurePosixPath(str(row["rel_file_path_posix"])))
            )

            new_row["frame_offset"] = frame_offset

            yield new_row
            frame_offset += frame_hop


def splitted_datatable(
    dataset_base_folder: Path,
    metadata: pd.DataFrame,
    frame_length: int,
    frame_hop: int,
    preserved_columns: bool | list[str] = False,
) -> pd.DataFrame:
    """Create a datatable with sliding-window frame segments for each entry in a metadata table."""
    return pd.DataFrame(
        _splitted_datatable_generator(
            dataset_base_folder=dataset_base_folder,
            metadata=metadata,
            frame_length=frame_length,
            frame_hop=frame_hop,
            preserved_columns=preserved_columns,
        )
    )


class SegmentedDataModule(L.LightningDataModule):
    """DataModule for segmented audio data"""

    def __init__(
        self,
        storage: DataStorage,
        frame_length: int,
        frame_hop: int,
        batch_size: int,
        metadata_query: str | None = None,
        datatable_query: str | None = None,
        datatable_preserved_columns: bool | list[str] = False,
        num_workers: int = 0,
        force_download: bool = False,
        use_cache: bool = False,
    ) -> None:
        """Constructor

        Parameters
        ----------
        storage : DataStorage
            Storage containing the dataset audio files and metadata
        frame_length : int
            Length of each frame segment
        frame_hop : int
            Hop size between segments
        batch_size : int
            Batch size for data loaders
        metadata_query : str | None, optional
            Query to filter metadata, by default None
        datatable_query : str | None, optional
            Query to filter datatable, by default None
        datatable_preserved_columns : bool | list[str], optional
            Columns to preserve in the datatable, by default False
        num_workers : int, optional
            Number of workers for data loaders, by default 0
        force_download : bool, optional
            Whether to force re-download of dataset files, by default False
        use_cache : bool, optional
            Whether to cache audio files in memory, by default False
        """
        super().__init__()

        self.frame_length = frame_length
        self.frame_hop = frame_hop
        self.batch_size = batch_size
        self.metadata_query = metadata_query
        self.datatable_query = datatable_query
        self.datatable_preserved_columns = datatable_preserved_columns

        self.num_workers = num_workers
        self.force_download = force_download

        self.storage = storage

        self.save_hyperparameters()

        self.use_cache = use_cache

    def prepare_data(self) -> None:
        self.storage.check_integrity(force=self.force_download)

    def generate_datatable(self):
        metadata = self.storage.metadata

        if self.metadata_query is None:
            selected_metadata = metadata
        else:
            selected_metadata = metadata.query(self.metadata_query)

        datatable = splitted_datatable(
            dataset_base_folder=self.storage.dataset_base_folder,
            metadata=selected_metadata,
            frame_length=self.frame_length,
            frame_hop=self.frame_hop,
            preserved_columns=self.datatable_preserved_columns,
        )

        if self.datatable_query is None:
            selected_datatable = datatable
        else:
            selected_datatable = datatable.query(self.datatable_query)

        return selected_datatable

    def generate_dataset(self, datatable: pd.DataFrame) -> SegmentedDataset:
        return SegmentedDataset(
            datatable=datatable,
            frame_length=self.frame_length,
            use_cache=self.use_cache,
        )

    def setup(self, stage: str):
        if stage == "fit":
            datatable = self.generate_datatable()
            dataset = self.generate_dataset(datatable=datatable)
            self.train_dataset, self.val_dataset = torch.utils.data.random_split(
                dataset=dataset,
                lengths=[0.8, 0.2],
            )

        elif stage == "test":
            raise NotImplementedError
        elif stage == "predict":
            raise NotImplementedError
        else:
            raise NotImplementedError

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            persistent_workers=True,
            shuffle=True,
            pin_memory=True,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            persistent_workers=True,
            pin_memory=True,
        )
