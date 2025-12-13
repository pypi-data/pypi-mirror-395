from lightning.pytorch.cli import LightningCLI
from pathlib import Path
import os
from jsonargparse import Namespace
from omegaconf import OmegaConf
from dataclasses import dataclass


@dataclass
class Requirement:
    name: str
    version: str | None = None


@dataclass
class RequirementsConfig:
    unnecessary: list[Requirement] | None = None
    replacements: dict[str, Requirement] | None = None
    additional: list[Requirement] | None = None


def fix_clearml_requirements(requirements: RequirementsConfig | None):
    """
    Fix ClearML requirements based on the provided configuration.

    This function modifies the ClearML task requirements according to the
    specified configuration, allowing for removal of unnecessary requirements,
    replacement of existing requirements, and addition of new requirements.


    Parameters
    ----------
    requirements : RequirementsConfig or None
        Configuration specifying which requirements to remove, replace, or add.
        If None, no changes are made.
    """
    if requirements is None:
        return

    from clearml.task import Task

    # remove unnecessary requirements
    if requirements.unnecessary is not None:
        for req in requirements.unnecessary:
            Task.ignore_requirements(req.name)

    # replace requirements
    if requirements.replacements is not None:
        for name, req in requirements.replacements.items():
            Task.ignore_requirements(name)
            Task.add_requirements(req.name, req.version)

    # add additional requirements
    if requirements.additional is not None:
        for req in requirements.additional:
            Task.add_requirements(req.name, req.version)


class CustomCLI(LightningCLI):
    """
    Custom LightningCLI with ClearML integration.

    This class extends the LightningCLI to add ClearML integration for experiment
    tracking and management. It allows for automatic logging of experiments to
    ClearML, with options to configure the ClearML task and requirements.

    Parameters
    ----------
    *args
        Positional arguments passed to the parent LightningCLI class
    clearml_requirements : RequirementsConfig, optional
        Configuration for ClearML requirements, by default None
    **kwargs
        Keyword arguments passed to the parent LightningCLI class
    """

    def __init__(
        self,
        *args,
        clearml_requirements: RequirementsConfig | None = None,
        **kwargs,
    ):
        self.clearml_requirements = clearml_requirements
        super().__init__(*args, **kwargs)

    def add_arguments_to_parser(self, parser):
        """
        Add custom arguments to the argument parser.


        This method adds ClearML-specific arguments to the CLI parser, allowing
        users to configure ClearML integration through command line arguments.

        Parameters
        ----------
        parser : ArgumentParser
            The argument parser to which to add arguments


        Adds the following arguments:

        --use_clearml
            If specified, enables ClearML integration
        --queue_name
            Name of the ClearML queue to use for remote execution
        --project_name
            Name of the ClearML project (default: "Untitled")
        --task_name
            Name of the ClearML task (default: "Untitled")
        --clearml_config_file
            Path to the ClearML config file (default: "clearml.conf")
        """
        parser.add_argument("--use_clearml", action="store_true")
        parser.add_argument("--queue_name", default="")
        parser.add_argument("--project_name", default="Untitled")
        parser.add_argument("--task_name", default="Untitled")
        parser.add_argument("--clearml_config_file", default="clearml.conf")

    def before_instantiate_classes(self):
        """
        Execute before instantiating classes in the CLI.


        This method is called before the CLI instantiates any classes. It sets up
        ClearML integration by configuring the ClearML environment, initializing
        a ClearML task, and optionally executing the task remotely.


        Notes
        -----
        This method will:

        - Set the ClearML config file environment variable
        - Initialize a ClearML task with the specified project and task names
        - Apply any requirement fixes specified in the configuration
        - Execute the task remotely if a queue name is specified
        """
        if self.subcommand:
            current_config: Namespace = self.config.get(self.subcommand)

            try:
                import clearml.task
                from assi.clearml.utils import set_conf_env

                # Try to set CLEARML_CONFIG_FILE environment variable
                # You can baypass this by setting clearml_config_file parameter to empty string
                set_conf_env(current_config["clearml_config_file"])
            except ModuleNotFoundError:
                return

            if not current_config.get("use_clearml"):
                return

            fix_clearml_requirements(self.clearml_requirements)

            self.task: clearml.task.Task = clearml.task.Task.init(
                project_name=current_config.get("project_name"),
                task_name=current_config.get("task_name"),
                output_uri=True,
                auto_connect_arg_parser={
                    "use_clearml": False,
                    "queue_name": False,
                    "project_name": False,
                    "task_name": False,
                    "clearml_config_file": False,
                },
            )

            if queue_name := current_config.get("queue_name"):
                self.task.execute_remotely(queue_name=queue_name, exit_process=True)


def run_cli(
    main_filepath: str | os.PathLike[str],
    run: bool = False,
    clearml_requirements: RequirementsConfig | None = None,
) -> CustomCLI:
    """
    Run the custom CLI for a given main file.
    You can add flowing lines to the python file:

        if __name__ == "__main__":
            run_cli(__file__)


    This function sets up and returns a CustomCLI instance for the specified
    main file. It registers a custom OmegaConf resolver for the lightning logs directory `assi.lightning_logs_dir`
    and configures the CLI with default settings.



    Parameters
    ----------
    main_filepath : str or os.PathLike[str]
        Path to the main file for which to run the CLI
    run : bool, default=False
        Whether to run the CLI immediately after creation
    clearml_requirements: RequirementsConfig | None, default=None
        Requirements fixes for the ClearML task, helpful for remote task execution.
    Returns
    -------
    CustomCLI
        Configured CustomCLI instance
    """
    main_filepath = Path(main_filepath).relative_to(os.getcwd())

    OmegaConf.register_new_resolver(
        "assi.lightning_logs_dir", lambda: str(main_filepath.parent)
    )

    return CustomCLI(
        parser_kwargs={
            "fit": {
                "default_config_files": [
                    (
                        main_filepath.parent / f"{main_filepath.stem}_fit_config.yml"
                    ).as_posix()
                ],
            },
            "parser_mode": "omegaconf",
        },
        run=run,
        clearml_requirements=clearml_requirements,
    )
