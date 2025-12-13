from assi.modelstorage import ModelStorage
import clearml
from pathlib import Path


class ClearMLModelStorage(ModelStorage):
    """
    Model storage backend for ClearML-managed models.
    Manages model checkpoints stored in ClearML's model registry and downloads them to the local filesystem as needed.
    """

    def __init__(self, model_id: str):
        """
        Parameters
        ----------
        model_id : str
            The ClearML model ID for the checkpoint to load
        """
        self.model = clearml.Model(model_id=model_id)

    @property
    def checkpoint_path(self) -> Path:
        """
        Get the local path to the model checkpoint.
        Downloads the checkpoint from ClearML if not already cached locally.

        Returns
        -------
        Path
            Path to the local checkpoint file
        """
        return Path(self.model.get_local_copy())

    def check_integrity(self, force: bool = False):
        """
        Verify the checkpoint is available locally.
        Downloads or re-downloads the checkpoint from ClearML if necessary.

        Parameters
        ----------
        force : bool, optional
            If True, force re-download the model from ClearML even if it already exists locally
        """
        self.model.get_local_copy(force_download=force)
