#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import urllib.error
import urllib.request
import uuid
from pathlib import Path


CREATE_DOCUMENT_ENDPOINT = "/tp/document/create"
LIST_DOCUMENT_LABELS_ENDPOINT = "/tp/document/label/list"
CREATE_DOCUMENT_LABEL_ENDPOINT = "/tp/document/label/create"
DELETE_DOCUMENT_LABEL_ENDPOINT = "/tp/document/label/delete"
DOCUMENT_DETAIL_ENDPOINT = "/tp/document/detail"
UPDATE_DOCUMENT_ENDPOINT = "/tp/document/update"
SEARCH_MINE_DOCUMENTS_ENDPOINT = "/tp/document/search/mine"
SEARCH_DOCUMENT_VECTOR_ENDPOINT = "/tp/document/vector/search"

LIST_SECTIONS_ENDPOINT = "/tp/section/mine/all"
CREATE_SECTION_LABEL_ENDPOINT = "/tp/section/label/create"
LIST_SECTION_LABELS_ENDPOINT = "/tp/section/label/list"
DELETE_SECTION_LABEL_ENDPOINT = "/tp/section/label/delete"
CREATE_SECTION_ENDPOINT = "/tp/section/create"
UPDATE_SECTION_ENDPOINT = "/tp/section/update"
SECTION_DETAIL_ENDPOINT = "/tp/section/detail"
SECTION_DOCUMENTS_ENDPOINT = "/tp/section/documents"
SEARCH_MINE_SECTIONS_ENDPOINT = "/tp/section/mine/search"
PUBLISH_SECTION_ENDPOINT = "/tp/section/publish"
GET_SECTION_PUBLISH_ENDPOINT = "/tp/section/publish/get"
REPUBLISH_SECTION_ENDPOINT = "/tp/section/republish"

UPLOAD_FILE_ENDPOINT = "/tp/file/upload"


