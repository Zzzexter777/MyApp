from fastapi import APIRouter
from src.routers.users import router as user_router
from src.routers.books import router as book_router
from src.routers.setup_db import router as setup_db_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(book_router)
main_router.include_router(setup_db_router)