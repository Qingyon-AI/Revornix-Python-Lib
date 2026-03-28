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
        auto_podcast=parse_optional_bool(auto_podcast),
        auto_illustration=parse_optional_bool(auto_illustration),
        process_task_trigger_type=process_task_trigger_type,
        process_task_trigger_scheduler=process_task_trigger_scheduler,
    )
    handle_api_call(lambda: session.update_section(payload))


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


@app.command("republish")
def republish_section(
    ctx: typer.Context,
    section_id: Annotated[int, typer.Option(..., "--section-id", help="Section id.")],
) -> None:
    session = session_from_context(ctx)
    payload = SectionSchema.SectionRePublishRequest(section_id=section_id)
    handle_api_call(lambda: session.republish_section(payload))
