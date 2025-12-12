from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable
from typing import TypeVar

import typer

import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.utils.env_vars import get_cli_env_vars
from latticeflow.go.cli.utils.yaml_utils import yaml_safe_dump_pretty
from latticeflow.go.client import Client
from latticeflow.go.models import LFBaseModel


def get_client_from_env(
    get_cli_env_vars_function: Callable = get_cli_env_vars,
) -> Client:
    return Client(*get_cli_env_vars_function())


def app_callback(check_env_vars_function) -> None:  # type: ignore[no-untyped-def]
    # NOTE: If the command is run with the `--help` flag, we
    # do not want to check for the env variables (i.e. force
    # the user to set them before asking for help). We use this
    # crude mechanism for the lack of a better way of checking in
    # Typer/Click.
    is_run_with_help_flag = "--help" in sys.argv
    if is_run_with_help_flag:
        return

    # NOTE: We dry-run the getter for the env vars to check that
    # they are set before actually running the command and parsing
    # the command args. This ensures that command args are not even
    # validated if the env vars are not set.
    check_env_vars_function()


def register_app_callback(
    cli_app: typer.Typer,
    check_env_vars_function: Callable = get_cli_env_vars,
    skipped_subcommands: set[str] | None = None,
    included_subcommands: set[str] | None = None,
) -> None:
    assert (skipped_subcommands is None) or (included_subcommands is None)

    @cli_app.callback()
    def _app_cb(ctx: typer.Context) -> None:
        if ctx.invoked_subcommand is not None:
            if included_subcommands is not None:
                if ctx.invoked_subcommand in included_subcommands:
                    app_callback(check_env_vars_function)
                return

            if skipped_subcommands and ctx.invoked_subcommand in skipped_subcommands:
                return

        app_callback(check_env_vars_function)


def get_files_at_path(path: Path) -> list[Path]:
    if path.is_absolute():
        files = sorted(path.parent.glob(path.name), key=lambda p: str(p))
    else:
        files = sorted(Path().glob(str(path)), key=lambda p: str(p))

    return files


S = TypeVar("S")


def update_single_entity(
    pretty_entity_name: str,
    update_fn: Callable[[], S],
    entity_identifier_value: str,
    entity_identifier_type: str = "key",
) -> S:
    cli_print.log_update_attempt_info(
        pretty_entity_name, entity_identifier_value, entity_identifier_type
    )
    updated = update_fn()
    cli_print.log_update_success_info(
        pretty_entity_name, entity_identifier_value, entity_identifier_type
    )
    return updated


def create_single_entity(
    pretty_entity_name: str,
    create_fn: Callable[[], S],
    entity_identifier_value: str | None,
    entity_identifier_type: str | None = "key",
) -> S:
    cli_print.log_create_attempt_info(
        pretty_entity_name, entity_identifier_value, entity_identifier_type
    )
    created = create_fn()
    cli_print.log_create_success_info(
        pretty_entity_name, entity_identifier_value, entity_identifier_type
    )
    return created


def is_update_payload_same_as_existing_entity(
    updated_entity: LFBaseModel,
    existing_entity: LFBaseModel,
    comparison_class_override: type[LFBaseModel] | None = None,
) -> bool:
    comparison_class = (
        comparison_class_override if comparison_class_override else type(updated_entity)
    )
    updated_entity_as_comparison_class = comparison_class.model_validate(
        updated_entity.model_dump()
    )
    existing_entity_as_comparison_class = comparison_class.model_validate(
        existing_entity.model_dump()
    )
    # NOTE: `exclude_none=True` ensures that fields explicitly set to None are treated
    # the same as unset fields, so both are omitted from the comparison.
    updated_dict = updated_entity_as_comparison_class.model_dump(exclude_none=True)
    existing_dict = existing_entity_as_comparison_class.model_dump(exclude_none=True)

    return updated_dict == existing_dict


def dump_entity_to_yaml_file(file: Path, entity: LFBaseModel) -> None:
    file.write_text(yaml_safe_dump_pretty(entity.model_dump(mode="json")))
