from pathlib import Path
import clearml.config
import os
import warnings


def set_conf_env(config_file: str | None = "clearml.conf"):
    if clearml.config.running_remotely():
        return

    if config_file is None:
        return

    if not config_file:
        return

    config_file_parh = Path(config_file).absolute()

    if not config_file_parh.exists() or not config_file_parh.is_file():
        warnings.warn(f"ClearML config file {config_file} does not exist.")

    os.environ["CLEARML_CONFIG_FILE"] = str(config_file_parh)
