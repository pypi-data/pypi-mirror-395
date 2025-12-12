from __future__ import annotations

import functools
import inspect
from typing import Any
from typing import Callable
from typing import cast

import typer

import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go import Client
from latticeflow.go.cli.utils.configuration import get_configuration_file
from latticeflow.go.cli.utils.configuration import upsert_configuration_file
from latticeflow.go.cli.utils.constants import LF_AIGO_URL_NAME
from latticeflow.go.cli.utils.constants import LF_API_KEY_NAME
from latticeflow.go.cli.utils.constants import LF_APP_KEY_CONTEXT_NAME
from latticeflow.go.cli.utils.constants import LF_VERIFY_SSL_NAME
from latticeflow.go.cli.utils.env_vars import get_cli_env_vars
from latticeflow.go.cli.utils.exceptions import CLIError
from latticeflow.go.cli.utils.helpers import app_callback
from latticeflow.go.cli.utils.helpers import get_client_from_env


def with_callback(
    cb: Callable[[], None],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            cb()
            return fn(*args, **kwargs)

        cast(Any, wrapped).__signature__ = inspect.signature(fn)
        return wrapped

    return deco


def register_workon_command(app: typer.Typer) -> None:
    app.command(
        name="workon",
        short_help="Set the AI app context for all AI-app-scoped entities",
        help=(
            "This command validates the AI app key by checking whether the "
            "AI app exists, and stores the AI app context in a configuration file "
            "(default location is '~/.latticeflow/config.json')."
        ),
    )(with_callback(lambda: app_callback(get_cli_env_vars))(_workon))


def _workon(
    ai_app_key: str = typer.Argument(
        ..., help="The key of the AI app in context.", envvar=LF_APP_KEY_CONTEXT_NAME
    ),
) -> None:
    client = get_client_from_env()
    try:
        client.ai_apps.get_ai_app_by_key(ai_app_key)
        config, config_file = get_configuration_file()
        config[LF_APP_KEY_CONTEXT_NAME] = ai_app_key
        upsert_configuration_file(config_file, config)
        cli_print.log_info(f"AI app context saved to '{config_file}'.")
    except Exception as error:
        raise CLIError(
            "Failed to set the AI app in context. Please check the AI app with "
            f"key '{ai_app_key}' exists and try again."
        ) from error


def register_configure_command(app: typer.Typer) -> None:
    app.command(
        name="configure",
        short_help="Configure AI GO! CLI options",
        help=(
            "This command validates and stores the CLI options into a configuration "
            "file (default location is '~/.latticeflow/config.json')."
        ),
    )(_configure)


def _configure(
    url: str = typer.Option(
        ...,
        help="URL to your AI GO! deployment.",
        prompt="Enter your AI GO! URL (e.g. 'https://aigo.myorg.com')",
        envvar=LF_AIGO_URL_NAME,
    ),
    api_key: str = typer.Option(
        ...,
        "--api-key",
        help="Your AI GO! API Key.",
        prompt="Enter your AI GO! API Key (e.g. '8421d0210751e999ce6b9e5759985346')",
        envvar=LF_API_KEY_NAME,
    ),
    verify_ssl: bool = typer.Option(
        True,
        "--verify-ssl/--no-verify-ssl",
        help="Flag whether to verify SSL certificates.",
        envvar=LF_VERIFY_SSL_NAME,
    ),
) -> None:
    try:
        client = Client(base_url=url, api_key=api_key, verify_ssl=verify_ssl)
        client.users.get_users()
        config, config_file = get_configuration_file()
        config[LF_AIGO_URL_NAME] = url
        config[LF_API_KEY_NAME] = api_key
        config[LF_VERIFY_SSL_NAME] = verify_ssl
        upsert_configuration_file(config_file, config)
        cli_print.log_info(f"CLI option saved to '{config_file}'.")
    except Exception as error:
        raise CLIError(
            f"Failed to connect to AI GO! at '{url}'. Please check your details and "
            f"try again."
        ) from error
