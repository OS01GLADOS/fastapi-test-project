from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from blog.database import engine, get_db 
from blog.oauth2 import get_current_user
from blog.repository import blog as blog_repo
from blog.schemas import Blog, ShowBlog, User

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', response_model=List[ShowBlog])
async def all(get_current_user: User = Depends(get_current_user)):
    async with engine.connect() as conn:
        return await blog_repo.get_all(conn)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(request: Blog,
            response_model=List[ShowBlog],
           get_current_user: User = Depends(get_current_user)
            ):
    async with engine.connect() as conn:
        user_mail = get_current_user.email
        return await blog_repo.create(user_mail, request, conn)


@router.get('/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ShowBlog,
            )
async def show(id: int,
         get_current_user: User = Depends(get_current_user)):
    async with engine.connect() as conn:
        blog = await blog_repo.get(id, conn)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Blog with the id {id} is not available')
        return blog


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int,
           request: Blog, db: Session = Depends(get_db),
           get_current_user: User = Depends(get_current_user)):
    user_mail = get_current_user.email
    blog = blog_repo.update(user_mail, id, request, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
    return 'updated'


@router.delete('/{id}',
               status_code=status.HTTP_204_NO_CONTENT,
               )
def destroy(id: int,
            db: Session = Depends(get_db),
            get_current_user: User = Depends(get_current_user)):
    user_mail = get_current_user.email
    res = blog_repo.delete(id, db)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
