from typing import List

from fastapi import APIRouter, HTTPException, status
from src.schemas.books import BookCreateSchema, GetBooksSchema, BookBaseSchema
from src.alchemy.orm import AsyncORM

router = APIRouter(
    tags=["Книги 📚"]
)

@router.post(
    "/add-book",
    response_model=BookBaseSchema,
    summary="Add new book"
)
async def add_new_book(book: BookCreateSchema):
    created_book = await AsyncORM.insert_book(book)

    return created_book

@router.get(
    "/get-books",
    # response_model=List[GetUserSchema],
    summary="Get books with pagination and relationships"
)
async def get_books_pag(page: int = 1, limit: int = 10):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Page cannot be lower than 1")

    books = await AsyncORM.get_books_with_relationship_pag(page, limit)

    return books
