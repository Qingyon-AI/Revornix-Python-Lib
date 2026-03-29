import json
from typing import ClassVar

from click.testing import CliRunner
import revornix.schema.common as CommonSchema
import revornix.schema.document as DocumentSchema
import revornix.schema.section as SectionSchema
from typer.main import get_command

from revornix.cli import app


runner = CliRunner()
cli = get_command(app)


def test_create_quick_note_cli_uses_env_and_repeated_ids(monkeypatch):
    class DummySession:
        created_payload: ClassVar[DocumentSchema.QuickNoteDocumentParameters | None] = None
        base_url: ClassVar[str | None] = None
        api_key: ClassVar[str | None] = None

        def __init__(self, base_url: str, api_key: str):
            DummySession.base_url = base_url
            DummySession.api_key = api_key

        def create_quick_note_document(self, data):
            DummySession.created_payload = data
            return DocumentSchema.DocumentCreateResponse(document_id=123)

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "documents",
            "create-quick-note",
            "--content",
            "hello from cli",
            "--section",
            "1",
            "--section",
            "2",
            "--label",
            "9",
            "--auto-summary",
        ],
        env={
            "REVORNIX_BASE_URL": "https://api.example.com",
            "REVORNIX_API_KEY": "secret-token",
        },
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"document_id": 123}
    assert DummySession.base_url == "https://api.example.com"
    assert DummySession.api_key == "secret-token"
    assert DummySession.created_payload is not None
    assert DummySession.created_payload.content == "hello from cli"
    assert DummySession.created_payload.sections == [1, 2]
    assert DummySession.created_payload.labels == [9]
    assert DummySession.created_payload.auto_summary is True


def test_create_quick_note_cli_rejects_legacy_env_aliases():
    result = runner.invoke(
        cli,
        [
            "documents",
            "create-quick-note",
            "--content",
            "hello from cli",
        ],
        env={
            "REVORNIX_URL_PREFIX": "https://api.example.com",
            "API_KEY": "secret-token",
        },
    )

    assert result.exit_code == 2
    assert "Missing Revornix base URL. Use --base-url or REVORNIX_BASE_URL." in result.output


def test_upload_file_cli_passes_arguments(monkeypatch, tmp_path):
    class DummySession:
        upload_args: ClassVar[dict[str, str] | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def upload_file(self, local_file_path: str, remote_file_path: str, content_type: str):
            DummySession.upload_args = {
                "local_file_path": local_file_path,
                "remote_file_path": remote_file_path,
                "content_type": content_type,
            }
            return CommonSchema.NormalResponse()

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("demo", encoding="utf-8")

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "files",
            "upload",
            "--local-file-path",
            str(sample_file),
            "--remote-file-path",
            "uploads/sample.txt",
            "--content-type",
            "text/plain",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "success": True,
        "message": "Success",
    }
    assert DummySession.upload_args == {
        "local_file_path": str(sample_file.resolve()),
        "remote_file_path": "uploads/sample.txt",
        "content_type": "text/plain",
    }


