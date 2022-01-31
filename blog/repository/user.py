import re
from sqlalchemy.orm import contains_eager

from sqlalchemy import insert, select, subquery
from sqlalchemy.ext.asyncio import AsyncSession
from blog import models
from blog.hashing import Hash
from blog.schemas import User


async def get(id: int, session: AsyncSession):
    query_res = await session.execute(select(models.User)
                                      .where(models.User.id == id))
    res = query_res.first()
    if not res:
        return None
    query_res = await session.execute(select(models.Blog)
                                      .where(models.Blog.user_id
                                             == id))
    blogs = query_res.all()
    res = dict(res)
    res['blogs'] = blogs
    return res


async def create(request: User, session: AsyncSession):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    session.execute(insert(models.User).values(
        name=request.name,
        email=request.email,
        password=hashed_password))
    await session.commit()
    query_res = await session.execute(select(models.User)
                                      .where(models.User.email
                                             == request.email))
    new_user = query_res.first()
    new_user = dict(new_user)
    new_user['blogs'] = []
    return new_user
