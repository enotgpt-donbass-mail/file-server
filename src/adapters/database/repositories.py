from src.adapters.database.models.File import File
from src.utils.repository import SQLAlchemyRepository


class FileRepository(SQLAlchemyRepository):
    model = File

