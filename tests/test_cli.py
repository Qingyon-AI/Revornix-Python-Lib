import json

from click.testing import CliRunner
import revornix.schema.common as CommonSchema
import revornix.schema.document as DocumentSchema
from typer.main import get_command

from revornix.cli import app


runner = CliRunner()
cli = get_command(app)


def test_create_quick_note_cli_uses_env_and_repeated_ids(monkeypatch):
    class DummySession:
        created_payload = None
        base_url = None
        api_key = None

        def __init__(self, base_url: str, api_key: str):
            DummySession.base_url = base_url
            DummySession.api_key = api_key

        def create_quick_note_document(self, data):
            DummySession.created_payload = data
            return DocumentSchema.DocumentCreateResponse(document_id=123)

    monkeypatch.setattr("revornix._cli.shared.Session", DummySession)

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
            "REVORNIX_URL_PREFIX": "https://api.example.com",
            "API_KEY": "secret-token",
        },
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"document_id": 123}
    assert DummySession.base_url == "https://api.example.com"
    assert DummySession.api_key == "secret-token"
    assert DummySession.created_payload.content == "hello from cli"
    assert DummySession.created_payload.sections == [1, 2]
    assert DummySession.created_payload.labels == [9]
    assert DummySession.created_payload.auto_summary is True


def test_upload_file_cli_passes_arguments(monkeypatch, tmp_path):
    class DummySession:
        upload_args = None

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

    monkeypatch.setattr("revornix._cli.shared.Session", DummySession)

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


def test_subcommand_help_does_not_require_credentials():
    result = runner.invoke(cli, ["documents", "create-quick-note", "--help"])

    assert result.exit_code == 0
    assert "--content" in result.stdout
