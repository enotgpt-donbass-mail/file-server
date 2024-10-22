from abc import abstractmethod
from typing import Any, Protocol, Callable

from sqlalchemy import func, insert, select, update, desc, asc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.base import ExecutableOption

from src.utils.exceptions import ResultNotFound

_sentinel: Any = object()


class AbstractRepository(Protocol):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = _sentinel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        try:
            return res.scalar_one()
        except NoResultFound:
            raise ResultNotFound

    async def edit_one(self, id: int, data: dict):
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        try:
            return res.unique().scalar_one()
        except NoResultFound:
            raise ResultNotFound

    async def find_all(self):
        stmt = select(self.model).options(*self.get_select_options())
        res = await self.session.execute(stmt)
        return res.unique().scalars().fetchall()

    async def find_filtered(self, **filter_by):
        stmt = (
            select(self.model)
            .options(*self.get_select_options())
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.unique().scalars().fetchall()

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .options(*self.get_select_options())
            .limit(1)
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        try:
            return res.unique().scalar_one()
        except NoResultFound:
            raise ResultNotFound

    async def count_filtered(self, **filter_by):
        stmt = (
            select(func.count())
            .select_from(self.model)
            .options(*self.get_select_options())
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        return res.scalar()

    async def delete_one(self, id: int) -> None:
        await self.session.delete((await self.find_one(id=id)))

    def get_select_options(self) -> list[ExecutableOption]:
        return []


# class SQLALchemyUserRepository(SQLAlchemyRepository):
#     async def authenticate(self, phone: str, password: str):
#         try:
#             user = await self.find_one(phone=phone)
#         except ResultNotFound:
#             raise WrongCredentials
#
#         if not checkpw(password.encode(), user.password.encode()):
#             raise WrongCredentials
#
#         return user
#
#     async def add_one(self, data: dict):
#         data["password"] = hashpw(data["password"].encode(), gensalt()).decode()
#         return await super().add_one(data)
#
#     async def edit_one(self, id: int, data: dict):
#         if "password" in data.keys():
#             data["password"] = hashpw(data["password"].encode(), gensalt()).decode()
#         return await super().edit_one(id, data)


class SQLAlchemyNewsContentsRepository(SQLAlchemyRepository):
    def get_select_options(self) -> list[ExecutableOption]:
        return [joinedload(self.model.contents)]

    async def select_with_pagination(self, page: int, limit: int, order_by: Callable[[Any], Any] = None, descending=True):
        offset = (page - 1) * limit
        stmt = select(self.model)

        if order_by is not None:
            stmt = stmt.order_by(desc(order_by)) if descending else stmt.order_by(asc(order_by))

        stmt = stmt.offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return res.unique().scalars().fetchall()

    async def count_items(self):
        stmt = (
            select(func.count())
            .select_from(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar()