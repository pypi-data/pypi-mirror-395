from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import questionary
import typer
from requests.structures import CaseInsensitiveDict

import latticeflow.go.cli.model_adapters as model_adapter_cli
import latticeflow.go.cli.utils.arguments as cli_args
import latticeflow.go.cli.utils.exceptions as cli_exc
import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.utils.dtypes import CLICreateModel
from latticeflow.go.cli.utils.dtypes import CLICreateModelAdapter
from latticeflow.go.cli.utils.dtypes import UserOrLFKey
from latticeflow.go.cli.utils.helpers import create_single_entity
from latticeflow.go.cli.utils.helpers import dump_entity_to_yaml_file
from latticeflow.go.cli.utils.helpers import get_client_from_env
from latticeflow.go.cli.utils.helpers import get_files_at_path
from latticeflow.go.cli.utils.helpers import is_update_payload_same_as_existing_entity
from latticeflow.go.cli.utils.helpers import register_app_callback
from latticeflow.go.cli.utils.helpers import update_single_entity
from latticeflow.go.cli.utils.schema_mappers import EntityByIdentifiersMap
from latticeflow.go.cli.utils.schema_mappers import map_model_adapter_cli_to_api_entity
from latticeflow.go.cli.utils.schema_mappers import map_model_api_to_cli_entity
from latticeflow.go.cli.utils.schema_mappers import map_model_cli_to_api_entity
from latticeflow.go.cli.utils.yaml_utils import load_yaml_recursively
from latticeflow.go.client import Client
from latticeflow.go.models import IntegrationModelProviderId
from latticeflow.go.models import MLTask
from latticeflow.go.models import Modality
from latticeflow.go.models import Model
from latticeflow.go.models import ModelAdapterInput
from latticeflow.go.models import ModelAdapterTransformationError
from latticeflow.go.models import ModelCustomConnectionConfig
from latticeflow.go.models import ModelProviderConnectionConfig
from latticeflow.go.models import RawModelInput
from latticeflow.go.models import RawModelOutput
from latticeflow.go.models import StoredModel
from latticeflow.go.models import StoredModelAdapter
from latticeflow.go.types import ApiError


PRETTY_ENTITY_NAME = "model"
TABLE_COLUMNS: list[tuple[str, Callable[[StoredModel], str]]] = [
    ("Key", lambda model: model.key),
    ("Name", lambda model: model.display_name),
    (
        "URL",
        lambda model: model.config.url
        if isinstance(model.config, ModelCustomConnectionConfig)
        else "",
    ),
]
model_app = typer.Typer(help="Model commands")
register_app_callback(model_app)


@model_app.command("list")
def _list(is_json_output: bool = cli_args.json_flag_option) -> None:
    """List all models as JSON or in a table."""
    if is_json_output:
        cli_print.suppress_logging()

    client = get_client_from_env()
    try:
        stored_models = client.models.get_models().models
        model_adapters_map = EntityByIdentifiersMap(
            client.model_adapters.get_model_adapters().model_adapters
        )
        cli_models = [
            map_model_api_to_cli_entity(
                stored_model=stored_model, model_adapters_map=model_adapters_map
            )
            for stored_model in stored_models
        ]
        if is_json_output:
            cli_print.print_entities_as_json(cli_models)
        else:
            cli_print.print_table("Models", cli_models, TABLE_COLUMNS)
    except Exception as error:
        raise cli_exc.CLIListError(PRETTY_ENTITY_NAME) from error


@model_app.command("create")
def _create(
    path: Path = cli_args.glob_config_path_argument(PRETTY_ENTITY_NAME),
) -> None:
    """Create/update model(s) based on YAML configuration(s)."""
    if not (config_files := get_files_at_path(path)):
        raise cli_exc.CLIConfigNotFoundError(PRETTY_ENTITY_NAME, path)

    client = get_client_from_env()
    existing_stored_models_by_key = {
        model.key: model for model in client.models.get_models().models
    }
    model_adapters_map = EntityByIdentifiersMap(
        client.model_adapters.get_model_adapters().model_adapters
    )
    is_creating_single_entity = len(config_files) == 1
    failures = 0
    for config_file in config_files:
        try:
            cli_model = _get_cli_model_from_file(config_file)
            if isinstance(cli_model.adapter, CLICreateModelAdapter):
                stored_model_adapter = _create_inlined_model_adapter(
                    client, cli_model.adapter, config_file
                )
                model_adapters_map.entity_map_by_key[stored_model_adapter.key] = (
                    stored_model_adapter
                )
                _map_inlined_model_adapter_to_key(cli_model, stored_model_adapter)
            model = map_model_cli_to_api_entity(
                cli_model=cli_model,
                model_adapters_map=model_adapters_map,
                config_file=path,
            )
            stored_model = existing_stored_models_by_key.get(model.key)
            create_or_update_single_model(client, model, stored_model)
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


@model_app.command("delete")
def _delete(key: str = cli_args.delete_key_argument(PRETTY_ENTITY_NAME)) -> None:
    """Delete the model with the provided key."""
    client = get_client_from_env()
    try:
        cli_print.log_delete_attempt_info(PRETTY_ENTITY_NAME, key)
        client.models.delete_model_by_key(key=key)
        cli_print.log_delete_success_info(PRETTY_ENTITY_NAME, key)
    except Exception as error:
        raise cli_exc.CLIDeleteError(PRETTY_ENTITY_NAME, key) from error


@model_app.command("export")
def _export(
    key: str = cli_args.export_key_argument(PRETTY_ENTITY_NAME),
    output: Path | None = cli_args.export_output_path_option,
) -> None:
    """Export the model with the provided key to a file or print as JSON."""
    if not output:
        cli_print.suppress_logging()

    client = get_client_from_env()
    try:
        stored_model = client.models.get_model_by_key(key=key)
        cli_model = map_model_api_to_cli_entity(
            stored_model=stored_model,
            model_adapters_map=EntityByIdentifiersMap(
                client.model_adapters.get_model_adapters().model_adapters
            ),
        )
        if output:
            dump_entity_to_yaml_file(output, cli_model)
            cli_print.log_export_success_info(PRETTY_ENTITY_NAME, output, key)
        else:
            cli_print.print_entities_as_json(cli_model)
    except Exception as error:
        raise cli_exc.CLIExportError(
            PRETTY_ENTITY_NAME, key, output_path=output
        ) from error


@model_app.command("from-provider")
def _create_model_from_provider() -> None:
    """Integrate a model from a third-party provider (e.g. OpenAI)."""
    selected_integration_id = IntegrationModelProviderId(
        questionary.select(
            "Select the provider of the model:",
            choices=[provider_id.value for provider_id in IntegrationModelProviderId],
        ).ask()
    )

    client = get_client_from_env()
    models = []
    for model_provider in client.models.get_model_providers().model_providers:
        if (
            model_provider.id == selected_integration_id
            and model_provider.has_credentials
        ):
            models = model_provider.models
            break

    if len(models) == 0:
        raise cli_exc.CLIProviderModelsNotFoundError(selected_integration_id)

    selected_model_name = questionary.autocomplete(
        "Select the model to integrate (Press Tab to see all models):",
        choices=[model.display_name for model in models],
        match_middle=True,
    ).ask()

    selected_model = next(
        (model for model in models if model.display_name == selected_model_name)
    )
    client.models.create_model(selected_model)


@model_app.command("test")
def _test(
    key: str = cli_args.test_configuration_key_argument(PRETTY_ENTITY_NAME),
    model_input_path: Path | None = typer.Option(
        None,
        "--model-input",
        help="Path to a JSON file with a model input in LatticeFlow AI format."
        "If not provided, default is used, for more details see "
        "https://aigo.latticeflow.io/docs/model-io.",
        callback=cli_args.check_path_not_emtpy,
    ),
) -> None:
    """Test model connection, inference and I/O adapter mapping of the model
    with the provided key."""
    client = get_client_from_env()
    try:
        stored_model = client.models.get_model_by_key(key)
        model_input = _get_test_model_input(model_input_path, stored_model)
        cli_print.log_info("1. Checking connection to model.")
        _check_connection(client, stored_model.key, stored_model)
        cli_print.log_char_full_width("=")
        cli_print.log_info("2. Transforming model input.")
        stored_model_adapter = client.model_adapters.get_model_adapter(
            stored_model.adapter_id
        )
        raw_model_input = _transform_model_input(
            client, model_input, stored_model, stored_model_adapter
        )
        cli_print.log_char_full_width("=")
        cli_print.log_info("3. Running inference.")
        raw_model_output = _run_model_inference(client, stored_model, raw_model_input)
        cli_print.log_char_full_width("=")
        cli_print.log_info("4. Transforming model output.")
        _transform_model_output(
            client, stored_model, stored_model_adapter, raw_model_output
        )
        cli_print.log_char_full_width("=")
        cli_print.log_test_success_info(PRETTY_ENTITY_NAME, key)
    except Exception as error:
        raise cli_exc.CLITestConfigurationError(PRETTY_ENTITY_NAME, key) from error


