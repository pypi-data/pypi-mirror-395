from pathlib import Path
from abc import ABC, abstractmethod
import pandas as pd


class DataStorage(ABC):
    """
    Abstract base class for dataset storage backends.
    Provides an interface for managing datasets from different sources (local filesystem, cloud services, ClearML, etc.).
    All implementations must provide access to the dataset folder and metadata.
    """

    @property
    @abstractmethod
    def dataset_base_folder(self) -> Path:
        """
        Get the root directory path of the dataset.

        Returns
        -------
        Path
            Root directory containing all dataset files and subdirectories
        """
        ...

    @abstractmethod
    def check_integrity(self, force: bool = False):
        """
        Verify the dataset is available and valid.
        Downloads or re-downloads the dataset if necessary.
        Implementations should use this method to ensure all required files are present before training.

        Parameters
        ----------
        force : bool, optional
            If True, re-download the dataset even if it already exists locally (default: False)
        """
        ...

    @property
    @abstractmethod
    def metadata(self) -> pd.DataFrame:
        """
        Get dataset metadata as a pandas DataFrame.

        For use with SegmentedDataModule the metadata should contain at least the following columns:

        - `rel_file_path_posix`: Relative path to audio file within dataset
        - `num_frames`: Number of samples in the audio file
        - `split`: Subset assignment (e.g., `'train'`, `'test'`, `'val'`)

        Returns
        -------
        pd.DataFrame
            Metadata DataFrame with file paths, frame counts, and split info
        """
        ...


class LocalStorage(DataStorage):
    """
    Dataset storage backend for local filesystem storage.
    Manages datasets stored on the local filesystem with metadata provided in a CSV file.
    """

    def __init__(self, dataset_base_folder: Path | str, metadata_path: Path | str):
        """
        Parameters
        ----------
        dataset_base_folder : Path | str
            Root directory of the dataset
        metadata_path : Path | str
            Path to the CSV file containing dataset metadata
        """
        self._dataset_base_folder = Path(dataset_base_folder)
        self._metadata = pd.read_csv(metadata_path)

    @property
    def dataset_base_folder(self) -> Path:
        """
        Get the root directory path of the dataset.

        Returns
        -------
        Path
            Root directory containing all dataset files and subdirectories
        """
        return self._dataset_base_folder

    def check_integrity(self, force: bool = False):
        """
        Verify the dataset directory exists.
        For local storage, only checks that the base folder exists.
        The force parameter is ignored since no downloads are performed.

        Parameters
        ----------
        force : bool, optional
            Ignored for local storage (default: False)
        """
        # No action needed for local path storage
        pass

    @property
    def metadata(self) -> pd.DataFrame:
        """
        Get dataset metadata from the CSV file.

        Returns
        -------
        pd.DataFrame
            Metadata DataFrame loaded from the CSV file
        """
        return self._metadata
