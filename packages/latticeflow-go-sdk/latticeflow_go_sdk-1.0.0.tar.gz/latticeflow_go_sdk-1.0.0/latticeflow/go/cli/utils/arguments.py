from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

import latticeflow.go.cli.utils.exceptions as cli_exc
import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.utils.configuration import get_configuration_file
from latticeflow.go.cli.utils.constants import LF_APP_KEY_CONTEXT_NAME
from latticeflow.go.models import Role


def parse_user_roles(roles: str) -> list[Role]:
    try:
        return [Role(value=role.strip()) for role in roles.split(",")]
    except Exception as error:
        raise typer.BadParameter(f"Could not parse roles '{roles}': {error}")


def check_path_not_emtpy(path: Path) -> Path:
    if not str(path).strip() or str(path) == ".":
        raise typer.BadParameter("Invalid path provided.")
    return path


def load_app_key_from_file() -> str | None:
    try:
        config, config_file = get_configuration_file()
    except Exception:
        cli_print.log_info(
            f"Contents of the configuration file at path '{config_file}' could not be loaded. "
            "The file was created anew."
        )

    if ai_app_key := config.get(LF_APP_KEY_CONTEXT_NAME):
        return ai_app_key

    raise cli_exc.CLIMissingAppContextError()


def glob_config_path_argument(entity_name: str) -> Any:
    return typer.Argument(
        ..., help=f"Glob path to {entity_name} configs.", callback=check_path_not_emtpy
    )


def single_config_path_argument(entity_name: str) -> Any:
    return typer.Argument(
        ...,
        help=f"Path to a single {entity_name} config.",
        callback=check_path_not_emtpy,
    )


def delete_key_argument(entity_name: str) -> Any:
    return typer.Argument(..., help=f"Key of the {entity_name} to be deleted.")


def export_key_argument(entity_name: str) -> Any:
    return typer.Argument(..., help=f"Key of the {entity_name} to be exported.")


def test_configuration_key_argument(entity_name: str) -> Any:
    return typer.Argument(
        ..., help=f"Key of the {entity_name} of which configuration should be tested."
    )


app_key_option = typer.Option(
    ...,
    help=(
        "The key of the AI app in context. "
        "If not provided, the value set by `lf workon` will be used (if any)."
    ),
    default_factory=load_app_key_from_file,
)
json_flag_option = typer.Option(
    False, "--json", help="If set, the output is printed to stdout as JSON."
)
export_output_path_option = typer.Option(
    None,
    "--output",
    help="Path to output YAML file. Omit to print as JSON to stdout.",
    callback=check_path_not_emtpy,
)
create_user_email_option = typer.Option(
    ..., help="A unique email for the user. Example: 'johndoe@latticeflow.ai'."
)
create_user_name_option = typer.Option(
    ..., help="Name of the user. Example: 'John Doe'."
)
create_user_roles_option = typer.Option(
    ...,
    help=(
        "Role(s) to assign to the user (comma-separated). Possible values are: "
        "'admin', 'member', 'viewer'. Example:'admin,member'."
    ),
)
reset_password_email_option = typer.Option(
    ...,
    help="Email of the user whose password to reset. Example: 'johndoe@latticeflow.ai'.",
)
