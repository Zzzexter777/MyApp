import asyncio
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from src.schemas.users import UserSchema, GetUserSchema, GetUserNoIdSchema
from src.alchemy.orm import AsyncORM
from src.schemas.relationships import GetUserRelSchema

router = APIRouter(
    tags=["Пользователи 👤"]
)

@router.get(
    "/get-users",
    response_model=List[GetUserNoIdSchema],
    summary="Get user with pagination"
)
async def get_users_pag(page: int = 1, limit: int = 10):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Page cannot be lower than 1")
    users = await AsyncORM.get_users_with_pag(page, limit)
    return users

@router.post(
    "/add-user",
    response_model=UserSchema,
    summary="Add new user"
)
async def add_new_user(user: UserSchema):
    created_user = await AsyncORM.insert_users(user)
    return created_user


@router.patch(
    "/edit-user",
    response_model=List[UserSchema],
    summary="Edit current user"
)
async def edit_current_user(user_id: int, user_new_data: UserSchema):
    await AsyncORM.find_user(user_id)

    edited_user = await AsyncORM.edit_user(user_id, user_new_data)

    return edited_user


@router.delete(
    "/delete-user",
    response_model=List[UserSchema],
    summary="Delete user"
)
async def delete_user(user_id: int) -> List[GetUserSchema]:
    await AsyncORM.find_user(user_id)

    deleted_user = await AsyncORM.delete_user(user_id)

    return deleted_user

@router.get(
    "/get-users-relationship",
    response_model=List[GetUserRelSchema],
    summary="Get users with relationship"
)
async def get_users_with_pag_and_relationship(page: int = 1, limit: int = 10):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Page cannot be lower than 1")

    users = await AsyncORM.get_users_with_relationship_pag(page, limit)

    return users