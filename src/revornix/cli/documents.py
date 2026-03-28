from pathlib import Path
from typing import Annotated

import typer

import revornix.schema.document as DocumentSchema
from revornix.cli.shared import (
    handle_api_call,
    normalize_ids,
    optional_ids,
    parse_bool,
    session_from_context,
)
from revornix.cli.workflows.documents import (
    upload_and_create_audio_document as upload_and_create_audio_document_workflow,
    upload_and_create_file_document as upload_and_create_file_document_workflow,
)


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


@app.command("upload-create-file")
def upload_and_create_file_document(
    ctx: typer.Context,
    local_file_path: Annotated[
        Path,
        typer.Option(
            ...,
            "--local-file-path",
            help="Local file to upload before creating the document.",
            exists=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    remote_file_path: Annotated[
        str | None,
        typer.Option("--remote-file-path", help="Remote file path in Revornix. Defaults to local file name."),
    ] = None,
    file_name: Annotated[
        str | None,
        typer.Option("--file-name", help="Document file name in Revornix. Defaults to the remote file path."),
    ] = None,
    content_type: Annotated[
        str | None,
        typer.Option("--content-type", help="Uploaded file content type. Guessed from the local file if omitted."),
    ] = None,
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
    handle_api_call(
        lambda: upload_and_create_file_document_workflow(
            session,
            local_file_path=local_file_path,
            remote_file_path=remote_file_path,
            content_type=content_type,
            file_name=file_name,
            title=title,
            description=description,
            cover=cover,
            sections=normalize_ids(sections),
            labels=normalize_ids(labels),
            auto_summary=auto_summary,
            auto_podcast=auto_podcast,
            auto_tag=auto_tag,
        )
    )


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


@app.command("upload-create-audio")
def upload_and_create_audio_document(
    ctx: typer.Context,
    local_file_path: Annotated[
        Path,
        typer.Option(
            ...,
            "--local-file-path",
            help="Local audio file to upload before creating the document.",
            exists=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    remote_file_path: Annotated[
        str | None,
        typer.Option("--remote-file-path", help="Remote file path in Revornix. Defaults to local file name."),
    ] = None,
    file_name: Annotated[
        str | None,
        typer.Option("--file-name", help="Document file name in Revornix. Defaults to the remote file path."),
    ] = None,
    content_type: Annotated[
        str | None,
        typer.Option("--content-type", help="Uploaded file content type. Guessed from the local file if omitted."),
    ] = None,
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
    handle_api_call(
        lambda: upload_and_create_audio_document_workflow(
            session,
            local_file_path=local_file_path,
            remote_file_path=remote_file_path,
            content_type=content_type,
            file_name=file_name,
            title=title,
            description=description,
            cover=cover,
            sections=normalize_ids(sections),
            labels=normalize_ids(labels),
            auto_summary=auto_summary,
            auto_podcast=auto_podcast,
            auto_transcribe=auto_transcribe,
            auto_tag=auto_tag,
        )
    )


@app.command("detail")
def get_document_detail(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentDetailRequest(document_id=document_id)
    handle_api_call(lambda: session.get_document_detail(payload))


@app.command("update")
def update_document(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    sections: Annotated[
        list[int] | None,
        typer.Option("--section", help="Section id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentUpdateRequest(
        document_id=document_id,
        title=title,
        description=description,
        cover=cover,
        labels=optional_ids(labels),
        sections=optional_ids(sections),
    )
    handle_api_call(lambda: session.update_document(payload))


@app.command("search-mine")
def search_mine_documents(
    ctx: typer.Context,
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    keyword: Annotated[str | None, typer.Option("--keyword")] = None,
    start: Annotated[int | None, typer.Option("--start")] = None,
    limit: Annotated[int, typer.Option("--limit")] = 10,
    desc: Annotated[str, typer.Option("--desc", help="Sort descending: true or false.")] = "true",
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.SearchAllMyDocumentsRequest(
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.search_mine_documents(payload))
