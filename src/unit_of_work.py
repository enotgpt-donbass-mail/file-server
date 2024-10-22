from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.models.base import Base
from src.adapters.database.repository_gateway import RepositoriesGateway
from src.adapters.database.session import async_session_maker, engine
from src.utils.repositories_gateway import RepositoriesGatewayProtocol
from src.utils.unit_of_work import UnitOfWorkProtocol


class UnitOfWork(UnitOfWorkProtocol):
    repositories: RepositoriesGatewayProtocol

    def __init__(self):
        self.db_session_factory = async_session_maker

    async def __aenter__(self):
        self.db_session = self.db_session_factory()

        self.repositories = RepositoriesGateway(self.db_session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.db_session.close()

    async def commit(self):
        await self.db_session.commit()

    async def rollback(self):
        await self.db_session.rollback()

    async def init_db(self) -> None:
        async with engine.begin() as connection:
            #await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)