def env_or_none(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError("Expected a boolean value: true or false.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Revornix API helper for OpenClaw skills.")
    parser.add_argument("--base-url", default=None, help="Revornix API base URL.")
    parser.add_argument("--api-key", default=None, help="Revornix API key.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-sections", help="List all sections.")
    subparsers.add_parser("list-document-labels", help="List all document labels.")
    subparsers.add_parser("list-section-labels", help="List all section labels.")

    create_section_parser = subparsers.add_parser("create-section", help="Create a section.")
    create_section_parser.add_argument("--title", required=True)
    create_section_parser.add_argument("--description", required=True)
    create_section_parser.add_argument("--cover", default=None)
    create_section_parser.add_argument("--label", action="append", type=int, default=[])
    create_section_parser.add_argument("--auto-publish", action="store_true")
    create_section_parser.add_argument("--auto-podcast", action="store_true")
    create_section_parser.add_argument("--auto-illustration", action="store_true")
    create_section_parser.add_argument("--process-task-trigger-type", type=int, default=1)
    create_section_parser.add_argument("--process-task-trigger-scheduler", default=None)

    update_section_parser = subparsers.add_parser("update-section", help="Update a section.")
    update_section_parser.add_argument("--section-id", required=True, type=int)
    update_section_parser.add_argument("--title", default=None)
    update_section_parser.add_argument("--description", default=None)
    update_section_parser.add_argument("--cover", default=None)
    update_section_parser.add_argument("--label", action="append", type=int)
    update_section_parser.add_argument("--auto-podcast", type=parse_bool, default=None)
    update_section_parser.add_argument("--auto-illustration", type=parse_bool, default=None)
    update_section_parser.add_argument("--process-task-trigger-type", type=int, default=None)
    update_section_parser.add_argument("--process-task-trigger-scheduler", default=None)

    section_detail_parser = subparsers.add_parser("section-detail", help="Get section detail.")
    section_detail_parser.add_argument("--section-id", required=True, type=int)

    section_documents_parser = subparsers.add_parser("section-documents", help="List section documents.")
    section_documents_parser.add_argument("--section-id", required=True, type=int)
    section_documents_parser.add_argument("--start", type=int, default=None)
    section_documents_parser.add_argument("--limit", type=int, default=10)
    section_documents_parser.add_argument("--keyword", default=None)
    section_documents_parser.add_argument("--desc", type=parse_bool, default=True)

    search_mine_sections_parser = subparsers.add_parser(
        "search-mine-sections",
        help="Search my sections.",
    )
    search_mine_sections_parser.add_argument("--keyword", default=None)
    search_mine_sections_parser.add_argument("--start", type=int, default=None)
    search_mine_sections_parser.add_argument("--limit", type=int, default=10)
    search_mine_sections_parser.add_argument("--label", action="append", type=int)
    search_mine_sections_parser.add_argument("--desc", type=parse_bool, default=True)

    publish_section_parser = subparsers.add_parser("publish-section", help="Publish or unpublish a section.")
    publish_section_parser.add_argument("--section-id", required=True, type=int)
    publish_section_parser.add_argument("--status", required=True, type=parse_bool)

    get_section_publish_parser = subparsers.add_parser(
        "get-section-publish",
        help="Get section publish status.",
    )
    get_section_publish_parser.add_argument("--section-id", required=True, type=int)

    republish_section_parser = subparsers.add_parser("republish-section", help="Republish a section.")
    republish_section_parser.add_argument("--section-id", required=True, type=int)

    create_document_label_parser = subparsers.add_parser(
        "create-document-label",
        help="Create a document label.",
    )
    create_document_label_parser.add_argument("--name", required=True)

    create_section_label_parser = subparsers.add_parser(
        "create-section-label",
        help="Create a section label.",
    )
    create_section_label_parser.add_argument("--name", required=True)

    delete_document_label_parser = subparsers.add_parser(
        "delete-document-label",
        help="Delete document labels.",
    )
    delete_document_label_parser.add_argument("--label-id", action="append", type=int, required=True)

    delete_section_label_parser = subparsers.add_parser(
        "delete-section-label",
        help="Delete section labels.",
    )
    delete_section_label_parser.add_argument("--label-id", action="append", type=int, required=True)

    upload_file_parser = subparsers.add_parser("upload-file", help="Upload a local file.")
    upload_file_parser.add_argument("--local-file-path", required=True)
    upload_file_parser.add_argument("--remote-file-path", required=True)
    upload_file_parser.add_argument("--content-type", default=None)

    create_quick_note_parser = subparsers.add_parser(
        "create-quick-note",
        help="Create a quick note document.",
    )
    add_document_common_args(create_quick_note_parser)
    create_quick_note_parser.add_argument("--content", required=True)

    create_website_parser = subparsers.add_parser(
        "create-website-document",
        help="Create a website document.",
    )
    add_document_common_args(create_website_parser)
    create_website_parser.add_argument("--url", required=True)

    create_file_parser = subparsers.add_parser(
        "create-file-document",
        help="Create a file document from an existing uploaded file.",
    )
    add_document_common_args(create_file_parser)
    create_file_parser.add_argument("--file-name", required=True)

    create_audio_parser = subparsers.add_parser(
        "create-audio-document",
        help="Create an audio document from an existing uploaded file.",
    )
    add_document_common_args(create_audio_parser)
    create_audio_parser.add_argument("--file-name", required=True)
    create_audio_parser.add_argument("--auto-transcribe", action="store_true")

    document_detail_parser = subparsers.add_parser("document-detail", help="Get document detail.")
    document_detail_parser.add_argument("--document-id", required=True, type=int)

    update_document_parser = subparsers.add_parser("update-document", help="Update document metadata.")
    update_document_parser.add_argument("--document-id", required=True, type=int)
    update_document_parser.add_argument("--title", default=None)
    update_document_parser.add_argument("--description", default=None)
    update_document_parser.add_argument("--cover", default=None)
    update_document_parser.add_argument("--section", action="append", type=int)
    update_document_parser.add_argument("--label", action="append", type=int)

    search_mine_documents_parser = subparsers.add_parser(
        "search-mine-documents",
        help="Search my documents.",
    )
    search_mine_documents_parser.add_argument("--keyword", default=None)
    search_mine_documents_parser.add_argument("--start", type=int, default=None)
    search_mine_documents_parser.add_argument("--limit", type=int, default=10)
    search_mine_documents_parser.add_argument("--label", action="append", type=int)
    search_mine_documents_parser.add_argument("--desc", type=parse_bool, default=True)

    search_document_vector_parser = subparsers.add_parser(
        "search-document-vector",
        help="Run semantic vector search across my documents.",
    )
    search_document_vector_parser.add_argument("--query", required=True)

    upload_and_create_file_parser = subparsers.add_parser(
        "upload-and-create-file-document",
        help="Upload a local file and create a file document.",
    )
    add_upload_and_document_args(upload_and_create_file_parser)

    upload_and_create_audio_parser = subparsers.add_parser(
        "upload-and-create-audio-document",
        help="Upload a local audio file and create an audio document.",
    )
    add_upload_and_document_args(upload_and_create_audio_parser)
    upload_and_create_audio_parser.add_argument("--auto-transcribe", action="store_true")

    return parser.parse_args()


def add_document_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--title", default=None)
    parser.add_argument("--description", default=None)
    parser.add_argument("--cover", default=None)
    parser.add_argument("--section", action="append", type=int, default=[])
    parser.add_argument("--label", action="append", type=int, default=[])
    parser.add_argument("--auto-summary", action="store_true")
    parser.add_argument("--auto-podcast", action="store_true")
    parser.add_argument("--auto-tag", action="store_true")


def add_upload_and_document_args(parser: argparse.ArgumentParser) -> None:
    add_document_common_args(parser)
    parser.add_argument("--local-file-path", required=True)
    parser.add_argument("--remote-file-path", default=None)
    parser.add_argument("--content-type", default=None)
    parser.add_argument("--file-name", default=None)


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def resolve_config(args: argparse.Namespace) -> tuple[str, str]:
    base_url = args.base_url or env_or_none("REVORNIX_BASE_URL")
    api_key = args.api_key or env_or_none("REVORNIX_API_KEY")
    if not base_url:
        raise SystemExit("Missing Revornix base URL. Set REVORNIX_BASE_URL or pass --base-url.")
    if not api_key:
        raise SystemExit("Missing Revornix API key. Set REVORNIX_API_KEY or pass --api-key.")
    return normalize_base_url(base_url), api_key


def json_headers(api_key: str) -> dict[str, str]:
    return {
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }


def post_json(base_url: str, api_key: str, endpoint: str, payload: dict | None = None) -> dict:
    request = urllib.request.Request(
        url=f"{base_url}{endpoint}",
        data=json.dumps(payload or {}).encode("utf-8"),
        headers=json_headers(api_key),
        method="POST",
    )
    return execute_request(request)


def post_multipart(
    base_url: str,
    api_key: str,
    endpoint: str,
    fields: dict[str, str],
    file_field_name: str,
    file_name: str,
    file_bytes: bytes,
    content_type: str,
) -> dict:
    boundary = f"revornix-{uuid.uuid4().hex}"
    body = bytearray()

    for field_name, field_value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(field_value).encode("utf-8"))
        body.extend(b"\r\n")

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        (
            f'Content-Disposition: form-data; name="{file_field_name}"; '
            f'filename="{file_name}"\r\n'
        ).encode("utf-8")
    )
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        url=f"{base_url}{endpoint}",
        data=bytes(body),
        headers={
            "Api-Key": api_key,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    return execute_request(request)


def execute_request(request: urllib.request.Request) -> dict:
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} {exc.reason}\n{response_body}".strip()) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc


