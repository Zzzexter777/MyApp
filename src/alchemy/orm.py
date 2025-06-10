from fastapi import HTTPException
from sqlalchemy import select, desc, update, delete
from sqlalchemy.orm import selectinload
from starlette import status

from src.logs.logging import logger

from src.schemas.users import UserSchema, GetUserSchema
from src.schemas.books import BookCreateSchema, GetBooksSchema
from src.schemas.relationships import GetBooksSchemaRel, GetUserRelSchema

from src.database import async_session, async_engine
from src.models.models import Base, UserORM, BookORM

class AsyncORM:
    # --------------------------Tables--------------------------
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            # async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # --------------------------Users--------------------------
    @staticmethod
    async def insert_users(user: UserSchema):
        async with async_session() as session:
            new_user = UserORM(**user.model_dump())

            session.add(new_user)
            await session.commit()

            await session.refresh(new_user)

            created_user = GetUserSchema.model_validate(new_user, from_attributes=True)

            logger.info(f"User was added: {created_user}")
            return created_user

    @staticmethod
    async def find_user(user_id: int):
        async with async_session() as session:
            query = (
                select(UserORM)
                .where(UserORM.id == user_id)
            )

            result = await session.execute(query)

            found_user_orm = result.scalars().all()

            if len(found_user_orm) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            found_user_schema = [GetUserSchema.model_validate(row, from_attributes=True) for row in found_user_orm]
            logger.info(f"User was found: {found_user_schema}")
            return found_user_schema


    @staticmethod
    async def edit_user(user_id: int, user_new_data: UserSchema):
        async with async_session() as session:
            query = (
                update(UserORM)
                .where(UserORM.id == user_id)
                .values(**user_new_data.model_dump())
                .returning(UserORM)
            )

            result = await session.execute(query)

            edited_user = result.scalars().all()

            await session.commit()

            edited_user_schema = [GetUserSchema.model_validate(row, from_attributes=True) for row in edited_user]
            logger.info(f"User was edited, new data: {edited_user_schema}")
            return edited_user_schema

    @staticmethod
    async def delete_user(user_id: int):
        async with async_session() as session:
            user = await session.get(UserORM, user_id, options=[selectinload(UserORM.book)])

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



            await session.delete(user)
            await session.commit()

            deleted_user_schema = [GetUserSchema.model_validate(user, from_attributes=True)]
            logger.info(f"User was deleted: {deleted_user_schema}")
            return deleted_user_schema


    @staticmethod
    async def get_users_with_pag(page: int, limit: int):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(UserORM)
                .limit(limit)
                .offset(offset)
                .order_by(UserORM.id)
            )

            result = await session.execute(query)

            user_orm = result.scalars().all()

            if len(user_orm) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

            users_schema = [GetUserSchema.model_validate(row, from_attributes=True) for row in user_orm]

            logger.info(f"Received users: {users_schema}")
            return users_schema

    @staticmethod
    async def get_users_with_relationship_pag(page: int, limit: int):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(UserORM)
                .limit(limit)
                .offset(offset)
                .order_by(UserORM.id)
                .options(selectinload(UserORM.book))
            )

            result = await session.execute(query)

            user_orm = result.scalars().all()

            logger.info(f"Received users: {user_orm}")

            if len(user_orm) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

            users_schema = [GetUserRelSchema.model_validate(row, from_attributes=True) for row in user_orm]

            logger.info(f"Received users: {users_schema}")
            return users_schema

    # --------------------------Books--------------------------
    @staticmethod
    async def select_book(book_id: int):
        async with async_session() as session:
            query = (
                select(BookORM)
                .where(BookORM.id == book_id)
            )

            result = await session.execute(query)

            found_book_orm = result.scalars().all()

            if len(found_book_orm) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            found_user_schema = [GetUserSchema.model_validate(row, from_attributes=True) for row in found_user_orm]
            logger.info(f"User was found: {found_user_schema}")
            return found_user_schema

    @staticmethod
    async def insert_book(book: BookCreateSchema):
        async with async_session() as session:
            author_exists = await session.get(UserORM, book.author_id)
            if not author_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Author with id={book.author_id} not found"
                )

            new_book = BookORM(**book.model_dump())

            session.add(new_book)

            await session.commit()

            await session.refresh(new_book)

            created_book = GetBooksSchema.model_validate(new_book, from_attributes=True)

            logger.info(f"Book was added: {book}")
            return created_book


    @staticmethod
    async def get_books_with_relationship_pag(page: int, limit: int):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(BookORM)
                .limit(limit)
                .offset(offset)
                .order_by(BookORM.id)
                .options(selectinload(BookORM.author))
            )

            result = await session.execute(query)

            books_orm = result.scalars().all()
            if len(books_orm) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")

            books_schema = [GetBooksSchemaRel.model_validate(row, from_attributes=True) for row in books_orm]
            logger.info(f"Received books: {books_schema}")
            return books_schema