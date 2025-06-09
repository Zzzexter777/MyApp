from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

class BookBaseSchema(BaseModel):
    name: Annotated[str, Field(..., max_length=84)]
    title: Annotated[Optional[str], Field(..., max_length=226)]
    description: Annotated[Optional[str], Field(..., max_length=1024)]

    class Config:
        from_attributes = True

class BookCreateSchema(BookBaseSchema):
    author_id: int


class GetBooksSchema(BookBaseSchema):
    id: int
    author_id: int | None
    created_at: datetime
    updated_at: datetime



