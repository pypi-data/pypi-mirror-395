from __future__ import annotations

from pathlib import Path
from typing import Callable

import typer

import latticeflow.go.cli.utils.arguments as cli_args
import latticeflow.go.cli.utils.exceptions as cli_exc
import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go import Client
from latticeflow.go.cli.utils.dtypes import CLICreateModelAdapter
from latticeflow.go.cli.utils.helpers import create_single_entity
from latticeflow.go.cli.utils.helpers import dump_entity_to_yaml_file
from latticeflow.go.cli.utils.helpers import get_client_from_env
from latticeflow.go.cli.utils.helpers import get_files_at_path
from latticeflow.go.cli.utils.helpers import is_update_payload_same_as_existing_entity
from latticeflow.go.cli.utils.helpers import register_app_callback
from latticeflow.go.cli.utils.helpers import update_single_entity
from latticeflow.go.cli.utils.schema_mappers import map_model_adapter_api_to_cli_entity
from latticeflow.go.cli.utils.schema_mappers import map_model_adapter_cli_to_api_entity
from latticeflow.go.cli.utils.yaml_utils import load_yaml_recursively
from latticeflow.go.models import ModelAdapter
from latticeflow.go.models import StoredModelAdapter


PRETTY_ENTITY_NAME = "model adapter"
TABLE_COLUMNS: list[tuple[str, Callable[[StoredModelAdapter], str]]] = [
    ("Key", lambda app: app.key),
    ("Name", lambda app: app.display_name),
]
model_adapter_app = typer.Typer(help="Model adapter commands")
register_app_callback(model_adapter_app)


@model_adapter_app.command("list")
def _list(is_json_output: bool = cli_args.json_flag_option) -> None:
    """List all model adapters as JSON or in a table."""
    if is_json_output:
        cli_print.suppress_logging()

    client = get_client_from_env()
    try:
        stored_model_adapters = (
            client.model_adapters.get_model_adapters().model_adapters
        )
        cli_model_adapters = [
            map_model_adapter_api_to_cli_entity(
                stored_model_adapter=stored_model_adapter
            )
            for stored_model_adapter in stored_model_adapters
        ]
        if is_json_output:
            cli_print.print_entities_as_json(cli_model_adapters)
        else:
            cli_print.print_table("Model adapters", cli_model_adapters, TABLE_COLUMNS)
    except Exception as error:
        raise cli_exc.CLIListError(PRETTY_ENTITY_NAME) from error


@model_adapter_app.command("create")
def _create(
    path: Path = cli_args.glob_config_path_argument(PRETTY_ENTITY_NAME),
) -> None:
    """Create/update model adapter(s) based on YAML configuration(s)."""
    if not (config_files := get_files_at_path(path)):
        raise cli_exc.CLIConfigNotFoundError(PRETTY_ENTITY_NAME, path)

    client = get_client_from_env()
    existing_stored_model_adapters_by_key = {
        model_adapter.key: model_adapter
        for model_adapter in client.model_adapters.get_model_adapters().model_adapters
    }
    is_creating_single_entity = len(config_files) == 1
    failures = 0
    for config_file in config_files:
        try:
            cli_model_adapter = _get_cli_model_adapter_from_file(config_file)
            model_adapter = map_model_adapter_cli_to_api_entity(
                cli_model_adapter=cli_model_adapter, config_file=config_file
            )
            stored_model_adapter = existing_stored_model_adapters_by_key.get(
                cli_model_adapter.key
            )
            create_or_update_single_model_adapter(
                client, model_adapter, stored_model_adapter
            )
        except Exception as error:
            failures += 1
            if is_creating_single_entity:
                raise cli_exc.CLICreateUpdateSingleEntityError(
                    PRETTY_ENTITY_NAME, config_file
                ) from error
            cli_print.log_create_update_fail_warning(
                PRETTY_ENTITY_NAME, config_file, error
            )
    if failures == len(config_files):
        raise cli_exc.CLICreateUpdateAllFailedError(PRETTY_ENTITY_NAME, config_file)


@model_adapter_app.command("delete")
def _delete(key: str = cli_args.delete_key_argument(PRETTY_ENTITY_NAME)) -> None:
    """Delete the model adapter with the provided key."""
    client = get_client_from_env()
    try:
        cli_print.log_delete_attempt_info(PRETTY_ENTITY_NAME, key)
        client.model_adapters.delete_model_adapter_by_key(key=key)
        cli_print.log_delete_success_info(PRETTY_ENTITY_NAME, key)
    except Exception as error:
        raise cli_exc.CLIDeleteError(PRETTY_ENTITY_NAME, key) from error


@model_adapter_app.command("export")
def _export(
    key: str = cli_args.export_key_argument(PRETTY_ENTITY_NAME),
    output: Path | None = cli_args.export_output_path_option,
) -> None:
    """Export the model adapter with the provided key to a file or print as JSON."""
    if not output:
        cli_print.suppress_logging()

    client = get_client_from_env()
    try:
        stored_model_adapter = client.model_adapters.get_model_adapter_by_key(key=key)
        cli_model_adapter = map_model_adapter_api_to_cli_entity(
            stored_model_adapter=stored_model_adapter
        )
        if output:
            dump_entity_to_yaml_file(output, cli_model_adapter)
            cli_print.log_export_success_info(PRETTY_ENTITY_NAME, output, key)
        else:
            cli_print.print_entities_as_json(cli_model_adapter)
    except Exception as error:
        raise cli_exc.CLIExportError(
            PRETTY_ENTITY_NAME, key, output_path=output
        ) from error


def _get_cli_model_adapter_from_file(config_file: Path) -> CLICreateModelAdapter:
    try:
        return CLICreateModelAdapter.model_validate(
            load_yaml_recursively(config_file), ignore_extra=False
        )
    except Exception as error:
        raise cli_exc.CLIInvalidConfigError(PRETTY_ENTITY_NAME, config_file) from error


def create_or_update_single_model_adapter(
    client: Client,
    model_adapter: ModelAdapter,
    stored_model_adapter: StoredModelAdapter | None,
) -> StoredModelAdapter:
    if stored_model_adapter and is_update_payload_same_as_existing_entity(
        model_adapter, stored_model_adapter
    ):
        cli_print.log_no_change_info(PRETTY_ENTITY_NAME, model_adapter.key)
        return stored_model_adapter
    elif stored_model_adapter:
        return update_single_model_adapter(client, stored_model_adapter, model_adapter)
    else:
        return create_single_model_adapter(client, model_adapter)


def update_single_model_adapter(
    client: Client,
    stored_model_adapter: StoredModelAdapter,
    model_adapter: ModelAdapter,
) -> StoredModelAdapter:
    return update_single_entity(
        PRETTY_ENTITY_NAME,
        lambda: client.model_adapters.update_model_adapter(
            stored_model_adapter.id, model_adapter
        ),
        stored_model_adapter.key,
    )


def create_single_model_adapter(
    client: Client, model_adapter: ModelAdapter
) -> StoredModelAdapter:
    return create_single_entity(
        PRETTY_ENTITY_NAME,
        lambda: client.model_adapters.create_model_adapter(model_adapter),
        model_adapter.key,
    )
