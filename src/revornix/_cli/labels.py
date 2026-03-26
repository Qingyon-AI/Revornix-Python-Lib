from typing import Annotated

import typer

import revornix.schema.document as DocumentSchema
import revornix.schema.section as SectionSchema
from revornix._cli.shared import handle_api_call, session_from_context


app = typer.Typer(help="Label operations.", no_args_is_help=True)


@app.command("list-document")
def list_document_labels(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.get_mine_all_document_labels)


@app.command("create-document")
def create_document_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Document label name.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.LabelAddRequest(name=name)
    handle_api_call(lambda: session.create_document_label(payload))


@app.command("create-section")
def create_section_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Section label name.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.LabelAddRequest(name=name)
    handle_api_call(lambda: session.create_section_label(payload))