def _get_cli_model_from_file(config_file: Path) -> CLICreateModel:
    try:
        return CLICreateModel.model_validate(
            load_yaml_recursively(config_file), ignore_extra=False
        )

    except Exception as error:
        raise cli_exc.CLIInvalidConfigError(PRETTY_ENTITY_NAME, config_file) from error


def _check_connection(client: Client, key: str, stored_model: StoredModel) -> None:
    if not isinstance(stored_model.config, ModelCustomConnectionConfig):
        raise cli_exc.CLIError(
            f"Model with key '{stored_model.key}' is not a model with a custom "
            "connection config."
        )

    if isinstance(stored_model.config, ModelCustomConnectionConfig):
        api_key_as_string_or_none = (
            stored_model.config.api_key.get_secret_value()
            if stored_model.config.api_key
            else None
        )
        cli_print.log_info(
            (
                f"- Key: {key}\n"
                f"- URL: {stored_model.config.url}\n"
                f"- API key: {api_key_as_string_or_none}\n"
                f"- Model key: {stored_model.config.model_key}"
            )
        )
    elif isinstance(stored_model.config, ModelProviderConnectionConfig):
        cli_print.log_info(
            (
                f"- Key: {key}\n"
                f"- Provider ID: {stored_model.config.provider_id}\n"
                f"- Model key: {stored_model.config.model_key}"
            )
        )

    connection_check_result = client.models.check_model_connection(stored_model.id)
    returned_message = (
        f"\nReturned message: {connection_check_result.message}"
        if connection_check_result.message
        else ""
    )
    if not connection_check_result.success:
        raise cli_exc.CLIError(
            f"Connection to model with key '{key}' was not successful.{returned_message}"
        )

    cli_print.log_info(
        f"Successfully connected to model with key '{key}'.{returned_message}"
    )


def _transform_model_input(
    client: Client,
    model_input: str,
    stored_model: StoredModel,
    stored_model_adapter: StoredModelAdapter,
) -> RawModelInput:
    cli_print.log_info(f"Model input in LatticeFlow AI format:\n{model_input}")
    cli_print.log_char_full_width("-")

    if stored_model_adapter.process_input:
        cli_print.log_info(
            f"Jinja input transform (from adapter "
            f"'{stored_model_adapter.display_name}'):\n"
            f"{stored_model_adapter.process_input.source_code}"
        )
        cli_print.log_char_full_width("-")

    try:
        raw_model_input = client.models.transform_input_model(
            stored_model.id, ModelAdapterInput(input=model_input)
        )
    except ApiError as error:
        if isinstance(error.error, ModelAdapterTransformationError):
            transformed_suffix = (
                f", {error.error.transformed}" if error.error.transformed else ""
            )
            raise cli_exc.CLIError(
                f"{error.error.message}{transformed_suffix}"
            ) from error
        raise

    cli_print.log_info(
        "Model input in the format expected by the model "
        f"(used for inference):\n{raw_model_input.input}"
    )

    return raw_model_input


def _format_headers(headers: dict[str, str]) -> str:
    return "\n".join(f"  {key}: {value}" for key, value in headers.items())


def _run_model_inference(
    client: Client, stored_model: StoredModel, raw_model_input: RawModelInput
) -> RawModelOutput:
    raw_model_output = client.models.run_model_inference(
        stored_model.id, body=raw_model_input
    )
    cli_print.log_info(
        f"Request headers:\n{_format_headers(raw_model_output.request_headers)}"
    )
    cli_print.log_char_full_width("-")

    # If the input headers specify that the input is JSON, verify that it is valid JSON.
    if (
        CaseInsensitiveDict(raw_model_output.request_headers).get("Content-Type")
        == "application/json"
    ):
        try:
            json.loads(raw_model_input.input)
        except json.JSONDecodeError as e:
            cli_print.log_warning(
                "The model input is not valid JSON, "
                "even though the request header specifies 'application/json'.\nError: "
                f"{str(e)}\nLine: {e.doc.splitlines()[e.lineno - 1]}\n"
                f"{' ' * (e.colno - 1 + 6)}^"
            )
            cli_print.log_char_full_width("-")

    cli_print.log_info(
        f"Response headers:\n{_format_headers(raw_model_output.response_headers)}"
    )
    return raw_model_output


