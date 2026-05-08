import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class FieldMapping(Base):
    __tablename__ = "field_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("uploaded_tables.id", ondelete="CASCADE"), nullable=False, index=True)
    original_column: Mapped[str] = mapped_column(String(255), nullable=False)
    mapped_column: Mapped[str] = mapped_column(String(255), nullable=False)

    table: Mapped["UploadedTable"] = relationship(back_populates="field_mappings")
