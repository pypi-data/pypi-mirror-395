from assi.datastorage import DataStorage
import pandas as pd
import clearml
from pathlib import Path


class ClearMLDataStorage(DataStorage):
    """
    Dataset storage backend for ClearML-managed datasets.
    Manages datasets stored in ClearML's dataset registry and downloads them to the local filesystem as needed.
    """

    def __init__(self, dataset_id: str, alias: str = "main"):
        """
        Parameters
        ----------
        dataset_id : str
            The ClearML dataset ID
        alias : str, optional
            Alias of the dataset.
        """
        self.dataset = clearml.Dataset.get(dataset_id=dataset_id, alias=alias)

    @property
    def dataset_base_folder(self) -> Path:
        """
        Get the local path to the dataset folder.
        Downloads the dataset from ClearML if not already cached locally.

        Returns
        -------
        Path
            Path to the local dataset directory
        """
        return Path(self.dataset.get_local_copy())

    @property
    def metadata(self) -> pd.DataFrame:
        """
        Get dataset metadata from ClearML.

        Returns
        -------
        pd.DataFrame
            Metadata DataFrame stored in the ClearML dataset

        Raises
        ------
        ValueError
            If the metadata is not a pandas DataFrame
        """
        metadata = self.dataset.get_metadata()

        if isinstance(metadata, pd.DataFrame):
            return metadata

        raise ValueError(
            f"Metadata must be a pandas DataFrame, but {type(metadata)} is found"
        )

    def check_integrity(self, force: bool = False):
        """
        Verify the dataset is available locally.
        Downloads or re-downloads the dataset from ClearML if necessary.

        Parameters
        ----------
        force : bool, optional
            Ignored for ClearMLDataStorage
        """
        self.dataset.get_local_copy()
