from datetime import datetime

from pydantic import BaseModel, Field

from revornix.schema.task import SectionPodcastTask, SectionProcessTask
from revornix.schema.user import UserPublicInfo


class LabelAddRequest(BaseModel):
    name: str


class LabelDeleteRequest(BaseModel):
    label_ids: list[int]


class SectionLabel(BaseModel):
    id: int
    name: str


Label = SectionLabel


class BaseSectionInfo(BaseModel):
    id: int
    title: str
    description: str | None = None
    authority: int | None = None
    publish_uuid: str | None = None


class AllMySectionsResponse(BaseModel):
    data: list[BaseSectionInfo]


class LabelListResponse(BaseModel):
    data: list[SectionLabel]


class CreateLabelResponse(BaseModel):
    id: int
    name: str


class SectionDocumentRequest(BaseModel):
    section_id: int
    start: int | None = None
    limit: int = 10
    desc: bool = True
    keyword: str | None = None


class SectionDetailRequest(BaseModel):
    section_id: int


class SectionDeleteRequest(BaseModel):
    section_id: int


class SearchMineSectionsRequest(BaseModel):
    keyword: str | None = None
    start: int | None = None
    limit: int = 10
    label_ids: list[int] | None = None
    desc: bool = True


class SectionPublishRequest(BaseModel):
    section_id: int
    status: bool


class SectionPublishGetRequest(BaseModel):
    section_id: int


class SectionPublishGetResponse(BaseModel):
    status: bool
    uuid: str | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None


class SectionRePublishRequest(BaseModel):
    section_id: int


class SectionDocumentInfo(BaseModel):
    id: int
    title: str
    status: int
    category: int
    cover: str | None = None
    description: str | None = None
    from_plat: str | None = None
    labels: list[SectionLabel] | None = None
    users: list[UserPublicInfo] | None = None
    create_time: datetime
    update_time: datetime | None = None


class SectionDocumentIntegrationSummary(BaseModel):
    wait_to_count: int = 0
    supplementing_count: int = 0
    success_count: int = 0
    failed_count: int = 0


class SectionInfo(BaseModel):
    id: int
    title: str
    creator: UserPublicInfo
    description: str
    auto_podcast: bool
    auto_illustration: bool
    documents_count: int = 0
    subscribers_count: int = 0
    create_time: datetime
    update_time: datetime | None = None
    authority: int | None = None
    is_subscribed: bool | None = None
    md_file_name: str | None = None
    labels: list[SectionLabel] | None = None
    cover: str | None = None
    publish_uuid: str | None = None
    podcast_task: SectionPodcastTask | None = None
    process_task: SectionProcessTask | None = None
    document_integration: SectionDocumentIntegrationSummary | None = None
    process_task_trigger_type: int | None = None
    process_task_trigger_scheduler: str | None = None


class SectionCreateRequest(BaseModel):
    title: str
    description: str
    cover: str | None = None
    labels: list[int] = Field(default_factory=list)
    auto_publish: bool = False
    auto_podcast: bool = False
    auto_illustration: bool = False
    process_task_trigger_type: int
    process_task_trigger_scheduler: str | None = None


class SectionCreateResponse(BaseModel):
    id: int


class SectionUpdateRequest(BaseModel):
    section_id: int
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    labels: list[int] | None = None
    auto_podcast: bool | None = None
    auto_illustration: bool | None = None
    process_task_trigger_type: int | None = None
    process_task_trigger_scheduler: str | None = None
