import uuid

from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.files import FileSchema


class Files(Base):
    __tablename__ = 'files'

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()),
                                    unique=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str] = mapped_column(String, nullable=False)

    def to_read_model(self) -> FileSchema:
        return FileSchema(
            id=str(self.id),
            file_name=self.file_name,
            extension=self.extension
        )
