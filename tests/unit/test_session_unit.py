from typing import cast

import httpx
import revornix.schema.document as DocumentSchema
import revornix.schema.section as SectionSchema
from revornix.session import Session


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class DummyClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def post(self, endpoint, json=None, files=None, data=None):
        self.calls.append(
            {
                "endpoint": endpoint,
                "json": json,
                "files": files,
                "data": data,
            }
        )
        return DummyResponse(self.responses[endpoint])


def test_search_mine_documents_posts_expected_payload_and_parses_pagination():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/document/search/mine": {
                "total": 1,
                "start": 0,
                "limit": 10,
                "has_more": False,
                "elements": [
                    {
                        "id": 1,
                        "creator_id": 2,
                        "category": 2,
                        "title": "hello",
                        "from_plat": "api",
                        "create_time": "2026-03-27T12:00:00",
                        "update_time": None,
                        "labels": [{"id": 10, "name": "research"}],
                        "sections": [{"id": 99, "title": "notes", "description": "demo"}],
                        "users": [],
                    }
                ],
                "next_start": None,
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.search_mine_documents(
        DocumentSchema.SearchAllMyDocumentsRequest(keyword="hello", start=0, label_ids=[10])
    )

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/document/search/mine",
            "json": {
                "keyword": "hello",
                "start": 0,
                "limit": 10,
                "label_ids": [10],
                "desc": True,
            },
            "files": None,
            "data": None,
        }
    ]
    assert result.total == 1
    assert result.elements[0].title == "hello"
    assert result.elements[0].labels[0].name == "research"
    assert result.elements[0].sections[0].id == 99


def test_get_section_detail_parses_nested_response():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/section/detail": {
                "id": 7,
                "title": "AI Notes",
                "creator": {
                    "id": 1,
                    "role": 1,
                    "avatar": "https://example.com/avatar.png",
                    "nickname": "kinda",
                    "slogan": "hello",
                },
                "description": "Knowledge base",
                "auto_podcast": False,
                "auto_illustration": True,
                "documents_count": 2,
                "subscribers_count": 3,
                "create_time": "2026-03-27T08:00:00",
                "update_time": "2026-03-27T09:00:00",
                "labels": [{"id": 5, "name": "tech"}],
                "cover": "cover.png",
                "publish_uuid": "pub-123",
                "podcast_task": {"status": 0, "podcast_file_name": None},
                "process_task": {"status": 1},
                "document_integration": {
                    "wait_to_count": 0,
                    "supplementing_count": 1,
                    "success_count": 2,
                    "failed_count": 0,
                },
                "process_task_trigger_type": 1,
                "process_task_trigger_scheduler": None,
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.get_section_detail(SectionSchema.SectionDetailRequest(section_id=7))

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/section/detail",
            "json": {"section_id": 7},
            "files": None,
            "data": None,
        }
    ]
    assert result.id == 7
    assert result.creator.nickname == "kinda"
    assert result.labels is not None
    assert result.labels[0].name == "tech"
    assert result.document_integration is not None
    assert result.document_integration.success_count == 2
    assert result.process_task is not None
    assert result.process_task.status == 1


def test_delete_document_posts_payload_and_returns_success_response():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/document/delete": {
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.delete_document(
        DocumentSchema.DocumentDeleteRequest(document_ids=[7, 8])
    )

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/document/delete",
            "json": {"document_ids": [7, 8]},
            "files": None,
            "data": None,
        }
    ]
    assert result.success is True
    assert result.code == 200


def test_delete_section_posts_payload_and_returns_success_response():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/section/delete": {
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.delete_section(
        SectionSchema.SectionDeleteRequest(section_id=12)
    )

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/section/delete",
            "json": {"section_id": 12},
            "files": None,
            "data": None,
        }
    ]
    assert result.success is True
    assert result.code == 200


def test_publish_section_posts_payload_and_returns_success_response():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/section/publish": {
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.publish_section(
        SectionSchema.SectionPublishRequest(section_id=7, status=True)
    )

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/section/publish",
            "json": {"section_id": 7, "status": True},
            "files": None,
            "data": None,
        }
    ]
    assert result.success is True
    assert result.code == 200


def test_search_document_vector_posts_query_and_parses_documents():
    session = Session(base_url="https://api.example.com", api_key="secret-token")
    dummy_client = DummyClient(
        {
            "/tp/document/vector/search": {
                "documents": [
                    {
                        "id": 1,
                        "creator_id": 2,
                        "category": 2,
                        "title": "Vector Search Note",
                        "from_plat": "api",
                        "create_time": "2026-03-27T12:00:00",
                        "update_time": None,
                        "labels": [{"id": 10, "name": "research"}],
                        "sections": [{"id": 99, "title": "notes", "description": "demo"}],
                        "users": [],
                    }
                ]
            }
        }
    )
    session.httpx_client = cast(httpx.Client, dummy_client)

    result = session.search_document_vector(
        DocumentSchema.VectorSearchRequest(query="semantic retrieval")
    )

    assert dummy_client.calls == [
        {
            "endpoint": "/tp/document/vector/search",
            "json": {"query": "semantic retrieval"},
            "files": None,
            "data": None,
        }
    ]
    assert len(result.documents) == 1
    assert result.documents[0].title == "Vector Search Note"
    assert result.documents[0].labels[0].name == "research"
