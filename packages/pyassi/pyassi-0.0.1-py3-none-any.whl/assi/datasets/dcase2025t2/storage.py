import pandas as pd
from pathlib import Path
import urllib.request
import zipfile
import contextlib
import wave


from assi.datastorage import DataStorage


DATASET_PARTS_ZIP_URLS = {
    "dev_ToyCar": "https://zenodo.org/records/15097779/files/dev_ToyCar.zip",
    "dev_ToyTrain": "https://zenodo.org/records/15097779/files/dev_ToyTrain.zip",
    "dev_bearing": "https://zenodo.org/records/15097779/files/dev_bearing.zip",
    "dev_fan": "https://zenodo.org/records/15097779/files/dev_fan.zip",
    "dev_gearbox": "https://zenodo.org/records/15097779/files/dev_gearbox.zip",
    "dev_slider": "https://zenodo.org/records/15097779/files/dev_slider.zip",
    "dev_valve": "https://zenodo.org/records/15097779/files/dev_valve.zip",
    "eval-train_ToyRCCar": "https://zenodo.org/records/15392814/files/eval_data_ToyRCCar_train.zip",
    "eval-train_ToyPet": "https://zenodo.org/records/15392814/files/eval_data_ToyPet_train.zip",
    "eval-train_HomeCamera": "https://zenodo.org/records/15392814/files/eval_data_HomeCamera_train.zip",
    "eval-train_AutoTrash": "https://zenodo.org/records/15392814/files/eval_data_AutoTrash_train.zip",
    "eval-train_Polisher": "https://zenodo.org/records/15392814/files/eval_data_Polisher_train.zip",
    "eval-train_ScrewFeeder": "https://zenodo.org/records/15392814/files/eval_data_ScrewFeeder_train.zip",
    "eval-train_BandSealer": "https://zenodo.org/records/15392814/files/eval_data_BandSealer_train.zip",
    "eval-train_CoffeeGrinder": "https://zenodo.org/records/15392814/files/eval_data_CoffeeGrinder_train.zip",
    "eval-test_ToyRCCar": "https://zenodo.org/records/15519362/files/eval_data_ToyRCCar_test.zip",
    "eval-test_ToyPet": "https://zenodo.org/records/15519362/files/eval_data_ToyPet_test.zip",
    "eval-test_HomeCamera": "https://zenodo.org/records/15519362/files/eval_data_HomeCamera_test.zip",
    "eval-test_AutoTrash": "https://zenodo.org/records/15519362/files/eval_data_AutoTrash_test.zip",
    "eval-test_Polisher": "https://zenodo.org/records/15519362/files/eval_data_Polisher_test.zip",
    "eval-test_ScrewFeeder": "https://zenodo.org/records/15519362/files/eval_data_ScrewFeeder_test.zip",
    "eval-test_BandSealer": "https://zenodo.org/records/15519362/files/eval_data_BandSealer_test.zip",
    "eval-test_CoffeeGrinder": "https://zenodo.org/records/15519362/files/eval_data_CoffeeGrinder_test.zip",
}


def download(zip_url: str, zip_path: Path):
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = int(downloaded * 100 / total_size) if total_size > 0 else 0
        print(f"\rDownloading {zip_url} {percent}%", end="", flush=True)

    urllib.request.urlretrieve(zip_url, zip_path, reporthook=show_progress)


def extract(zip_path: Path, dataset_base_folder: Path):
    dataset_base_folder.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dataset_base_folder)
    except Exception as e:
        dataset_base_folder.unlink(missing_ok=True)
        raise e


def process_part(force, dataset_base_folder: Path, part_name: str):
    dir_path = dataset_base_folder / f"{part_name}"
    zip_path = dataset_base_folder / f"{part_name}.zip"

    zip_url = DATASET_PARTS_ZIP_URLS[part_name]

    # === downloading ===
    if force or not dir_path.exists() or not dir_path.is_dir():
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
    #          supplemental
    #             000001.wav
    #              000002.wav
    #              ....
    #          test
    #              000002.wav
    #              000001.wav
    #              ....
    #          train
    #              000001.wav
    #              000002.wav
    #              ....
    #
    part_type, machine_type = part_name.split("_")

    def record_generator():
        for folder in (dir_path / machine_type).iterdir():
            if not folder.is_dir():
                continue

            split = folder.name
            if split not in ["test", "train"]:
                continue

            for file in folder.iterdir():
                if not file.suffix == ".wav":
                    continue

                with contextlib.closing(wave.open(str(file), "r")) as f:
                    num_frames = f.getnframes()

                if part_type == "eval-test":
                    _, section, idx = file.stem.split("_")
                    section = int(section)
                    idx = int(idx)

                    yield {
                        "machine_type": machine_type,
                        "split": split,
                        "rel_file_path_posix": file.relative_to(
                            dataset_base_folder
                        ).as_posix(),
                        "num_frames": num_frames,
                    }
                    continue

                _, section, domain, split, anomaly_type, idx, *attributes = (
                    file.stem.split("_")
                )
                section = int(section)
                idx = int(idx)

                yield {
                    "machine_type": machine_type,
                    "anomaly_type": anomaly_type,
                    "domain": domain,
                    "split": split,
                    "rel_file_path_posix": file.relative_to(
                        dataset_base_folder
                    ).as_posix(),
                    "num_frames": num_frames,
                }

    metadata = pd.DataFrame(record_generator())
    metadata.to_csv(dir_path / "metadata.csv", index=False)


class DCASE2025T2Storage(DataStorage):
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
