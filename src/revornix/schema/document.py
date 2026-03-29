from datetime import datetime

from pydantic import BaseModel, Field

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


class SearchAllMyDocumentsRequest(BaseModel):
    keyword: str | None = None
    start: int | None = None
    limit: int = 10
    label_ids: list[int] | None = None
    desc: bool = True


class DocumentDeleteRequest(BaseModel):
    document_ids: list[int]


class DocumentDetailRequest(BaseModel):
    document_id: int


class VectorSearchRequest(BaseModel):
    query: str


class WebsiteDocumentInfo(BaseModel):
    url: str


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
    labels: list[DocumentLabel] = Field(default_factory=list)
    creator: UserPublicInfo
    sections: list[BaseSectionInfo] = Field(default_factory=list)
    users: list[UserPublicInfo] = Field(default_factory=list)
    is_star: bool | None = None
    is_read: bool | None = None
    website_info: WebsiteDocumentInfo | None = None
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
