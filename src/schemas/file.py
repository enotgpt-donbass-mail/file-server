from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SuccessResponse(BaseModel):
    status: bool = True
    model_config = ConfigDict(from_attributes=True)


class FileUploadOutput(SuccessResponse):
    url: str


class DataFile(BaseModel):
    id: int
    name: str
    hash: str
    create_date: datetime
    url: str

class AllFilesOutput(SuccessResponse):
    items: list["DataFile"]

