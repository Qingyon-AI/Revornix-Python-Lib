from pathlib import Path
from typing import TypeVar

import httpx
from pydantic import BaseModel

import revornix.schema.common as CommonSchema
import revornix.schema.document as DocumentSchema
import revornix.schema.graph as GraphSchema
import revornix.schema.pagination as PaginationSchema
import revornix.schema.section as SectionSchema
from revornix.endpoints.document import DocumentApi
from revornix.endpoints.file import FileApi
from revornix.endpoints.graph import GraphApi
from revornix.endpoints.section import SectionApi


ResponseModelT = TypeVar("ResponseModelT", bound=BaseModel)


class Session:
    api_key: str
    base_url: str
    from_plat: str = "revornix python package"
    httpx_client: httpx.Client

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.httpx_client = httpx.Client(
            base_url=self.base_url,
            headers={"Api-Key": self.api_key},
            timeout=15.0,
        )

    def _post_json(
        self,
        endpoint: str,
        response_model: type[ResponseModelT],
        payload: BaseModel | dict | None = None,
    ) -> ResponseModelT:
        if payload is None:
            response = self.httpx_client.post(endpoint)
        else:
            json_payload = payload.model_dump(exclude_none=True) if isinstance(payload, BaseModel) else payload
            response = self.httpx_client.post(endpoint, json=json_payload)
        response.raise_for_status()
        return response_model.model_validate(response.json())

    def _post_json_raw(
        self,
        endpoint: str,
        payload: BaseModel | dict | None = None,
    ) -> dict:
        if payload is None:
            response = self.httpx_client.post(endpoint)
        else:
            json_payload = payload.model_dump(exclude_none=True) if isinstance(payload, BaseModel) else payload
            response = self.httpx_client.post(endpoint, json=json_payload)
        response.raise_for_status()
        return response.json()

    def _create_document(
        self,
        data: BaseModel,
        category: int,
    ) -> DocumentSchema.DocumentCreateResponse:
        payload = data.model_dump(exclude_none=True)
        payload["category"] = category
        payload["from_plat"] = self.from_plat
        return self._post_json(
            DocumentApi.create_document,
            DocumentSchema.DocumentCreateResponse,
            payload,
        )

    def upload_file(
        self,
        local_file_path: str,
        remote_file_path: str,
        content_type: str | None = "application/octet-stream",
    ) -> CommonSchema.NormalResponse:
        with open(local_file_path, "rb") as file_obj:
            files = {
                "file": (Path(local_file_path).name, file_obj, content_type),
            }
            data = {
                "file_path": remote_file_path,
                "content_type": content_type,
            }
            response = self.httpx_client.post(FileApi.upload_file, files=files, data=data)
            response.raise_for_status()
        return CommonSchema.NormalResponse.model_validate(response.json())

    def create_file_document(
        self,
        data: DocumentSchema.FileDocumentParameters,
    ) -> DocumentSchema.DocumentCreateResponse:
        return self._create_document(data, category=0)

    def create_website_document(
        self,
        data: DocumentSchema.WebsiteDocumentParameters,
    ) -> DocumentSchema.DocumentCreateResponse:
        return self._create_document(data, category=1)

    def create_quick_note_document(
        self,
        data: DocumentSchema.QuickNoteDocumentParameters,
    ) -> DocumentSchema.DocumentCreateResponse:
        return self._create_document(data, category=2)

    def create_audio_document(
        self,
        data: DocumentSchema.AudioDocumentParameters,
    ) -> DocumentSchema.DocumentCreateResponse:
        return self._create_document(data, category=3)

    def get_mine_all_document_labels(self) -> DocumentSchema.LabelListResponse:
        return self._post_json(
            DocumentApi.get_mine_all_document_labels,
            DocumentSchema.LabelListResponse,
        )

    def create_document_label(
        self,
        data: DocumentSchema.LabelAddRequest,
    ) -> DocumentSchema.CreateLabelResponse:
        return self._post_json(
            DocumentApi.create_document_label,
            DocumentSchema.CreateLabelResponse,
            data,
        )

    def delete_document_label(
        self,
        data: DocumentSchema.LabelDeleteRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            DocumentApi.delete_document_label,
            CommonSchema.NormalResponse,
            data,
        )

    def get_document_detail(
        self,
        data: DocumentSchema.DocumentDetailRequest,
    ) -> DocumentSchema.DocumentDetailResponse:
        return self._post_json(
            DocumentApi.get_document_detail,
            DocumentSchema.DocumentDetailResponse,
            data,
        )

    def ask_document(
        self,
        data: DocumentSchema.DocumentAskRequest,
    ) -> dict:
        return self._post_json_raw(DocumentApi.ask_document, data)

    def create_document_ai_summary(
        self,
        data: DocumentSchema.DocumentTaskRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.create_ai_summary, CommonSchema.NormalResponse, data)

    def create_document_embedding(
        self,
        data: DocumentSchema.DocumentTaskRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.create_embedding, CommonSchema.NormalResponse, data)

    def transcribe_audio_document(
        self,
        data: DocumentSchema.DocumentEngineTaskRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.transcribe_audio, CommonSchema.NormalResponse, data)

    def generate_document_graph(
        self,
        data: DocumentSchema.DocumentTaskRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.generate_graph, CommonSchema.NormalResponse, data)

    def generate_document_podcast(
        self,
        data: DocumentSchema.DocumentEngineTaskRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.generate_podcast, CommonSchema.NormalResponse, data)

    def get_document_month_summary(self) -> DocumentSchema.DocumentMonthSummaryResponse:
        return self._post_json(DocumentApi.month_summary, DocumentSchema.DocumentMonthSummaryResponse)

    def create_document_note(
        self,
        data: DocumentSchema.DocumentNoteCreateRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.create_note, CommonSchema.NormalResponse, data)

    def search_document_notes(
        self,
        data: DocumentSchema.SearchDocumentNoteRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentNoteInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentNoteInfo]
        return self._post_json(DocumentApi.search_notes, response_model, data)

    def delete_document_notes(
        self,
        data: DocumentSchema.DocumentNoteDeleteRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.delete_notes, CommonSchema.NormalResponse, data)

    def update_document(
        self,
        data: DocumentSchema.DocumentUpdateRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            DocumentApi.update_document,
            CommonSchema.NormalResponse,
            data,
        )

    def transform_document_markdown(
        self,
        data: DocumentSchema.DocumentMarkdownConvertRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.transform_markdown, CommonSchema.NormalResponse, data)

    def delete_document(
        self,
        data: DocumentSchema.DocumentDeleteRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            DocumentApi.delete_document,
            CommonSchema.NormalResponse,
            data,
        )

    def search_mine_documents(
        self,
        data: DocumentSchema.SearchAllMyDocumentsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]
        return self._post_json(
            DocumentApi.search_mine_documents,
            response_model,
            data,
        )

    def search_unread_documents(
        self,
        data: DocumentSchema.SearchAllMyDocumentsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]
        return self._post_json(DocumentApi.search_unread_documents, response_model, data)

    def search_recent_documents(
        self,
        data: DocumentSchema.SearchAllMyDocumentsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]
        return self._post_json(DocumentApi.search_recent_documents, response_model, data)

    def search_star_documents(
        self,
        data: DocumentSchema.SearchAllMyDocumentsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[DocumentSchema.DocumentInfo]
        return self._post_json(DocumentApi.search_star_documents, response_model, data)

    def search_document_vector(
        self,
        data: DocumentSchema.VectorSearchRequest,
    ) -> DocumentSchema.VectorSearchResponse:
        return self._post_json(
            DocumentApi.search_document_vector,
            DocumentSchema.VectorSearchResponse,
            data,
        )

    def set_document_read_status(
        self,
        data: DocumentSchema.ReadRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.read_document, CommonSchema.NormalResponse, data)

    def set_document_star_status(
        self,
        data: DocumentSchema.StarRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(DocumentApi.star_document, CommonSchema.NormalResponse, data)

    def create_section_label(
        self,
        data: SectionSchema.LabelAddRequest,
    ) -> SectionSchema.CreateLabelResponse:
        return self._post_json(
            SectionApi.create_section_label,
            SectionSchema.CreateLabelResponse,
            data,
        )

    def get_mine_all_section_labels(self) -> SectionSchema.LabelListResponse:
        return self._post_json(
            SectionApi.get_mine_all_section_labels,
            SectionSchema.LabelListResponse,
        )

    def delete_section_label(
        self,
        data: SectionSchema.LabelDeleteRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            SectionApi.delete_section_label,
            CommonSchema.NormalResponse,
            data,
        )

    def create_section(
        self,
        data: SectionSchema.SectionCreateRequest,
    ) -> SectionSchema.SectionCreateResponse:
        return self._post_json(
            SectionApi.create_section,
            SectionSchema.SectionCreateResponse,
            data,
        )

    def update_section(
        self,
        data: SectionSchema.SectionUpdateRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            SectionApi.update_section,
            CommonSchema.NormalResponse,
            data,
        )

    def delete_section(
        self,
        data: SectionSchema.SectionDeleteRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            SectionApi.delete_section,
            CommonSchema.NormalResponse,
            data,
        )

    def get_section_detail(
        self,
        data: SectionSchema.SectionDetailRequest,
    ) -> SectionSchema.SectionInfo:
        return self._post_json(
            SectionApi.get_section_detail,
            SectionSchema.SectionInfo,
            data,
        )

    def get_section_documents(
        self,
        data: SectionSchema.SectionDocumentRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionDocumentInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionDocumentInfo]
        return self._post_json(
            SectionApi.get_section_documents,
            response_model,
            data,
        )

    def ask_section(
        self,
        data: SectionSchema.SectionAskRequest,
    ) -> dict:
        return self._post_json_raw(SectionApi.ask_section, data)

    def get_mine_all_sections(self) -> SectionSchema.AllMySectionsResponse:
        return self._post_json(
            SectionApi.get_mine_all_section,
            SectionSchema.AllMySectionsResponse,
        )

    def search_mine_sections(
        self,
        data: SectionSchema.SearchMineSectionsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]
        return self._post_json(
            SectionApi.search_mine_sections,
            response_model,
            data,
        )

    def search_subscribed_sections(
        self,
        data: SectionSchema.SearchSubscribedSectionRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]
        return self._post_json(SectionApi.search_subscribed_sections, response_model, data)

    def search_public_sections(
        self,
        data: SectionSchema.SearchPublicSectionsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]
        return self._post_json(SectionApi.search_public_sections, response_model, data)

    def search_user_sections(
        self,
        data: SectionSchema.SearchUserSectionsRequest,
    ) -> PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]:
        response_model = PaginationSchema.InfiniteScrollPagination[SectionSchema.SectionInfo]
        return self._post_json(SectionApi.search_user_sections, response_model, data)

    def generate_section_podcast(
        self,
        data: SectionSchema.GenerateSectionPodcastRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(SectionApi.generate_podcast, CommonSchema.NormalResponse, data)

    def generate_section_ppt(
        self,
        data: SectionSchema.GenerateSectionPptRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(SectionApi.generate_ppt, CommonSchema.NormalResponse, data)

    def trigger_section_process(
        self,
        data: SectionSchema.TriggerSectionProcessRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(SectionApi.trigger_process, CommonSchema.NormalResponse, data)

    def retry_section_document(
        self,
        data: SectionSchema.RetrySectionDocumentRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(SectionApi.retry_document, CommonSchema.NormalResponse, data)

    def publish_section(
        self,
        data: SectionSchema.SectionPublishRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            SectionApi.publish_section,
            CommonSchema.NormalResponse,
            data,
        )

    def get_section_publish(
        self,
        data: SectionSchema.SectionPublishGetRequest,
    ) -> SectionSchema.SectionPublishGetResponse:
        return self._post_json(
            SectionApi.get_section_publish,
            SectionSchema.SectionPublishGetResponse,
            data,
        )

    def republish_section(
        self,
        data: SectionSchema.SectionRePublishRequest,
    ) -> CommonSchema.NormalResponse:
        return self._post_json(
            SectionApi.republish_section,
            CommonSchema.NormalResponse,
            data,
        )

    def search_graph(self) -> GraphSchema.GraphResponse:
        return self._post_json(GraphApi.search_graph, GraphSchema.GraphResponse)

    def search_document_graph(
        self,
        data: GraphSchema.DocumentGraphRequest,
    ) -> GraphSchema.GraphResponse:
        return self._post_json(GraphApi.document_graph, GraphSchema.GraphResponse, data)

    def search_section_graph(
        self,
        data: GraphSchema.SectionGraphRequest,
    ) -> GraphSchema.GraphResponse:
        return self._post_json(GraphApi.section_graph, GraphSchema.GraphResponse, data)
