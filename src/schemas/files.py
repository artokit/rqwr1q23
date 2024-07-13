from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    extension: str


class FileSchema(BaseModel):
    id: str
    file_name: str
    extension: str


class FileDownloadResponse(BaseModel):
    url: str
    file_name: str
    extension: str
