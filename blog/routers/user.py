import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog.database import engine, get_db
from blog.repository import user as user_repo
from blog.schemas import User, ShowUser

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=ShowUser
             )
async def create_user(request: User):
    async with engine.connect() as conn:
        return await user_repo.create(request, conn)


@router.get('/{id}', 
response_model=ShowUser
)
async def get_user(id: int):
    async with engine.connect() as conn:
        user = await user_repo.get(id, conn)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User with id {id} is not available')
        return user