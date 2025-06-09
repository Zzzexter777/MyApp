from typing import Annotated, Optional, Any, Self

from pydantic import BaseModel, Field
from datetime import datetime, UTC

class UserSchema(BaseModel):
    name: Annotated[str, Field(..., max_length=126)]
    date_of_birth: datetime
    bio: Annotated[Optional[str], Field(..., max_length=1024)]

    class Config:
        from_attributes = True


class GetUserNoIdSchema(UserSchema):
    created_at: datetime
    updated_at: datetime


class GetUserSchema(UserSchema):
    id: int
    created_at: datetime
    updated_at: datetime

