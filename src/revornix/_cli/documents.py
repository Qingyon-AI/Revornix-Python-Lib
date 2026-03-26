from typing import Annotated

import typer

import revornix.schema.document as DocumentSchema
from revornix._cli.shared import handle_api_call, normalize_ids, session_from_context


app = typer.Typer(help="Document operations.", no_args_is_help=True)


@app.command("create-file")
def create_file_document(
    ctx: typer.Context,
    file_name: Annotated[
        str,
        typer.Option(..., "--file-name", help="Uploaded file name in Revornix."),
    ],
    sections: Annotated[
        list[int] | None,
        typer.Option("--section", help="Section id. Repeat the option for multiple values."),
    ] = None,
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    auto_summary: Annotated[bool, typer.Option("--auto-summary")] = False,
    auto_podcast: Annotated[bool, typer.Option("--auto-podcast")] = False,
    auto_tag: Annotated[bool, typer.Option("--auto-tag")] = False,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.FileDocumentParameters(
        title=title,
        description=description,
        cover=cover,
        sections=normalize_ids(sections),
        labels=normalize_ids(labels),
        file_name=file_name,
        auto_summary=auto_summary,
        auto_podcast=auto_podcast,
        auto_tag=auto_tag,
    )
    handle_api_call(lambda: session.create_file_document(payload))


@app.command("create-website")
def create_website_document(
    ctx: typer.Context,
    url: Annotated[str, typer.Option(..., "--url", help="Website URL to import.")],
    sections: Annotated[
        list[int] | None,
        typer.Option("--section", help="Section id. Repeat the option for multiple values."),
    ] = None,
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    auto_summary: Annotated[bool, typer.Option("--auto-summary")] = False,
    auto_podcast: Annotated[bool, typer.Option("--auto-podcast")] = False,
    auto_tag: Annotated[bool, typer.Option("--auto-tag")] = False,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.WebsiteDocumentParameters(
        title=title,
        description=description,
        cover=cover,
        sections=normalize_ids(sections),
        labels=normalize_ids(labels),
        url=url,
        auto_summary=auto_summary,
        auto_podcast=auto_podcast,
        auto_tag=auto_tag,
    )
    handle_api_call(lambda: session.create_website_document(payload))


@app.command("create-quick-note")
def create_quick_note_document(
    ctx: typer.Context,
    content: Annotated[str, typer.Option(..., "--content", help="Quick note content.")],
    sections: Annotated[
        list[int] | None,
        typer.Option("--section", help="Section id. Repeat the option for multiple values."),
    ] = None,
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    auto_summary: Annotated[bool, typer.Option("--auto-summary")] = False,
    auto_podcast: Annotated[bool, typer.Option("--auto-podcast")] = False,
    auto_tag: Annotated[bool, typer.Option("--auto-tag")] = False,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.QuickNoteDocumentParameters(
        title=title,
        description=description,
        cover=cover,
        sections=normalize_ids(sections),
        labels=normalize_ids(labels),
        content=content,
        auto_summary=auto_summary,
        auto_podcast=auto_podcast,
        auto_tag=auto_tag,
    )
    handle_api_call(lambda: session.create_quick_note_document(payload))


@app.command("create-audio")
def create_audio_document(
    ctx: typer.Context,
    file_name: Annotated[
        str,
        typer.Option(..., "--file-name", help="Uploaded audio file name in Revornix."),
    ],
    sections: Annotated[
        list[int] | None,
        typer.Option("--section", help="Section id. Repeat the option for multiple values."),
    ] = None,
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    auto_summary: Annotated[bool, typer.Option("--auto-summary")] = False,
    auto_podcast: Annotated[bool, typer.Option("--auto-podcast")] = False,
    auto_transcribe: Annotated[bool, typer.Option("--auto-transcribe")] = False,
    auto_tag: Annotated[bool, typer.Option("--auto-tag")] = False,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.AudioDocumentParameters(
        title=title,
        description=description,
        cover=cover,
        sections=normalize_ids(sections),
        labels=normalize_ids(labels),
        file_name=file_name,
        auto_summary=auto_summary,
        auto_podcast=auto_podcast,
        auto_transcribe=auto_transcribe,
        auto_tag=auto_tag,
    )
    handle_api_call(lambda: session.create_audio_document(payload))
