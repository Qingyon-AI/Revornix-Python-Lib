import json
from dataclasses import dataclass
from typing import Any

import httpx
import typer
from pydantic import BaseModel

from revornix.session import Session


@dataclass(slots=True)
class AppConfig:
    base_url: str | None
    api_key: str | None


def _to_output_data(payload: Any) -> Any:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="json", exclude_none=True)
    if isinstance(payload, dict):
        return {key: _to_output_data(value) for key, value in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [_to_output_data(item) for item in payload]
    return payload


def dump_output(payload: Any) -> None:
    data = _to_output_data(payload)
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


def credentials_from_context(ctx: typer.Context) -> tuple[str, str]:
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
    return config.base_url, config.api_key


def session_from_context(ctx: typer.Context) -> Session:
    base_url, api_key = credentials_from_context(ctx)
    return Session(base_url=base_url, api_key=api_key)


def normalize_ids(values: list[int] | None) -> list[int]:
    return list(values or [])


def optional_ids(values: list[int] | None) -> list[int] | None:
    if values is None:
        return None
    return list(values)


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise typer.BadParameter("Expected a boolean value: true or false.")


def parse_optional_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return parse_bool(value)
