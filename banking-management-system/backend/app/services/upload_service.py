import uuid
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.uploaded_table import UploadedTable, UploadedRow
from app.models.field_mapping import FieldMapping
from app.schemas.upload import UploadResponse, ConfirmMappingRequest, MappingConfirmedResponse, FieldMappingItem
from app.utils.file_parser import FileParser
from app.services.mapping_service import MappingService
from app.core.exceptions import BadRequestException, NotFoundException, ForbiddenException
from sqlalchemy import select


class UploadService:

    @staticmethod
    async def upload_and_detect(
        file: UploadFile,
        table_name: str,
        user: User,
        db: AsyncSession,
    ) -> UploadResponse:
        content = await file.read()
        filename = file.filename or "upload"
        ext = filename.rsplit(".", 1)[-1].lower()

        if ext not in ["xlsx", "xls", "csv"]:
            raise BadRequestException(f"Unsupported file type: {ext}")

        df = FileParser.parse(content, ext)
        if df is None or df.empty:
            raise BadRequestException("File is empty or could not be parsed")

        detected_columns = list(df.columns)
        suggested_mappings = MappingService.suggest_mappings(detected_columns)

        table = UploadedTable(
            user_id=user.id,
            table_name=table_name,
            original_filename=filename,
            row_count=len(df),
        )
        db.add(table)
        await db.flush()

        # store raw rows temporarily (without confirmed mappings yet)
        for idx, row in df.iterrows():
            db.add(UploadedRow(
                table_id=table.id,
                user_id=user.id,
                row_data=row.to_dict(),
                row_index=int(idx),
            ))

        return UploadResponse(
            table_id=table.id,
            table_name=table_name,
            original_filename=filename,
            detected_columns=detected_columns,
            suggested_mappings=suggested_mappings,
            row_count=len(df),
        )

    @staticmethod
    async def confirm_mapping(
        payload: ConfirmMappingRequest,
        user: User,
        db: AsyncSession,
    ) -> MappingConfirmedResponse:
        result = await db.execute(
            select(UploadedTable).where(
                UploadedTable.id == payload.table_id,
                UploadedTable.user_id == user.id,
            )
        )
        table = result.scalar_one_or_none()
        if not table:
            raise NotFoundException("Table")

        for item in payload.mappings:
            db.add(FieldMapping(
                table_id=table.id,
                original_column=item.original_column,
                mapped_column=item.mapped_column,
            ))

        return MappingConfirmedResponse(
            table_id=table.id,
            message="Field mappings saved successfully",
            row_count=table.row_count,
        )
