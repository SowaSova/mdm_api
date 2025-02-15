from typing import Optional

from sqlalchemy import Selectable, delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload

from src.core.exceptions import DatabaseErrorException


class SQLAlchemyRepository:
    model = None

    @classmethod
    async def find_one(cls, session: AsyncSession, **kwargs):
        query = select(cls.model)
        for field_name, field_value in kwargs.items():
            query = query.where(getattr(cls.model, field_name) == field_value)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none_with_relations(
        cls, session: AsyncSession, *relations: Mapped, **filter_by
    ):
        query = (
            select(cls.model)
            .filter_by(**filter_by)
            .options(*[joinedload(relation) for relation in relations])
        )
        result = await session.execute(query)
        return result.unique().scalars().one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_all_with_pagination(
        cls,
        session: AsyncSession,
        *relations: Mapped,
        skip: int = 0,
        limit: int = 10,
        **filter_by,
    ):
        result = await session.execute(
            select(cls.model)
            .filter_by(**filter_by)
            .options(*[joinedload(relation) for relation in relations])
            .offset(skip)
            .limit(limit)
        )
        return result.unique().scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            print("Database Exc: ", str(e))
            raise DatabaseErrorException

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        await session.execute(query)

    @classmethod
    async def add_bulk(cls, session: AsyncSession, *data):
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            result = await session.execute(query)
            return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            print("Database Exc: ", str(e))
            raise DatabaseErrorException

    @classmethod
    async def get_entities_with_relations(
        cls,
        session: AsyncSession,
        *relations: Mapped,
        skip: int = 0,
        limit: int = 10,
    ):
        result = await session.execute(
            select(cls.model)
            .options(*[joinedload(relation) for relation in relations])
            .offset(skip)
            .limit(limit)
        )
        return result.unique().scalars().all()

    @classmethod
    async def count(
        cls, session: AsyncSession, condition: Optional[Selectable] = None
    ) -> int:
        query = select(func.count()).select_from(cls.model.__table__)

        if condition is not None:
            query = query.where(condition)

        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def update(cls, session: AsyncSession, entity_id: int, **data):
        try:
            query = (
                update(cls.model)
                .where(cls.model.id == entity_id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
        except (SQLAlchemyError, Exception) as e:
            print("Database Exc: ", str(e))
            raise DatabaseErrorException
