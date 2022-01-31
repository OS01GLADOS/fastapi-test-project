from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog import models
from blog.hashing import Hash
from blog.schemas import User


async def get(id: int, session: AsyncSession):
    query_res = await session.execute(select(models.User).where(models.User.id == id))
    res = query_res.fetchone()
    if not res:
        return None
    return res

async def create(request: User,session: AsyncSession):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    print(new_user)
    return new_user