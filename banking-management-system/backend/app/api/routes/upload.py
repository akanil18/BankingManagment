from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.upload import UploadResponse, ConfirmMappingRequest, MappingConfirmedResponse
from app.services.upload_service import UploadService

router = APIRouter()


@router.post("/file", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    table_name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await UploadService.upload_and_detect(file, table_name, current_user, db)


@router.post("/confirm-mapping", response_model=MappingConfirmedResponse)
async def confirm_mapping(
    payload: ConfirmMappingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await UploadService.confirm_mapping(payload, current_user, db)
