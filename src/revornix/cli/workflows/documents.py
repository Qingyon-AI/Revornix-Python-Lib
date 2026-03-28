import mimetypes
from pathlib import Path
from typing import Any

import revornix.schema.document as DocumentSchema
from revornix.session import Session


def guess_content_type(local_file_path: Path, explicit_content_type: str | None) -> str:
    if explicit_content_type:
        return explicit_content_type
    guessed, _ = mimetypes.guess_type(local_file_path.name)
    return guessed or "application/octet-stream"


def normalize_remote_file_path(local_file_path: Path, remote_file_path: str | None) -> str:
    return remote_file_path or local_file_path.name


def upload_and_create_file_document(
    session: Session,
    *,
    local_file_path: Path,
    remote_file_path: str | None,
    content_type: str | None,
    file_name: str | None,
    title: str | None,
    description: str | None,
    cover: str | None,
    sections: list[int],
    labels: list[int],
    auto_summary: bool,
    auto_podcast: bool,
    auto_tag: bool,
) -> dict[str, Any]:
    normalized_remote_file_path = normalize_remote_file_path(local_file_path, remote_file_path)
    normalized_content_type = guess_content_type(local_file_path, content_type)
    upload_result = session.upload_file(
        local_file_path=str(local_file_path),
        remote_file_path=normalized_remote_file_path,
        content_type=normalized_content_type,
    )
    document_result = session.create_file_document(
        DocumentSchema.FileDocumentParameters(
            title=title,
            description=description,
            cover=cover,
            sections=sections,
            labels=labels,
            file_name=file_name or normalized_remote_file_path,
            auto_summary=auto_summary,
            auto_podcast=auto_podcast,
            auto_tag=auto_tag,
        )
    )
    return {"upload": upload_result, "document": document_result}


def upload_and_create_audio_document(
    session: Session,
    *,
    local_file_path: Path,
    remote_file_path: str | None,
    content_type: str | None,
    file_name: str | None,
    title: str | None,
    description: str | None,
    cover: str | None,
    sections: list[int],
    labels: list[int],
    auto_summary: bool,
    auto_podcast: bool,
    auto_transcribe: bool,
    auto_tag: bool,
) -> dict[str, Any]:
    normalized_remote_file_path = normalize_remote_file_path(local_file_path, remote_file_path)
    normalized_content_type = guess_content_type(local_file_path, content_type)
    upload_result = session.upload_file(
        local_file_path=str(local_file_path),
        remote_file_path=normalized_remote_file_path,
        content_type=normalized_content_type,
    )
    document_result = session.create_audio_document(
        DocumentSchema.AudioDocumentParameters(
            title=title,
            description=description,
            cover=cover,
            sections=sections,
            labels=labels,
            file_name=file_name or normalized_remote_file_path,
            auto_summary=auto_summary,
            auto_podcast=auto_podcast,
            auto_transcribe=auto_transcribe,
            auto_tag=auto_tag,
        )
    )
    return {"upload": upload_result, "document": document_result}
