from typing import Optional, List

from src.schemas.users import GetUserSchema
from src.schemas.books import GetBooksSchema


class GetBooksSchemaRel(GetBooksSchema):
    """
    Book schema with relationship
    """
    author: GetUserSchema | None


class GetUserRelSchema(GetUserSchema):
    """
    User schema with relationship
    """
    book: List[Optional[GetBooksSchema]]