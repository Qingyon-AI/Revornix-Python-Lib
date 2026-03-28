from pathlib import Path
from typing import Annotated

import typer

from revornix.cli.shared import handle_api_call, session_from_context


app = typer.Typer(help="File operations.", no_args_is_help=True)


@app.command("upload")
def upload_file(
    ctx: typer.Context,
    local_file_path: Annotated[
        Path,
        typer.Option(
            ...,
            "--local-file-path",
            help="Local file to upload.",
            exists=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    remote_file_path: Annotated[
        str,
        typer.Option(..., "--remote-file-path", help="Remote file path in Revornix."),
    ],
    content_type: Annotated[
        str,
        typer.Option("--content-type", help="Uploaded file content type."),
    ] = "application/octet-stream",
) -> None:
    session = session_from_context(ctx)
    handle_api_call(
        lambda: session.upload_file(
            local_file_path=str(local_file_path),
            remote_file_path=remote_file_path,
            content_type=content_type,
        )
    )
