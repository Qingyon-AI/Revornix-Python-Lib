from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from revornix.schema.ai import ChatItem
from revornix.schema.task import (
    DocumentConvertTask,
    DocumentEmbeddingTask,
    DocumentGraphTask,
    DocumentPodcastTask,
    DocumentProcessTask,
    DocumentSummarizeTask,
    DocumentTranscribeTask,
)
from revornix.schema.user import UserPublicInfo


class BaseSectionInfo(BaseModel):
    id: int
    title: str
    description: str | None = None
    publish_uuid: str | None = None


class DocumentLabel(BaseModel):
    id: int
    name: str


Label = DocumentLabel


class LabelListResponse(BaseModel):
    data: list[DocumentLabel]


class CreateLabelResponse(BaseModel):
    id: int
    name: str


class LabelAddRequest(BaseModel):
    name: str


class LabelDeleteRequest(BaseModel):
    label_ids: list[int]


class DocumentCreateResponse(BaseModel):
    document_id: int


class BaseDocumentParameters(BaseModel):
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    sections: list[int] = Field(default_factory=list)
    labels: list[int] = Field(default_factory=list)
    auto_summary: bool = False
    auto_podcast: bool = False
    auto_tag: bool = False


class FileDocumentParameters(BaseDocumentParameters):
    file_name: str | None = None


class WebsiteDocumentParameters(BaseDocumentParameters):
    url: str | None = None


class QuickNoteDocumentParameters(BaseDocumentParameters):
    content: str | None = None


class AudioDocumentParameters(BaseDocumentParameters):
    file_name: str | None = None
    auto_transcribe: bool = False


class DocumentUpdateRequest(BaseModel):
    document_id: int
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    labels: list[int] | None = None
    sections: list[int] | None = None
    content: str | None = None
    is_public: bool | None = None


class SearchAllMyDocumentsRequest(BaseModel):
    keyword: str | None = None
    start: int | None = None
    limit: int = 10
    label_ids: list[int] | None = None
    desc: bool = True


class DocumentDeleteRequest(BaseModel):
    document_ids: list[int]


class DocumentDetailRequest(BaseModel):
    document_id: int | None = None
    url: str | None = None

    @model_validator(mode="after")
    def validate_document_identifier(self):
        if self.document_id is None and (self.url is None or len(self.url.strip()) == 0):
            raise ValueError("Either document_id or url is required")
        return self


class VectorSearchRequest(BaseModel):
    query: str
    mode: str = "vector"
    limit: int = 10


class DocumentAskRequest(BaseModel):
    document_id: int
    messages: list[ChatItem]
    enable_mcp: bool = False
    model_id: int | None = None
    assistant_chat_id: str | None = None


class DocumentTaskRequest(BaseModel):
    document_id: int
    model_id: int | None = None


class DocumentEngineTaskRequest(BaseModel):
    document_id: int
    engine_id: int | None = None


class DocumentMarkdownConvertRequest(BaseModel):
    document_id: int


class DocumentPublishRequest(BaseModel):
    document_id: int
    status: bool


class DocumentPublishGetRequest(BaseModel):
    document_id: int


class DocumentPublishGetResponse(BaseModel):
    status: bool
    create_time: datetime | None = None
    update_time: datetime | None = None


class DocumentNoteCreateRequest(BaseModel):
    document_id: int
    content: str


class SearchDocumentNoteRequest(BaseModel):
    document_id: int
    keyword: str | None = None
    start: int | None = None
    limit: int = 10


class DocumentNoteDeleteRequest(BaseModel):
    document_note_ids: list[int]


class DocumentStatusRequest(BaseModel):
    document_id: int
    status: bool


ReadRequest = DocumentStatusRequest
StarRequest = DocumentStatusRequest


class WebsiteDocumentInfo(BaseModel):
    url: str
    latest_snapshot_time: datetime | None = None
    snapshot_count: int = 0


class WebsiteDocumentSnapshotInfo(BaseModel):
    id: int
    url: str
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    md_file_name: str | None = None
    create_time: datetime


class FileDocumentInfo(BaseModel):
    file_name: str


class QuickNoteDocumentInfo(BaseModel):
    content: str


class AudioDocumentInfo(BaseModel):
    audio_file_name: str


class DocumentInfo(BaseModel):
    id: int
    creator_id: int
    category: int
    title: str
    from_plat: str
    create_time: datetime
    update_time: datetime | None = None
    cover: str | None = None
    description: str | None = None
    labels: list[DocumentLabel] = Field(default_factory=list)
    sections: list[BaseSectionInfo] = Field(default_factory=list)
    users: list[UserPublicInfo] = Field(default_factory=list)
    convert_task: DocumentConvertTask | None = None
    embedding_task: DocumentEmbeddingTask | None = None
    graph_task: DocumentGraphTask | None = None
    podcast_task: DocumentPodcastTask | None = None
    summarize_task: DocumentSummarizeTask | None = None
    transcribe_task: DocumentTranscribeTask | None = None
    process_task: DocumentProcessTask | None = None


class DocumentDetailResponse(BaseModel):
    id: int
    category: int
    title: str
    from_plat: str
    description: str | None = None
    cover: str | None = None
    create_time: datetime
    update_time: datetime | None = None
    content_update_time: datetime | None = None
    labels: list[DocumentLabel] = Field(default_factory=list)
    creator: UserPublicInfo
    sections: list[BaseSectionInfo] = Field(default_factory=list)
    users: list[UserPublicInfo] = Field(default_factory=list)
    is_star: bool | None = None
    is_read: bool | None = None
    website_info: WebsiteDocumentInfo | None = None
    website_snapshots: list[WebsiteDocumentSnapshotInfo] = Field(default_factory=list)
    file_info: FileDocumentInfo | None = None
    quick_note_info: QuickNoteDocumentInfo | None = None
    audio_info: AudioDocumentInfo | None = None
    convert_task: DocumentConvertTask | None = None
    embedding_task: DocumentEmbeddingTask | None = None
    graph_task: DocumentGraphTask | None = None
    podcast_task: DocumentPodcastTask | None = None
    summarize_task: DocumentSummarizeTask | None = None
    transcribe_task: DocumentTranscribeTask | None = None
    process_task: DocumentProcessTask | None = None


class VectorSearchResponse(BaseModel):
    documents: list[DocumentInfo] = Field(default_factory=list)
    snippets: dict[int, str] = Field(default_factory=dict)


class DocumentNoteInfo(BaseModel):
    id: int
    content: str
    user: UserPublicInfo
    create_time: datetime
    update_time: datetime | None = None


class SummaryItem(BaseModel):
    date: str
    total: int


class DocumentMonthSummaryResponse(BaseModel):
    data: list[SummaryItem] = Field(default_factory=list)


class LabelSummaryItem(BaseModel):
    label_info: DocumentLabel
    count: int


class LabelSummaryResponse(BaseModel):
    data: list[LabelSummaryItem] = Field(default_factory=list)
