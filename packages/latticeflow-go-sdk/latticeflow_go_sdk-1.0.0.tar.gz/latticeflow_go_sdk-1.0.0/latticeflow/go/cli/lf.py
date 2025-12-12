from __future__ import annotations

from pathlib import Path
from typing import Any

import click
import typer
from dotenv import load_dotenv

import latticeflow.go.cli.utils.printing as cli_print
from latticeflow.go.cli.ai_apps import ai_app_app
from latticeflow.go.cli.control_plane import tenant_app
from latticeflow.go.cli.dataset_generators import dataset_generator_app
from latticeflow.go.cli.datasets import dataset_app
from latticeflow.go.cli.evaluations import evaluation_app
from latticeflow.go.cli.integrations import integration_app
from latticeflow.go.cli.model_adapters import model_adapter_app
from latticeflow.go.cli.models import model_app
from latticeflow.go.cli.tasks import task_app
from latticeflow.go.cli.top_level_commands import register_configure_command
from latticeflow.go.cli.top_level_commands import register_workon_command
from latticeflow.go.cli.users import user_app
from latticeflow.go.cli.utils.exceptions import CLIError
from latticeflow.go.types import ApiError


load_dotenv(dotenv_path=Path.cwd() / ".env", verbose=True)
cli_print.configure_logging()


class SafeGroup(typer.core.TyperGroup):
    def invoke(self, ctx: click.Context) -> Any:
        try:
            return super().invoke(ctx)
        except click.ClickException:
            # NOTE: We let Click handle its own errors to pretty-print things like
            # missing or invalid arguments and params.
            raise
        except ApiError as api_error:
            cli_print.log_error(cli_print.summarize_exception_chain(api_error))
            raise typer.Exit(code=1)
        except CLIError as cli_error:
            cli_print.log_error(cli_print.summarize_exception_chain(cli_error))
            raise typer.Exit(code=1)
        except typer.Exit:
            # NOTE: typer raises exits with 0 status codes which
            # we just need to re-raise to make sure the operation
            # is handled successfully.
            raise
        except Exception as error:
            cli_print.log_error(str(error))
            raise typer.Exit(code=1)


CLI_HELP = """\
LatticeFlow AI GO! CLI

This CLI supports '.env' files. You can store any environment variables you deem 
necessary and leverage them in YAML config files, e.g. when creating or referencing 
other entities.
"""

app = typer.Typer(help=CLI_HELP, cls=SafeGroup, add_completion=False)

# Top-level commands
register_configure_command(app)
register_workon_command(app)

# High-level
app.add_typer(ai_app_app, name="app")
app.add_typer(evaluation_app, name="evaluation")

# Integrations
app.add_typer(model_app, name="model")
app.add_typer(model_adapter_app, name="model-adapter")

app.add_typer(dataset_app, name="dataset")
app.add_typer(dataset_generator_app, name="dataset-generator")

app.add_typer(task_app, name="task")

# Miscs
app.add_typer(user_app, name="user")
app.add_typer(integration_app, name="integration")
app.add_typer(tenant_app, name="tenant")

if __name__ == "__main__":
    app()
