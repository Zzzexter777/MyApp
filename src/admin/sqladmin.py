from sqladmin import ModelView

from src.models.models import UserORM, BookORM

class UserAdmin(ModelView, model=UserORM):
    form_excluded_columns = [UserORM.created_at, UserORM.updated_at]

    column_list = [UserORM.id, UserORM.name, UserORM.date_of_birth, UserORM.bio]
    can_create = True
    can_edit = True
    can_delete = True

class BookAdmin(ModelView, model=BookORM):
    form_excluded_columns = [BookORM.created_at, BookORM.updated_at]

    column_list = [BookORM.id, BookORM.name, BookORM.title, BookORM.author_id, BookORM.description]
    can_create = True
    can_edit = True
    can_delete = True
