from services.files import FileService
from repositories.files import FilesRepository


def file_service() -> FileService:
    return FileService(FilesRepository)
