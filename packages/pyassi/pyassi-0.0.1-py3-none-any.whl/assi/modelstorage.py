from pathlib import Path
from abc import ABC, abstractmethod


class ModelStorage(ABC):
    """
    Abstract base class for model storage backends.
    Provides an interface for managing model checkpoints from different sources (local filesystem, remote servers, etc.).
    """

    @property
    @abstractmethod
    def checkpoint_path(self) -> Path:
        """
        Get the path to the model checkpoint.

        Returns
        -------
        Path
            Path to the checkpoint file
        """
        ...

    @abstractmethod
    def check_integrity(self, force: bool = False):
        """
        Verify the model checkpoint is available and valid.
        Downloads or re-downloads the checkpoint if necessary.

        Parameters
        ----------
        force : bool, optional
            If True, re-download the model even if it already exists
        """
        ...


class LocalModelStorage(ModelStorage):
    """
    Model storage for local filesystem storage.
    Manages model checkpoints stored on the local filesystem.
    """

    def __init__(self, checkpoint_path: Path | str):
        """
        Parameters
        ----------
        checkpoint_path : Path | str
            Path to the model checkpoint file
        """
        self._checkpoint_path = Path(checkpoint_path)

    @property
    def checkpoint_path(self) -> Path:
        """
        Get the path to the model checkpoint.

        Returns
        -------
        Path
            Path to the checkpoint file
        """
        return self._checkpoint_path

    def check_integrity(self, force: bool = False):
        """
        Verify the checkpoint exists at the specified path.

        Parameters
        ----------
        force : bool, optional
            Ignored for local storage (does not re-download)

        Raises
        ------
        FileNotFoundError
            If the checkpoint file does not exist at the specified path
        """
        if not self._checkpoint_path.exists():
            raise FileNotFoundError(
                f"Checkpoint path {self._checkpoint_path} does not exist."
            )
