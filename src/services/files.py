import uuid
from typing import Type, Optional
from fastapi import UploadFile
from minio import Minio
from sqlalchemy.exc import DBAPIError, NoResultFound
from config import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_URL, BUCKET_NAME
from repositories.files import FilesRepository
from schemas.files import FileUploadResponse, FileDownloadResponse


class FileService:
    __instance = None

    def __init__(self, repo: Type[FilesRepository]):
        self.repo = repo()
        if self.__instance is None:
            self.__instance = Minio(MINIO_URL, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)

    async def upload_file(self, file: UploadFile) -> FileUploadResponse:
        file_id = str(uuid.uuid4())
        extension = file.filename.split('.')[-1]
        file_name = ".".join(file.filename.split(".")[:-1])
        self.__instance.put_object(
            BUCKET_NAME,
            data=file.file,
            object_name=f"{file_id}.{extension}",
            length=-1,
            content_type=file.content_type,
            part_size=10 * 1024 * 1024
        )
        await self.repo.add_file(file_id, file_name, extension)
        return FileUploadResponse(file_id=file_id, extension=file.filename.split('.')[-1], file_name=file_name)

    async def get_object(self, file_id: str) -> Optional[FileDownloadResponse]:
        try:
            file = await self.repo.get_file(file_id)
            url = self.__instance.presigned_get_object(
                bucket_name=BUCKET_NAME,
                object_name=file_id + "." + file.extension
            )
            return FileDownloadResponse(url=url, file_name=file.file_name, extension=file.extension)
        except (NoResultFound, DBAPIError):
            return None
