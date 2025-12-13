import pandas as pd
from pathlib import Path
import urllib.request
import zipfile
import re
import numpy as np

from assi.datastorage import DataStorage

FRAMES_PER_SIGNAL = 160_000
SR = 16_000

DATASET_PARTS_ZIP_URLS = {
    "-6_dB_fan": "https://zenodo.org/records/3384388/files/-6_dB_fan.zip",
    "-6_dB_pump": "https://zenodo.org/records/3384388/files/-6_dB_pump.zip",
    "-6_dB_slider": "https://zenodo.org/records/3384388/files/-6_dB_slider.zip",
    "-6_dB_valve": "https://zenodo.org/records/3384388/files/-6_dB_valve.zip",
    "0_dB_fan": "https://zenodo.org/records/3384388/files/0_dB_fan.zip",
    "0_dB_pump": "https://zenodo.org/records/3384388/files/0_dB_pump.zip",
    "0_dB_slider": "https://zenodo.org/records/3384388/files/0_dB_slider.zip",
    "0_dB_valve": "https://zenodo.org/records/3384388/files/0_dB_valve.zip",
    "6_dB_fan": "https://zenodo.org/records/3384388/files/6_dB_fan.zip",
    "6_dB_pump": "https://zenodo.org/records/3384388/files/6_dB_pump.zip",
    "6_dB_slider": "https://zenodo.org/records/3384388/files/6_dB_slider.zip",
    "6_dB_valve": "https://zenodo.org/records/3384388/files/6_dB_valve.zip",
}


def download(zip_url: str, zip_path: Path):
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
        print(f"\rDownloading {zip_url} {percent}%", end="", flush=True)

    urllib.request.urlretrieve(zip_url, zip_path, reporthook=show_progress)


def extract(zip_path: Path, dataset_base_folder: Path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dataset_base_folder)


def process_part(force, dataset_base_folder: Path, part_name: str):
    dir_path = dataset_base_folder / f"{part_name}"
    zip_path = dataset_base_folder / f"{part_name}.zip"

    zip_url = DATASET_PARTS_ZIP_URLS[part_name]

    # === downloading ===
    if force or not dir_path.exists() or not dir_path.is_dir():
        dir_path.mkdir(parents=True, exist_ok=True)
        if not zip_path.exists():
            download(zip_url, zip_path)

        try:
            print()
            extract(zip_path, dir_path)
        except zipfile.BadZipFile:
            zip_path.unlink()
            download(zip_url, zip_path)
            print()
            extract(zip_path, dir_path)
        finally:
            zip_path.unlink()

    # === metadata generation ===

    # structure of the files:
    #  <dir_path>
    #      <machine_type>
    #          id_<machine_id>
    #              abnormal
    #                  000001.wav
    #                  000002.wav
    #                  ....
    #              normal
    #                  000001.wav
    #                  000002.wav
    #                  ....
    #          id_<machine_id>
    #              ....
    #
    snr, _, machine_type = part_name.split("_")
    snr = int(snr)

    def record_generator():
        for folder in (dir_path / machine_type).iterdir():
            if not folder.is_dir():
                continue
            if not re.match(r"^id_\d\d$", folder.name):
                continue
            machine_id = int(folder.name.removeprefix("id_"))

            for subfolder in folder.iterdir():
                if not subfolder.is_dir():
                    continue
                anomaly_type = subfolder.name

                for file in subfolder.iterdir():
                    if not file.suffix == ".wav":
                        continue

                    yield {
                        "machine_type": machine_type,
                        "anomaly_type": anomaly_type,
                        "rel_file_path_posix": file.relative_to(
                            dataset_base_folder
                        ).as_posix(),
                        "SNR": snr,
                        "machine_id": machine_id,
                    }

    metadata = pd.DataFrame(record_generator())

    # === split data to train and test ===
    metadata["split"] = "train"

    for machine_id in metadata["machine_id"].unique():
        selection = metadata[metadata["machine_id"] == machine_id]

        normal_idx = selection[selection["anomaly_type"] == "normal"].index  # type: ignore
        abnormal_idx = selection[selection["anomaly_type"] != "normal"].index  # type: ignore

        # for each machine id the number of normal and abnormal files are the same
        rng = np.random.default_rng(seed=42)
        chosen_normals = rng.choice(normal_idx, len(abnormal_idx), replace=False)

        # Set split type
        metadata.loc[chosen_normals, "split"] = "test"  # type: ignore
        metadata.loc[abnormal_idx, "split"] = "test"
    metadata["num_frames"] = FRAMES_PER_SIGNAL
    metadata.to_csv(dir_path / "metadata.csv", index=False)


class MIMIIStorage(DataStorage):
    def __init__(
        self,
        dataset_base_folder: Path | str,
        part_name: str,
    ):
        self._dataset_base_folder = Path(dataset_base_folder)
        self._part_name = part_name
        self._metadata_path = self._dataset_base_folder / part_name / "metadata.csv"
        self._metadata: pd.DataFrame | None = None

    @property
    def dataset_base_folder(self) -> Path:
        return self._dataset_base_folder

    def check_integrity(self, force: bool = False):
        process_part(
            dataset_base_folder=self._dataset_base_folder,
            part_name=self._part_name,
            force=force,
        )
        self._metadata = pd.read_csv(self._metadata_path)

    @property
    def metadata(self) -> pd.DataFrame:
        if self._metadata is None:
            self.check_integrity()
        if not isinstance(self._metadata, pd.DataFrame):
            raise ValueError("Metadata is not a valid DataFrame.")
        return self._metadata
