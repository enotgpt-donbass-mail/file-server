from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repositories import FileRepository
from src.utils.repositories_gateway import RepositoriesGatewayProtocol


class RepositoriesGateway(RepositoriesGatewayProtocol):
    def __init__(self, session: AsyncSession):
        self.file = FileRepository(session)