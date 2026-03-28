from typing import Annotated

import typer

import revornix.schema.document as DocumentSchema
import revornix.schema.section as SectionSchema
from revornix.cli.shared import handle_api_call, session_from_context


app = typer.Typer(help="Label operations.", no_args_is_help=True)


def _list_document_labels(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.get_mine_all_document_labels)


def _create_document_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Document label name.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.LabelAddRequest(name=name)
    handle_api_call(lambda: session.create_document_label(payload))


def _create_section_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Section label name.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.LabelAddRequest(name=name)
    handle_api_call(lambda: session.create_section_label(payload))


def _list_section_labels(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.get_mine_all_section_labels)


def _delete_document_labels(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Document label id. Repeat the option for multiple values."),
    ],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.LabelDeleteRequest(label_ids=list(label_ids))
    handle_api_call(lambda: session.delete_document_label(payload))


def _delete_section_labels(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Section label id. Repeat the option for multiple values."),
    ],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.LabelDeleteRequest(label_ids=list(label_ids))
    handle_api_call(lambda: session.delete_section_label(payload))


@app.command("list-document-labels")
def list_document_labels(ctx: typer.Context) -> None:
    _list_document_labels(ctx)


@app.command("create-document-label")
def create_document_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Document label name.")],
) -> None:
    _create_document_label(ctx, name)


@app.command("create-section-label")
def create_section_label(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Section label name.")],
) -> None:
    _create_section_label(ctx, name)


@app.command("list-section-labels")
def list_section_labels(ctx: typer.Context) -> None:
    _list_section_labels(ctx)


@app.command("delete-document-labels")
def delete_document_labels(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Document label id. Repeat the option for multiple values."),
    ],
) -> None:
    _delete_document_labels(ctx, label_ids)


@app.command("delete-section-labels")
def delete_section_labels(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Section label id. Repeat the option for multiple values."),
    ],
) -> None:
    _delete_section_labels(ctx, label_ids)


@app.command("list-document", hidden=True)
def list_document_labels_legacy(ctx: typer.Context) -> None:
    _list_document_labels(ctx)


@app.command("create-document", hidden=True)
def create_document_label_legacy(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Document label name.")],
) -> None:
    _create_document_label(ctx, name)


@app.command("create-section", hidden=True)
def create_section_label_legacy(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(..., "--name", help="Section label name.")],
) -> None:
    _create_section_label(ctx, name)


@app.command("list-section", hidden=True)
def list_section_labels_legacy(ctx: typer.Context) -> None:
    _list_section_labels(ctx)


@app.command("delete-document", hidden=True)
def delete_document_labels_legacy(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Document label id. Repeat the option for multiple values."),
    ],
) -> None:
    _delete_document_labels(ctx, label_ids)


@app.command("delete-section", hidden=True)
def delete_section_labels_legacy(
    ctx: typer.Context,
    label_ids: Annotated[
        list[int],
        typer.Option("--label-id", help="Section label id. Repeat the option for multiple values."),
    ],
) -> None:
    _delete_section_labels(ctx, label_ids)
