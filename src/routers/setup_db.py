from fastapi import APIRouter
from src.alchemy.orm import AsyncORM

router = APIRouter(
    tags=["<Поднять щиты 🛡️>"]
)

@router.post(
    "/setup",
    summary="Удалить + Создать таблицы"
)
async def setup_db():
    await AsyncORM.create_tables()
    return {"ok": True}