def print_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def guess_content_type(path: Path, explicit_content_type: str | None) -> str:
    if explicit_content_type:
        return explicit_content_type
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def upload_file(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    local_path = Path(args.local_file_path).expanduser().resolve()
    remote_file_path = args.remote_file_path or local_path.name
    content_type = guess_content_type(local_path, args.content_type)

    if not local_path.is_file():
        raise SystemExit(f"Local file not found: {local_path}")

    return post_multipart(
        base_url=base_url,
        api_key=api_key,
        endpoint=UPLOAD_FILE_ENDPOINT,
        fields={
            "file_path": remote_file_path,
            "content_type": content_type,
        },
        file_field_name="file",
        file_name=local_path.name,
        file_bytes=local_path.read_bytes(),
        content_type=content_type,
    )


def build_document_payload(args: argparse.Namespace, category: int) -> dict:
    payload = {
        "title": args.title,
        "description": args.description,
        "cover": args.cover,
        "sections": args.section,
        "labels": args.label,
        "auto_summary": args.auto_summary,
        "auto_podcast": args.auto_podcast,
        "auto_tag": args.auto_tag,
        "category": category,
        "from_plat": "openclaw skill",
    }
    return {key: value for key, value in payload.items() if value is not None}


def create_quick_note(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = build_document_payload(args, category=2)
    payload["content"] = args.content
    return post_json(base_url, api_key, CREATE_DOCUMENT_ENDPOINT, payload)


def create_website_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = build_document_payload(args, category=1)
    payload["url"] = args.url
    return post_json(base_url, api_key, CREATE_DOCUMENT_ENDPOINT, payload)


def create_file_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = build_document_payload(args, category=0)
    payload["file_name"] = args.file_name
    return post_json(base_url, api_key, CREATE_DOCUMENT_ENDPOINT, payload)


def create_audio_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = build_document_payload(args, category=3)
    payload["file_name"] = args.file_name
    payload["auto_transcribe"] = args.auto_transcribe
    return post_json(base_url, api_key, CREATE_DOCUMENT_ENDPOINT, payload)


def get_document_detail(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(base_url, api_key, DOCUMENT_DETAIL_ENDPOINT, {"document_id": args.document_id})


def update_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "document_id": args.document_id,
        "title": args.title,
        "description": args.description,
        "cover": args.cover,
        "sections": args.section,
        "labels": args.label,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, UPDATE_DOCUMENT_ENDPOINT, payload)


def search_mine_documents(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "keyword": args.keyword,
        "start": args.start,
        "limit": args.limit,
        "label_ids": args.label,
        "desc": args.desc,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, SEARCH_MINE_DOCUMENTS_ENDPOINT, payload)


def search_document_vector(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(
        base_url,
        api_key,
        SEARCH_DOCUMENT_VECTOR_ENDPOINT,
        {"query": args.query},
    )


def upload_and_create_file_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    local_path = Path(args.local_file_path).expanduser().resolve()
    remote_file_path = args.remote_file_path or local_path.name
    upload_args = argparse.Namespace(
        local_file_path=str(local_path),
        remote_file_path=remote_file_path,
        content_type=args.content_type,
    )
    upload_result = upload_file(base_url, api_key, upload_args)

    file_args = argparse.Namespace(**vars(args))
    file_args.file_name = args.file_name or remote_file_path
    document_result = create_file_document(base_url, api_key, file_args)
    return {"upload": upload_result, "document": document_result}


def upload_and_create_audio_document(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    local_path = Path(args.local_file_path).expanduser().resolve()
    remote_file_path = args.remote_file_path or local_path.name
    upload_args = argparse.Namespace(
        local_file_path=str(local_path),
        remote_file_path=remote_file_path,
        content_type=args.content_type,
    )
    upload_result = upload_file(base_url, api_key, upload_args)

    audio_args = argparse.Namespace(**vars(args))
    audio_args.file_name = args.file_name or remote_file_path
    document_result = create_audio_document(base_url, api_key, audio_args)
    return {"upload": upload_result, "document": document_result}


def create_section(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "title": args.title,
        "description": args.description,
        "cover": args.cover,
        "labels": args.label,
        "auto_publish": args.auto_publish,
        "auto_podcast": args.auto_podcast,
        "auto_illustration": args.auto_illustration,
        "process_task_trigger_type": args.process_task_trigger_type,
        "process_task_trigger_scheduler": args.process_task_trigger_scheduler,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, CREATE_SECTION_ENDPOINT, payload)


def update_section(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "section_id": args.section_id,
        "title": args.title,
        "description": args.description,
        "cover": args.cover,
        "labels": args.label,
        "auto_podcast": args.auto_podcast,
        "auto_illustration": args.auto_illustration,
        "process_task_trigger_type": args.process_task_trigger_type,
        "process_task_trigger_scheduler": args.process_task_trigger_scheduler,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, UPDATE_SECTION_ENDPOINT, payload)


def get_section_detail(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(base_url, api_key, SECTION_DETAIL_ENDPOINT, {"section_id": args.section_id})


def get_section_documents(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "section_id": args.section_id,
        "start": args.start,
        "limit": args.limit,
        "desc": args.desc,
        "keyword": args.keyword,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, SECTION_DOCUMENTS_ENDPOINT, payload)


def search_mine_sections(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    payload = {
        "keyword": args.keyword,
        "start": args.start,
        "limit": args.limit,
        "label_ids": args.label,
        "desc": args.desc,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    return post_json(base_url, api_key, SEARCH_MINE_SECTIONS_ENDPOINT, payload)


def publish_section(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(
        base_url,
        api_key,
        PUBLISH_SECTION_ENDPOINT,
        {"section_id": args.section_id, "status": args.status},
    )


def get_section_publish(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(
        base_url,
        api_key,
        GET_SECTION_PUBLISH_ENDPOINT,
        {"section_id": args.section_id},
    )


def republish_section(base_url: str, api_key: str, args: argparse.Namespace) -> dict:
    return post_json(
        base_url,
        api_key,
        REPUBLISH_SECTION_ENDPOINT,
        {"section_id": args.section_id},
    )


def create_named_resource(base_url: str, api_key: str, endpoint: str, name: str) -> dict:
    return post_json(base_url, api_key, endpoint, {"name": name})


def delete_labels(base_url: str, api_key: str, endpoint: str, label_ids: list[int]) -> dict:
    return post_json(base_url, api_key, endpoint, {"label_ids": label_ids})


def list_sections(base_url: str, api_key: str) -> dict:
    return post_json(base_url, api_key, LIST_SECTIONS_ENDPOINT)


def list_document_labels(base_url: str, api_key: str) -> dict:
    return post_json(base_url, api_key, LIST_DOCUMENT_LABELS_ENDPOINT)


def list_section_labels(base_url: str, api_key: str) -> dict:
    return post_json(base_url, api_key, LIST_SECTION_LABELS_ENDPOINT)


def main() -> None:
    args = parse_args()
    base_url, api_key = resolve_config(args)

    if args.command == "list-sections":
        result = list_sections(base_url, api_key)
    elif args.command == "list-document-labels":
        result = list_document_labels(base_url, api_key)
    elif args.command == "list-section-labels":
        result = list_section_labels(base_url, api_key)
    elif args.command == "create-section":
        result = create_section(base_url, api_key, args)
    elif args.command == "update-section":
        result = update_section(base_url, api_key, args)
    elif args.command == "section-detail":
        result = get_section_detail(base_url, api_key, args)
    elif args.command == "section-documents":
        result = get_section_documents(base_url, api_key, args)
    elif args.command == "search-mine-sections":
        result = search_mine_sections(base_url, api_key, args)
    elif args.command == "publish-section":
        result = publish_section(base_url, api_key, args)
    elif args.command == "get-section-publish":
        result = get_section_publish(base_url, api_key, args)
    elif args.command == "republish-section":
        result = republish_section(base_url, api_key, args)
    elif args.command == "create-document-label":
        result = create_named_resource(base_url, api_key, CREATE_DOCUMENT_LABEL_ENDPOINT, args.name)
    elif args.command == "create-section-label":
        result = create_named_resource(base_url, api_key, CREATE_SECTION_LABEL_ENDPOINT, args.name)
    elif args.command == "delete-document-label":
        result = delete_labels(base_url, api_key, DELETE_DOCUMENT_LABEL_ENDPOINT, args.label_id)
    elif args.command == "delete-section-label":
        result = delete_labels(base_url, api_key, DELETE_SECTION_LABEL_ENDPOINT, args.label_id)
    elif args.command == "upload-file":
        result = upload_file(base_url, api_key, args)
    elif args.command == "create-quick-note":
        result = create_quick_note(base_url, api_key, args)
    elif args.command == "create-website-document":
        result = create_website_document(base_url, api_key, args)
    elif args.command == "create-file-document":
        result = create_file_document(base_url, api_key, args)
    elif args.command == "create-audio-document":
        result = create_audio_document(base_url, api_key, args)
    elif args.command == "document-detail":
        result = get_document_detail(base_url, api_key, args)
    elif args.command == "update-document":
        result = update_document(base_url, api_key, args)
    elif args.command == "search-mine-documents":
        result = search_mine_documents(base_url, api_key, args)
    elif args.command == "search-document-vector":
        result = search_document_vector(base_url, api_key, args)
    elif args.command == "upload-and-create-file-document":
        result = upload_and_create_file_document(base_url, api_key, args)
    elif args.command == "upload-and-create-audio-document":
        result = upload_and_create_audio_document(base_url, api_key, args)
    else:
        raise SystemExit(f"Unknown command: {args.command}")

    print_json(result)


if __name__ == "__main__":
    main()
