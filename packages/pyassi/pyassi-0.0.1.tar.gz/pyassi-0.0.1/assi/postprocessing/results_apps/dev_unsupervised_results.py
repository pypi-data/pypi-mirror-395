import os
import pandas as pd
from pathlib import Path

from assi.postprocessing.results_apps.unsupervised_results import create_app
from assi.datastorage import LocalStorage

development = os.getenv("ENVIRONMENT", "production").lower() == "development"

results_table = pd.read_csv(
    Path(__file__).absolute().parent.parent.parent.parent
    / "drafts"
    / "results_table.csv"
)
ds_path = Path(__file__).absolute().parent.parent.parent.parent / ".cache" / "generated"

app = create_app(
    results_table=results_table,
    data_storage=LocalStorage(ds_path, ds_path / "metadata.csv"),
    groupby=["split"],
    development=development,
)
