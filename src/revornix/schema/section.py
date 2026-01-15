from pydantic import BaseModel

class LabelAddRequest(BaseModel):
    name: str
    
class BaseSectionInfo(BaseModel):
    id: int
    title: str
    description: str
        
class AllMySectionsResponse(BaseModel):
    data: list[BaseSectionInfo]
    
class SectionCreateRequest(BaseModel):
    title: str
    description: str
    cover: str | None = None
    labels: list[int]
    auto_publish: bool = False
    auto_podcast: bool = False
    auto_illustration: bool = False
    process_task_trigger_type: int
    process_task_trigger_scheduler: str | None = None
    
class SectionCreateResponse(BaseModel):
    id: int