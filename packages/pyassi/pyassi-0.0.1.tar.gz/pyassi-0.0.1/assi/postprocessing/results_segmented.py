from jsonargparse.typing import import_object  # type: ignore
import pandas as pd
import torch
from torch.utils.data import DataLoader
import lightning as L

from assi.modelstorage import ModelStorage
from assi.datasets.dataset_segmented import SegmentedDataModule


def calculate_results_over_the_whole_dataset(
    data_type: str,
    model_type: str,
    model_storage: ModelStorage,
    metadata_query: str | None = None,
    score_column: str = "score",
    batch_size: int = 1000,
) -> pd.DataFrame:
    """Generate results table based on datatable for the model over the whole segmented dataset

    Parameters
    ----------
    data_type : str
        Data module type
    model_type : str
        Model type
    model_storage : ModelStorage
        Model storage containing the checkpoint
    metadata_query : str | None, optional
        Query to filter metadata, by default None
    score_column : str, optional
        Column name for the score in the results table, by default "score"

    Returns
    -------
    pd.DataFrame
        Results table with scores
    """
    DataModule: SegmentedDataModule = import_object(data_type)
    Model: L.LightningModule = import_object(model_type)

    ckpt = model_storage.checkpoint_path
    model = Model.load_from_checkpoint(ckpt)
    datamodule = DataModule.load_from_checkpoint(ckpt)

    # Create datatable for the whole dataset
    datamodule.datatable_preserved_columns = True
    datamodule.metadata_query = metadata_query
    datamodule.use_cache = False
    datatable = datamodule.generate_datatable()
    dataset = datamodule.generate_dataset(datatable=datatable)

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
    )
    trainer = L.Trainer(logger=False, enable_checkpointing=False)
    pred_batches = trainer.predict(model, dataloaders=dataloader)
    scores = torch.cat(pred_batches)  # type: ignore[no-matching-overload]

    results_table = dataset.datatable.copy()
    results_table[score_column] = scores.numpy()
    results_table = results_table.drop(columns="file_path")

    return results_table
