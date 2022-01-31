from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from blog import models
from blog.hashing import Hash
from blog.database import engine
from blog.token import create_access_token


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    async with engine.connect() as conn:
        # user = db.query(models.User).filter(models.User.email
        #                                     == request.username).first()
        query_res = await conn.execute(select(models.User)
                                  .where(models.User.email
                                         == request.username))
        user = query_res.first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Invalid credentials')
        if not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Invalid credentials')

        access_token = create_access_token(
            data={'sub': user.email},
        )
        return {'access_token': access_token, 'token_type': 'bearer'}
