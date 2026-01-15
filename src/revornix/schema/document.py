from pydantic import BaseModel

class Label(BaseModel):
    id: int
    name: str

class LabelListResponse(BaseModel):
    data: list[Label]
    
class CreateLabelResponse(BaseModel):
    id: int
    name: str
    
class LabelAddRequest(BaseModel):
    name: str

class DocumentCreateResponse(BaseModel):
    document_id: int  
  
class FileDocumentParameters(BaseModel):
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    sections: list[int]
    labels: list[int]
    file_name: str | None = None
    auto_summary: bool = False
    auto_podcast: bool = False
    auto_tag: bool = False

class WebsiteDocumentParameters(BaseModel):
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    sections: list[int]
    labels: list[int]
    url: str | None = None
    auto_summary: bool = False
    auto_podcast: bool = False
    auto_tag: bool = False


class QuickNoteDocumentParameters(BaseModel):
    title: str | None = None
    description: str | None = None
    cover: str | None = None
    sections: list[int]
    labels: list[int]
    content: str | None = None
    auto_summary: bool = False
    auto_podcast: bool = False
    auto_tag: bool = False