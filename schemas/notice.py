from pydantic import BaseModel

class NoticeBase(BaseModel):
    category: str
    status: str
    message: str

class NoticeCreate(NoticeBase):
    pass

class NoticeResponse(NoticeBase):
    id: int

    class Config:
        from_attributes = True

