from fastapi import FastAPI
from src.routers import main_router
from src.database import async_engine

from sqladmin import Admin
from src.admin.sqladmin import UserAdmin, BookAdmin

app = FastAPI()

app.include_router(main_router)

admin = Admin(
    app=app,
    engine=async_engine,
    base_url="/myadmin",
)

admin.add_view(UserAdmin)
admin.add_view(BookAdmin)