def test_upload_create_file_cli_uploads_then_creates_document(monkeypatch, tmp_path):
    class DummySession:
        upload_args: ClassVar[dict[str, str] | None] = None
        created_payload: ClassVar[DocumentSchema.FileDocumentParameters | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def upload_file(self, local_file_path: str, remote_file_path: str, content_type: str):
            DummySession.upload_args = {
                "local_file_path": local_file_path,
                "remote_file_path": remote_file_path,
                "content_type": content_type,
            }
            return CommonSchema.NormalResponse()

        def create_file_document(self, data):
            DummySession.created_payload = data
            return DocumentSchema.DocumentCreateResponse(document_id=456)

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("demo", encoding="utf-8")

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "documents",
            "upload-create-file",
            "--local-file-path",
            str(sample_file),
            "--section",
            "1",
            "--label",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {
        "upload": {"success": True, "message": "Success"},
        "document": {"document_id": 456},
    }
    assert DummySession.upload_args == {
        "local_file_path": str(sample_file.resolve()),
        "remote_file_path": "sample.txt",
        "content_type": "text/plain",
    }
    assert DummySession.created_payload is not None
    assert DummySession.created_payload.file_name == "sample.txt"
    assert DummySession.created_payload.sections == [1]
    assert DummySession.created_payload.labels == [2]


def test_subcommand_help_does_not_require_credentials():
    result = runner.invoke(cli, ["documents", "create-quick-note", "--help"])

    assert result.exit_code == 0
    assert "--content" in result.stdout


def test_document_detail_cli_passes_document_id(monkeypatch):
    class DummySession:
        payload: ClassVar[DocumentSchema.DocumentDetailRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def get_document_detail(self, data):
            DummySession.payload = data
            return {"id": 7, "title": "Demo"}

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "documents",
            "detail",
            "--document-id",
            "7",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"id": 7, "title": "Demo"}
    assert DummySession.payload is not None
    assert DummySession.payload.document_id == 7


def test_delete_section_label_cli_passes_repeated_ids(monkeypatch):
    class DummySession:
        payload: ClassVar[SectionSchema.LabelDeleteRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def delete_section_label(self, data):
            DummySession.payload = data
            return CommonSchema.NormalResponse()

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "labels",
            "delete-section-labels",
            "--label-id",
            "1",
            "--label-id",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.label_ids == [1, 2]
    assert json.loads(result.stdout) == {"success": True, "message": "Success"}


def test_legacy_delete_section_label_alias_still_works(monkeypatch):
    class DummySession:
        payload: ClassVar[SectionSchema.LabelDeleteRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def delete_section_label(self, data):
            DummySession.payload = data
            return CommonSchema.NormalResponse()

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "labels",
            "delete-section",
            "--label-id",
            "3",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.label_ids == [3]


def test_search_mine_documents_cli_passes_filters(monkeypatch):
    class DummySession:
        payload: ClassVar[DocumentSchema.SearchAllMyDocumentsRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def search_mine_documents(self, data):
            DummySession.payload = data
            return {
                "total": 0,
                "start": 5,
                "limit": 20,
                "has_more": False,
                "elements": [],
                "next_start": None,
            }

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "documents",
            "search-mine",
            "--keyword",
            "notes",
            "--label",
            "9",
            "--label",
            "10",
            "--start",
            "5",
            "--limit",
            "20",
            "--desc",
            "false",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.keyword == "notes"
    assert DummySession.payload.label_ids == [9, 10]
    assert DummySession.payload.start == 5
    assert DummySession.payload.limit == 20
    assert DummySession.payload.desc is False


def test_search_document_vector_cli_passes_query(monkeypatch):
    class DummySession:
        payload: ClassVar[DocumentSchema.VectorSearchRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def search_document_vector(self, data):
            DummySession.payload = data
            return {"documents": [{"id": 8, "title": "Semantic Notes"}]}

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "documents",
            "search-vector",
            "--query",
            "semantic retrieval",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.query == "semantic retrieval"
    assert json.loads(result.stdout) == {"documents": [{"id": 8, "title": "Semantic Notes"}]}


def test_update_section_cli_passes_optional_fields(monkeypatch):
    class DummySession:
        payload: ClassVar[SectionSchema.SectionUpdateRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def update_section(self, data):
            DummySession.payload = data
            return CommonSchema.NormalResponse()

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "sections",
            "update",
            "--section-id",
            "12",
            "--title",
            "Updated Title",
            "--description",
            "Updated Description",
            "--label",
            "3",
            "--label",
            "4",
            "--auto-podcast",
            "true",
            "--auto-illustration",
            "false",
            "--process-task-trigger-type",
            "2",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.section_id == 12
    assert DummySession.payload.title == "Updated Title"
    assert DummySession.payload.description == "Updated Description"
    assert DummySession.payload.labels == [3, 4]
    assert DummySession.payload.auto_podcast is True
    assert DummySession.payload.auto_illustration is False
    assert DummySession.payload.process_task_trigger_type == 2


def test_publish_section_cli_passes_status(monkeypatch):
    class DummySession:
        payload: ClassVar[SectionSchema.SectionPublishRequest | None] = None

        def __init__(self, base_url: str, api_key: str):
            self.base_url = base_url
            self.api_key = api_key

        def publish_section(self, data):
            DummySession.payload = data
            return CommonSchema.NormalResponse()

    monkeypatch.setattr("revornix.cli.shared.Session", DummySession)

    result = runner.invoke(
        cli,
        [
            "--base-url",
            "https://api.example.com",
            "--api-key",
            "secret-token",
            "sections",
            "publish",
            "--section-id",
            "12",
            "--status",
            "true",
        ],
    )

    assert result.exit_code == 0
    assert DummySession.payload is not None
    assert DummySession.payload.section_id == 12
    assert DummySession.payload.status is True
