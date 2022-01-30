from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.repository import user as user_repo
from blog.schemas import User, ShowUser

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=ShowUser)
async def create_user(request: User, db: Session = Depends(get_db)):
    return user_repo.create(request, db)


@router.get('/{id}', response_model=ShowUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} is not available')
    return user
