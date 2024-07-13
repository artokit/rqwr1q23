from sqlalchemy import insert, select
from db.db import async_session_maker
from models.files import Files
from utils.repository import AbstractRepository


class FilesRepository(AbstractRepository):
    model = Files

    async def add_file(self, file_id: str, file_name: str, extension: str):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(
                id=file_id,
                file_name=file_name,
                extension=extension
            ).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()

    async def get_file(self, file_id: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == file_id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()
