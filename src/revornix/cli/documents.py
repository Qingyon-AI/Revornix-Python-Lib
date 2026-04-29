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
    user_message,
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


@app.command("ask")
def ask_document(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    question: Annotated[str, typer.Option(..., "--question", help="Question to ask the document AI.")],
    enable_mcp: Annotated[bool, typer.Option("--enable-mcp")] = False,
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentAskRequest(
        document_id=document_id,
        messages=user_message(question),
        enable_mcp=enable_mcp,
        model_id=model_id,
    )
    handle_api_call(lambda: session.ask_document(payload))


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
    content: Annotated[str | None, typer.Option("--content")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentUpdateRequest(
        document_id=document_id,
        title=title,
        description=description,
        cover=cover,
        content=content,
        labels=optional_ids(labels),
        sections=optional_ids(sections),
    )
    handle_api_call(lambda: session.update_document(payload))


@app.command("delete")
def delete_document(
    ctx: typer.Context,
    document_ids: Annotated[
        list[int],
        typer.Option("--document-id", help="Document id. Repeat the option for multiple values."),
    ],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentDeleteRequest(document_ids=list(document_ids))
    handle_api_call(lambda: session.delete_document(payload))


def _search_request(
    labels: list[int] | None,
    keyword: str | None,
    start: int | None,
    limit: int,
    desc: str,
) -> DocumentSchema.SearchAllMyDocumentsRequest:
    return DocumentSchema.SearchAllMyDocumentsRequest(
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )


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
    payload = _search_request(labels, keyword, start, limit, desc)
    handle_api_call(lambda: session.search_mine_documents(payload))


@app.command("search-unread")
def search_unread_documents(
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
    payload = _search_request(labels, keyword, start, limit, desc)
    handle_api_call(lambda: session.search_unread_documents(payload))


@app.command("search-recent")
def search_recent_documents(
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
    payload = _search_request(labels, keyword, start, limit, desc)
    handle_api_call(lambda: session.search_recent_documents(payload))


@app.command("search-star")
def search_star_documents(
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
    payload = _search_request(labels, keyword, start, limit, desc)
    handle_api_call(lambda: session.search_star_documents(payload))


@app.command("search-vector")
def search_document_vector(
    ctx: typer.Context,
    query: Annotated[str, typer.Option(..., "--query", help="Semantic query text.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.VectorSearchRequest(query=query)
    handle_api_call(lambda: session.search_document_vector(payload))


@app.command("read")
def set_document_read_status(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    status: Annotated[str, typer.Option(..., "--status", help="Read status: true or false.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.ReadRequest(document_id=document_id, status=parse_bool(status))
    handle_api_call(lambda: session.set_document_read_status(payload))


@app.command("star")
def set_document_star_status(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    status: Annotated[str, typer.Option(..., "--status", help="Star status: true or false.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.StarRequest(document_id=document_id, status=parse_bool(status))
    handle_api_call(lambda: session.set_document_star_status(payload))


@app.command("create-note")
def create_document_note(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    content: Annotated[str, typer.Option(..., "--content", help="Note content.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentNoteCreateRequest(document_id=document_id, content=content)
    handle_api_call(lambda: session.create_document_note(payload))


@app.command("search-notes")
def search_document_notes(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    keyword: Annotated[str | None, typer.Option("--keyword")] = None,
    start: Annotated[int | None, typer.Option("--start")] = None,
    limit: Annotated[int, typer.Option("--limit")] = 10,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.SearchDocumentNoteRequest(
        document_id=document_id,
        keyword=keyword,
        start=start,
        limit=limit,
    )
    handle_api_call(lambda: session.search_document_notes(payload))


@app.command("delete-notes")
def delete_document_notes(
    ctx: typer.Context,
    note_ids: Annotated[
        list[int],
        typer.Option("--note-id", help="Document note id. Repeat the option for multiple values."),
    ],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentNoteDeleteRequest(document_note_ids=list(note_ids))
    handle_api_call(lambda: session.delete_document_notes(payload))


@app.command("summary")
def create_document_ai_summary(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentTaskRequest(document_id=document_id, model_id=model_id)
    handle_api_call(lambda: session.create_document_ai_summary(payload))


@app.command("embedding")
def create_document_embedding(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentTaskRequest(document_id=document_id, model_id=model_id)
    handle_api_call(lambda: session.create_document_embedding(payload))


@app.command("transcribe")
def transcribe_audio_document(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    engine_id: Annotated[int | None, typer.Option("--engine-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentEngineTaskRequest(document_id=document_id, engine_id=engine_id)
    handle_api_call(lambda: session.transcribe_audio_document(payload))


@app.command("generate-graph")
def generate_document_graph(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentTaskRequest(document_id=document_id, model_id=model_id)
    handle_api_call(lambda: session.generate_document_graph(payload))


@app.command("generate-podcast")
def generate_document_podcast(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
    engine_id: Annotated[int | None, typer.Option("--engine-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentEngineTaskRequest(document_id=document_id, engine_id=engine_id)
    handle_api_call(lambda: session.generate_document_podcast(payload))


@app.command("transform-markdown")
def transform_document_markdown(
    ctx: typer.Context,
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
) -> None:
    session = session_from_context(ctx)
    payload = DocumentSchema.DocumentMarkdownConvertRequest(document_id=document_id)
    handle_api_call(lambda: session.transform_document_markdown(payload))


@app.command("month-summary")
def get_document_month_summary(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.get_document_month_summary)
