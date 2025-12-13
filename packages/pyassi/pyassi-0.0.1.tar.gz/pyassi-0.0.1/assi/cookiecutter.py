import argparse
from pathlib import Path
from shutil import copy
from importlib import import_module
from typing import Optional


def resolve_model_class(model_name: str) -> type:
    """
    Import and resolve a model class by name from assi.models.

    Parameters
    ----------
    model_name : str
        Name of the model class (e.g., 'AENet')

    Returns
    -------
    type
        The model class

    Raises
    ------
    AttributeError
        If the model class is not found in assi.models
    ImportError
        If assi.models cannot be imported
    """
    models_module = import_module("assi.models")
    model_class = getattr(models_module, model_name)
    return model_class


def get_model_source_dir(model_class: type) -> Path:
    """
    Get the directory where the model class source code is located.

    Parameters
    ----------
    model_class : type
        The model class object

    Returns
    -------
    Path
        Path to the directory containing the model source code

    Raises
    ------
    ValueError
        If the source directory cannot be determined
    """
    if hasattr(model_class, "__module__"):
        module_name = model_class.__module__
        # Get the module
        module = import_module(module_name)
        if hasattr(module, "__file__") and module.__file__:
            return Path(module.__file__).parent

    raise ValueError(f"Could not determine source directory for {model_class}")


def copy_config(
    model_name: str, output_dir: Optional[Path] = None, force: bool = False
) -> Path:
    """
    Copy module_fit_config.yml from the model's source directory to the output directory.

    Parameters
    ----------
    model_name : str
        Name of the model class (e.g., 'AENet')
    output_dir : Path, optional
        Directory to copy the config to. If None, uses current working directory.
    force : bool, optional
        If True, overwrite existing files. If False (default), raise error if file exists.

    Returns
    -------
    Path
        Path to the copied configuration file

    Raises
    ------
    FileNotFoundError
        If module_fit_config.yml is not found in the model's directory
    FileExistsError
        If output file already exists and force is False
    ImportError
        If the model class cannot be imported
    AttributeError
        If the model class is not found in assi.models
    """
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)

    # Resolve model class
    model_class = resolve_model_class(model_name)

    # Get source directory
    source_dir = get_model_source_dir(model_class)

    # Find config file
    config_file = source_dir / "module_fit_config.yml"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_file}\n"
            f"Expected to find module_fit_config.yml in {source_dir}"
        )

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy file
    output_path = output_dir / config_file.name

    if output_path.exists() and not force:
        raise FileExistsError(
            f"Output file already exists: {output_path}\nUse --force to overwrite"
        )

    copy(config_file, output_path)

    return output_path


def create_cli_script(output_dir: Optional[Path] = None, force: bool = False) -> Path:
    """
    Create a Python CLI script with run_cli entry point.

    Parameters
    ----------
    output_dir : Path, optional
        Directory to create the script in. If None, uses current working directory.
    force : bool, optional
        If True, overwrite existing files. If False (default), raise error if file exists.

    Returns
    -------
    Path
        Path to the created script file

    Raises
    ------
    FileExistsError
        If output file already exists and force is False
    """
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define output file
    output_path = output_dir / "module.py"

    # Check if file exists
    if output_path.exists() and not force:
        raise FileExistsError(
            f"Output file already exists: {output_path}\nUse --force to overwrite"
        )

    # Define script content
    script_content = """from assi.cli import run_cli


if __name__ == "__main__":
    run_cli(__file__, run=True)
"""

    # Write file
    output_path.write_text(script_content)

    return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Copy model configuration files for models in assi.models"
    )

    parser.add_argument(
        "model",
        help="Name of the model class (e.g., AENet)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory (default: current working directory)",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )

    args = parser.parse_args()

    copy_config(args.model, args.output, force=args.force)
    create_cli_script(args.output, force=args.force)


if __name__ == "__main__":
    main()