def _transform_model_output(
    client: Client,
    stored_model: StoredModel,
    stored_model_adapter: StoredModelAdapter,
    raw_model_output: RawModelOutput,
) -> None:
    cli_print.log_info(
        f"Model output in the format returned by the model:\n{raw_model_output.output}"
    )
    cli_print.log_char_full_width("-")

    try:
        transformed_output = client.models.transform_output_model(
            stored_model.id, raw_model_output
        )
    except ApiError as error:
        if isinstance(error.error, ModelAdapterTransformationError):
            transformed_suffix = (
                f", {error.error.transformed}" if error.error.transformed else ""
            )
            raise cli_exc.CLIError(
                f"{error.error.message}{transformed_suffix}"
            ) from error
        raise

    if stored_model_adapter.process_output:
        cli_print.log_info(
            "Jinja output transform (from adapter "
            f"'{stored_model_adapter.display_name}'):\n"
            f"{stored_model_adapter.process_output.source_code}"
        )
        cli_print.log_char_full_width("-")

    cli_print.log_info(
        f"Model output in the format expected by LatticeFlow AI:\n{transformed_output}"
    )


def _get_test_model_input(
    model_input_path: Path | None, stored_model: StoredModel
) -> str:
    if model_input_path:
        if not model_input_path.is_file():
            raise cli_exc.CLIInvalidSingleFilePathError(model_input_path)

        return model_input_path.read_text()
    else:
        if (stored_model.modality, stored_model.task) == (
            Modality.TEXT,
            MLTask.CHAT_COMPLETION,
        ):
            return '{"messages": [{"role": "user", "content": "Hello!"}]}'

        raise cli_exc.CLIError(
            f"Model testing for modality '{stored_model.modality.value}' "
            f"and task '{stored_model.task.value}' "
            f"requires model input to be specified and passed with `--model-input`."
        )


def _create_inlined_model_adapter(
    client: Client, cli_model_adapter: CLICreateModelAdapter, config_file: Path
) -> StoredModelAdapter:
    try:
        cli_print.log_char_full_width("=")
        cli_print.log_detected_referenced_entity_info("model adapter")
        stored_model_adapters_filtered_by_key = (
            client.model_adapters.get_model_adapters(
                key=cli_model_adapter.key
            ).model_adapters
        )
        existing_stored_model_adapter = (
            stored_model_adapters_filtered_by_key[0]
            if stored_model_adapters_filtered_by_key
            else None
        )
        model_adapter = map_model_adapter_cli_to_api_entity(
            cli_model_adapter=cli_model_adapter, config_file=config_file
        )
        stored_model_adapter = model_adapter_cli.create_or_update_single_model_adapter(
            client, model_adapter, existing_stored_model_adapter
        )

        cli_print.log_char_full_width("=")
        return stored_model_adapter
    except Exception as error:
        raise cli_exc.CLICreateReferencedEntityError(
            PRETTY_ENTITY_NAME, "model adapter", config_file
        ) from error


def _map_inlined_model_adapter_to_key(
    cli_model: CLICreateModel, stored_model_adapter: StoredModelAdapter
) -> None:
    cli_model.adapter = UserOrLFKey(key=stored_model_adapter.key)


def create_or_update_single_model(
    client: Client, model: Model, stored_model: StoredModel | None
) -> StoredModel:
    if stored_model and is_update_payload_same_as_existing_entity(model, stored_model):
        cli_print.log_no_change_info(PRETTY_ENTITY_NAME, model.key)
        return stored_model
    elif stored_model:
        return update_single_model(client, stored_model, model)
    else:
        return create_single_model(client, model)


def update_single_model(
    client: Client, stored_model: StoredModel, model: Model
) -> StoredModel:
    return update_single_entity(
        PRETTY_ENTITY_NAME,
        lambda: client.models.update_model(stored_model.id, model),
        stored_model.key,
    )


def create_single_model(client: Client, model: Model) -> StoredModel:
    return create_single_entity(
        PRETTY_ENTITY_NAME, lambda: client.models.create_model(model), model.key
    )
