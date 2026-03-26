import json
from dataclasses import dataclass
from typing import Any

import httpx
import typer
from pydantic import BaseModel

from revornix.core import Session


@dataclass(slots=True)
class AppConfig:
    base_url: str | None
    api_key: str | None


def dump_output(payload: Any) -> None:
    if isinstance(payload, BaseModel):
        data = payload.model_dump(mode="json", exclude_none=True)
    else:
        data = payload
    typer.echo(json.dumps(data, ensure_ascii=False, indent=2))


def handle_api_call(callback: Any) -> None:
    try:
        dump_output(callback())
    except httpx.HTTPStatusError as exc:
        response_text = exc.response.text.strip() if exc.response is not None else ""
        message = response_text or str(exc)
        typer.secho(message, fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    except httpx.HTTPError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc


def session_from_context(ctx: typer.Context) -> Session:
    config = ctx.obj
    if not config.base_url:
        typer.secho(
            "Missing Revornix base URL. Use --base-url or REVORNIX_BASE_URL.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=2)
    if not config.api_key:
        typer.secho(
            "Missing Revornix API key. Use --api-key or REVORNIX_API_KEY.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=2)
    return Session(base_url=config.base_url, api_key=config.api_key)


def normalize_ids(values: list[int] | None) -> list[int]:
    return list(values or [])
