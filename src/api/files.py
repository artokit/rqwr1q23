from fastapi import APIRouter, UploadFile, Depends, HTTPException
from api.dependencies import file_service
from schemas.files import FileUploadResponse, FileDownloadResponse
from services.files import FileService

router = APIRouter(prefix="/api/files", tags=["files"])


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile, service: FileService = Depends(file_service)):
    return await service.upload_file(file)


@router.get("/{file_id}", response_model=FileDownloadResponse)
async def get_file(file_id: str, service: FileService = Depends(file_service)):
    res = await service.get_object(file_id)
    if res:
        return res

    raise HTTPException(status_code=404, detail="Файл не найден")
