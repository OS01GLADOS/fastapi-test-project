from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from blog.database import get_db
from blog.oauth2 import get_current_user
from blog.repository import blog as blog_repo
from blog.schemas import Blog, ShowBlog, User

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', response_model=List[ShowBlog])
def all(db: Session = Depends(get_db),
        get_current_user: User = Depends(get_current_user)):
    return blog_repo.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog,
           db: Session = Depends(get_db),
           get_current_user: User = Depends(get_current_user)
           ):
    user_mail = get_current_user.email
    return blog_repo.create(user_mail, request, db)


@router.get('/{id}',
            status_code=status.HTTP_200_OK,
            response_model=ShowBlog,
            )
def show(id: int,
         db: Session = Depends(get_db),
         get_current_user: User = Depends(get_current_user)):
    blog = blog_repo.get(id, db)
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
