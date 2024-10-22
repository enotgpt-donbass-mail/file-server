from abc import abstractmethod
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repositories import FileRepository


class RepositoriesGatewayProtocol(Protocol):
    file: FileRepository

    @abstractmethod
    def __init__(self, session: AsyncSession):
        raise NotImplementedError

