from datetime import datetime

from pydantic import BaseModel, Field

from revornix.schema.ai import ChatItem
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


class SearchSubscribedSectionRequest(SearchMineSectionsRequest):
    pass


class SearchPublicSectionsRequest(SearchMineSectionsRequest):
    pass


class SearchUserSectionsRequest(SearchMineSectionsRequest):
    user_id: int


class SectionAskRequest(BaseModel):
    section_id: int
    messages: list[ChatItem]
    enable_mcp: bool = False
    model_id: int | None = None
    assistant_chat_id: str | None = None


class GenerateSectionPodcastRequest(BaseModel):
    section_id: int
    engine_id: int | None = None


class GenerateSectionPptRequest(BaseModel):
    section_id: int
    model_id: int | None = None
    image_engine_id: int | None = None


class TriggerSectionProcessRequest(BaseModel):
    section_id: int
    model_id: int | None = None
    image_engine_id: int | None = None
    podcast_engine_id: int | None = None


class RetrySectionDocumentRequest(BaseModel):
    section_id: int
    document_id: int


class SectionPptSlide(BaseModel):
    id: str
    title: str
    summary: str
    prompt: str
    image_url: str | None = None


class SectionPptPreview(BaseModel):
    status: str
    title: str | None = None
    subtitle: str | None = None
    theme_prompt: str | None = None
    pptx_url: str | None = None
    error_message: str | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None
    slides: list[SectionPptSlide] = Field(default_factory=list)


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


class SectionCommentInfo(BaseModel):
    id: int
    content: str
    create_time: datetime
    update_time: datetime | None = None
    creator: UserPublicInfo
    parent_id: int | None = None
    root_id: int | None = None
    reply_user: UserPublicInfo | None = None
    like_count: int = 0
    liked: bool = False
    reply_count: int = 0
    preview_replies: list["SectionCommentInfo"] = Field(default_factory=list)


class SectionCommentCreateRequest(BaseModel):
    content: str
    section_id: int
    parent_id: int | None = None


class SectionCommentSearchRequest(BaseModel):
    section_id: int
    start: int | None = None
    limit: int = 10
    keyword: str | None = None
    sort: str = "time"
    preview_reply_limit: int = 2


class SectionCommentDeleteRequest(BaseModel):
    section_comment_ids: list[int]


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
    graph_stale: bool | None = None
    process_task_trigger_type: int | None = None
    process_task_trigger_scheduler: str | None = None
    is_day_section: bool = False
    day_section_date: str | None = None
    ppt_preview: SectionPptPreview | None = None


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
    is_public: bool | None = None
    auto_podcast: bool | None = None
    auto_illustration: bool | None = None
    process_task_trigger_type: int | None = None
    process_task_trigger_scheduler: str | None = None


class DaySectionRequest(BaseModel):
    date: str


class DaySectionResponse(BaseModel):
    section_id: int | None = None
    creator: UserPublicInfo | None = None
    date: str
    title: str | None = None
    description: str | None = None
    auto_podcast: bool = True
    auto_illustration: bool = True
    create_time: datetime | None = None
    update_time: datetime | None = None
    md_file_name: str | None = None
    documents: list[SectionDocumentInfo] = Field(default_factory=list)
    podcast_task: SectionPodcastTask | None = None
    process_task: SectionProcessTask | None = None
    process_task_trigger_type: int | None = None
    process_task_trigger_scheduler: str | None = None
    is_created: bool = True
