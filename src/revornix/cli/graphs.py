from typing import Annotated

import typer

import revornix.schema.graph as GraphSchema
from revornix.cli.shared import handle_api_call, session_from_context


app = typer.Typer(help="Knowledge graph operations.", no_args_is_help=True)


@app.command("search")
def search_graph(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.search_graph)


@app.command("document")
def search_document_graph(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
) -> None:
    session = session_from_context(ctx)
    payload = GraphSchema.DocumentGraphRequest(document_id=document_id)
    handle_api_call(lambda: session.search_document_graph(payload))


@app.command("section")
def search_section_graph(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = GraphSchema.SectionGraphRequest(section_id=section_id)
    handle_api_call(lambda: session.search_section_graph(payload))
