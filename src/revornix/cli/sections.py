from typing import Annotated

import typer

import revornix.schema.section as SectionSchema
from revornix.cli.shared import (
    handle_api_call,
    normalize_ids,
    optional_ids,
    parse_bool,
    parse_optional_bool,
    session_from_context,
    user_message,
)


app = typer.Typer(help="Section operations.", no_args_is_help=True)


@app.command("list")
def list_sections(ctx: typer.Context) -> None:
    session = session_from_context(ctx)
    handle_api_call(session.get_mine_all_sections)


@app.command("create")
def create_section(
    ctx: typer.Context,
    title: Annotated[str, typer.Option(..., "--title", help="Section title.")],
    description: Annotated[
        str,
        typer.Option(..., "--description", help="Section description."),
    ],
    process_task_trigger_type: Annotated[
        int,
        typer.Option(
            ...,
            "--process-task-trigger-type",
            help="Revornix process task trigger type.",
        ),
    ],
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    process_task_trigger_scheduler: Annotated[
        str | None,
        typer.Option("--process-task-trigger-scheduler"),
    ] = None,
    auto_publish: Annotated[bool, typer.Option("--auto-publish")] = False,
    access_key: Annotated[
        str | None,
        typer.Option("--access-key", help="Optional access key when auto publishing."),
    ] = None,
    auto_podcast: Annotated[bool, typer.Option("--auto-podcast")] = False,
    auto_illustration: Annotated[bool, typer.Option("--auto-illustration")] = False,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionCreateRequest(
        title=title,
        description=description,
        cover=cover,
        labels=normalize_ids(labels),
        auto_publish=auto_publish,
        access_key=access_key,
        auto_podcast=auto_podcast,
        auto_illustration=auto_illustration,
        process_task_trigger_type=process_task_trigger_type,
        process_task_trigger_scheduler=process_task_trigger_scheduler,
    )
    handle_api_call(lambda: session.create_section(payload))


@app.command("detail")
def get_section_detail(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionDetailRequest(section_id=section_id)
    handle_api_call(lambda: session.get_section_detail(payload))


@app.command("date")
def get_section_date(
    ctx: typer.Context,
    date: Annotated[str, typer.Option(..., "--date", help="Day section date, formatted as YYYY-MM-DD.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.DaySectionRequest(date=date)
    handle_api_call(lambda: session.get_section_date(payload))


@app.command("documents")
def get_section_documents(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    keyword: Annotated[str | None, typer.Option("--keyword")] = None,
    start: Annotated[int | None, typer.Option("--start")] = None,
    limit: Annotated[int, typer.Option("--limit")] = 10,
    desc: Annotated[str, typer.Option("--desc", help="Sort descending: true or false.")] = "true",
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionDocumentRequest(
        section_id=section_id,
        keyword=keyword,
        start=start,
        limit=limit,
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.get_section_documents(payload))


@app.command("ask")
def ask_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    question: Annotated[str, typer.Option(..., "--question", help="Question to ask the section AI.")],
    enable_mcp: Annotated[bool, typer.Option("--enable-mcp")] = False,
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
    assistant_chat_id: Annotated[str | None, typer.Option("--assistant-chat-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionAskRequest(
        section_id=section_id,
        messages=user_message(question),
        enable_mcp=enable_mcp,
        model_id=model_id,
        assistant_chat_id=assistant_chat_id,
    )
    handle_api_call(lambda: session.ask_section(payload))


@app.command("create-comment")
def create_section_comment(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    content: Annotated[str, typer.Option(..., "--content", help="Comment content.")],
    parent_id: Annotated[int | None, typer.Option("--parent-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionCommentCreateRequest(
        section_id=section_id,
        content=content,
        parent_id=parent_id,
    )
    handle_api_call(lambda: session.create_section_comment(payload))


@app.command("search-comments")
def search_section_comments(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    keyword: Annotated[str | None, typer.Option("--keyword")] = None,
    start: Annotated[int | None, typer.Option("--start")] = None,
    limit: Annotated[int, typer.Option("--limit")] = 10,
    sort: Annotated[str, typer.Option("--sort", help="Sort mode: time or hot.")] = "time",
    preview_reply_limit: Annotated[int, typer.Option("--preview-reply-limit")] = 2,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionCommentSearchRequest(
        section_id=section_id,
        keyword=keyword,
        start=start,
        limit=limit,
        sort=sort,
        preview_reply_limit=preview_reply_limit,
    )
    handle_api_call(lambda: session.search_section_comments(payload))


@app.command("delete-comments")
def delete_section_comments(
    ctx: typer.Context,
    comment_ids: Annotated[
        list[int],
        typer.Option("--comment-id", help="Section comment id. Repeat the option for multiple values."),
    ],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionCommentDeleteRequest(section_comment_ids=list(comment_ids))
    handle_api_call(lambda: session.delete_section_comments(payload))


@app.command("search-mine")
def search_mine_sections(
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
    payload = SectionSchema.SearchMineSectionsRequest(
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.search_mine_sections(payload))


@app.command("search-subscribed")
def search_subscribed_sections(
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
    payload = SectionSchema.SearchSubscribedSectionRequest(
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.search_subscribed_sections(payload))


@app.command("search-public")
def search_public_sections(
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
    payload = SectionSchema.SearchPublicSectionsRequest(
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.search_public_sections(payload))


@app.command("search-user")
def search_user_sections(
    ctx: typer.Context,
    user_id: Annotated[int, typer.Option(..., "--user-id", help="User id.")],
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
    payload = SectionSchema.SearchUserSectionsRequest(
        user_id=user_id,
        keyword=keyword,
        start=start,
        limit=limit,
        label_ids=optional_ids(labels),
        desc=parse_bool(desc),
    )
    handle_api_call(lambda: session.search_user_sections(payload))


@app.command("update")
def update_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    labels: Annotated[
        list[int] | None,
        typer.Option("--label", help="Label id. Repeat the option for multiple values."),
    ] = None,
    title: Annotated[str | None, typer.Option("--title")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    cover: Annotated[str | None, typer.Option("--cover")] = None,
    is_public: Annotated[str | None, typer.Option("--is-public", help="Set public status to true or false.")] = None,
    auto_podcast: Annotated[
        str | None,
        typer.Option("--auto-podcast", help="Set auto podcast to true or false."),
    ] = None,
    auto_illustration: Annotated[
        str | None,
        typer.Option("--auto-illustration", help="Set auto illustration to true or false."),
    ] = None,
    process_task_trigger_type: Annotated[int | None, typer.Option("--process-task-trigger-type")] = None,
    process_task_trigger_scheduler: Annotated[
        str | None,
        typer.Option("--process-task-trigger-scheduler"),
    ] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionUpdateRequest(
        section_id=section_id,
        title=title,
        description=description,
        cover=cover,
        labels=optional_ids(labels),
        is_public=parse_optional_bool(is_public),
        auto_podcast=parse_optional_bool(auto_podcast),
        auto_illustration=parse_optional_bool(auto_illustration),
        process_task_trigger_type=process_task_trigger_type,
        process_task_trigger_scheduler=process_task_trigger_scheduler,
    )
    handle_api_call(lambda: session.update_section(payload))


@app.command("delete")
def delete_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionDeleteRequest(section_id=section_id)
    handle_api_call(lambda: session.delete_section(payload))


@app.command("publish")
def publish_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    status: Annotated[str, typer.Option(..., "--status", help="Publish status: true or false.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionPublishRequest(section_id=section_id, status=parse_bool(status))
    handle_api_call(lambda: session.publish_section(payload))


@app.command("get-publish")
def get_section_publish(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionPublishGetRequest(section_id=section_id)
    handle_api_call(lambda: session.get_section_publish(payload))


@app.command("set-publish-access-key")
def set_section_publish_access_key(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    access_key: Annotated[
        str | None,
        typer.Option("--access-key", help="Access key to set. Omit or pass blank to clear."),
    ] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionAccessKeyUpdateRequest(section_id=section_id, access_key=access_key)
    handle_api_call(lambda: session.update_section_publish_access_key(payload))


@app.command("republish")
def republish_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionRePublishRequest(section_id=section_id)
    handle_api_call(lambda: session.republish_section(payload))


@app.command("generate-podcast")
def generate_section_podcast(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    engine_id: Annotated[int | None, typer.Option("--engine-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.GenerateSectionPodcastRequest(section_id=section_id, engine_id=engine_id)
    handle_api_call(lambda: session.generate_section_podcast(payload))


@app.command("generate-ppt")
def generate_section_ppt(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
    image_engine_id: Annotated[int | None, typer.Option("--image-engine-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.GenerateSectionPptRequest(
        section_id=section_id,
        model_id=model_id,
        image_engine_id=image_engine_id,
    )
    handle_api_call(lambda: session.generate_section_ppt(payload))


@app.command("trigger-process")
def trigger_section_process(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    model_id: Annotated[int | None, typer.Option("--model-id")] = None,
    image_engine_id: Annotated[int | None, typer.Option("--image-engine-id")] = None,
    podcast_engine_id: Annotated[int | None, typer.Option("--podcast-engine-id")] = None,
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.TriggerSectionProcessRequest(
        section_id=section_id,
        model_id=model_id,
        image_engine_id=image_engine_id,
        podcast_engine_id=podcast_engine_id,
    )
    handle_api_call(lambda: session.trigger_section_process(payload))


@app.command("retry-document")
def retry_section_document(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
    document_id: Annotated[int, typer.Option(..., "--document-id", help="Document id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.RetrySectionDocumentRequest(section_id=section_id, document_id=document_id)
    handle_api_call(lambda: session.retry_section_document(payload))
