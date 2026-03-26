from typing import Annotated

import typer

import revornix.schema.section as SectionSchema
from revornix._cli.shared import handle_api_call, normalize_ids, session_from_context


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
