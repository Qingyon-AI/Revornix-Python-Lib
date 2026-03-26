from typing import Annotated

import typer

from revornix._cli.documents import app as documents_app
from revornix._cli.files import app as files_app
from revornix._cli.labels import app as labels_app
from revornix._cli.sections import app as sections_app
from revornix._cli.shared import AppConfig


app = typer.Typer(
    help="Command line interface for the Revornix API.",
    no_args_is_help=True,
)

app.add_typer(files_app, name="files")
app.add_typer(documents_app, name="documents")
app.add_typer(labels_app, name="labels")
app.add_typer(sections_app, name="sections")


@app.callback()
def main_callback(
    ctx: typer.Context,
    base_url: Annotated[
        str | None,
        typer.Option(
            "--base-url",
            help="Revornix API base URL.",
            envvar=["REVORNIX_BASE_URL", "REVORNIX_URL_PREFIX"],
        ),
    ] = None,
    api_key: Annotated[
        str | None,
        typer.Option(
            "--api-key",
            help="Revornix API key.",
            envvar=["REVORNIX_API_KEY", "API_KEY"],
        ),
    ] = None,
) -> None:
    ctx.obj = AppConfig(base_url=base_url, api_key=api_key)


def main() -> None:
    app()
