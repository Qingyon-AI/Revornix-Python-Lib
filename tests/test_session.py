import os

import pytest
from dotenv import load_dotenv

load_dotenv(override=True)

import revornix.schema.document as DocumentSchema
import revornix.schema.section as SectionSchema
from revornix.core import Session


def _required_env(*names: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    pytest.skip(
        f"missing required environment variables: {', '.join(names)}",
        allow_module_level=True,
    )
    raise AssertionError("unreachable")


base_url = _required_env("REVORNIX_BASE_URL", "REVORNIX_URL_PREFIX")
api_key = _required_env("REVORNIX_API_KEY", "API_KEY")

session = Session(base_url=base_url, api_key=api_key)

def test_upload_text_file():
    res = session.upload_file(local_file_path="./tests/test.txt", remote_file_path="test.txt")
    assert res is not None

def test_upload_mp3_file():
    res = session.upload_file(local_file_path="./tests/test.mp3", remote_file_path="test.mp3")
    assert res is not None
    
def test_create_file_document():
    data = DocumentSchema.FileDocumentParameters(
        file_name="demo",
        sections=[],
        labels=[],
        auto_summary=False
    )
    res = session.create_file_document(data=data)
    assert res is not None

def test_create_audio_document():
    data = DocumentSchema.AudioDocumentParameters(
        file_name="test.mp3",
        sections=[],
        labels=[],
        auto_summary=False
    )
    res = session.create_audio_document(data=data)
    assert res is not None
    
def test_create_website_document():
    data = DocumentSchema.WebsiteDocumentParameters(
        url="https://www.google.com",
        sections=[],
        labels=[],
        auto_summary=False
    )
    res = session.create_website_document(data=data)
    assert res is not None
    
def test_create_quick_note_document():
    data = DocumentSchema.QuickNoteDocumentParameters(
        content="test",
        sections=[],
        labels=[],
        auto_summary=False
    )
    res = session.create_quick_note_document(data=data)
    assert res is not None
    
def test_create_document_label():
    data = DocumentSchema.LabelAddRequest(
        name="test"
    )
    res = session.create_document_label(data=data)
    assert res is not None
    
def test_create_section_label():
    data = SectionSchema.LabelAddRequest(
        name="test"
    )
    res = session.create_section_label(data=data)
    assert res is not None
    
def test_create_section():
    data = SectionSchema.SectionCreateRequest(
        title="test",
        description="test",
        auto_publish=False,
        cover='test.png',
        labels=[],
        process_task_trigger_type=1
    )
    res = session.create_section(data=data)
    assert res is not None

def test_get_mine_all_document_labels():
    res = session.get_mine_all_document_labels()
    assert res is not None
    
def test_get_mine_all_sections():
    res = session.get_mine_all_sections()
    assert res is not None
