from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from blog import models
from blog.schemas import Blog


async def get(id: int, session: AsyncSession):
    query_res = await session.execute(
        select(models.Blog).where(models.Blog.id == id)
    )
    blog = query_res.first()
    if not blog:
        return None
    query_res = await session.execute(
        select(models.User.email, models.User.name).where(
            models.User.id == blog.user_id
        )
    )
    user = query_res.first()
    blog = dict(blog)
    blog['author'] = user
    return blog


async def get_all(session: AsyncSession):
    query_res = await session.execute(select(models.Blog))
    blogs = query_res.fetchall()
    res = []
    for item in blogs:
        query_res = await session.execute(
            select(models.User.email, models.User.name).where(
                models.User.id == item.user_id
            )
        )
        user = query_res.first()
        item = dict(item)
        item['author'] = user
        res.append(item)
    return res


async def create(user_mail: str, request: Blog, session: AsyncSession):
    query_res = await session.execute(
        select(models.User).where(models.User.email == user_mail)
    )
    blog_user = query_res.first()
    await session.execute(
        insert(models.Blog).values(
            title=request.title, body=request.body, user_id=blog_user.id
        )
    )
    await session.commit()
    query_res = await session.execute(
        select(models.Blog).where(
            models.Blog.title == request.title,
            models.Blog.user_id == blog_user.id,
        )
    )
    new_blog = query_res.first()
    new_blog = dict(new_blog)
    new_blog['author'] = blog_user
    return new_blog


async def change(
    user_mail: str, id: int, request: Blog, session: AsyncSession
):
    query_res = await session.execute(
        select(models.User).where(models.User.email == user_mail)
    )
    blog_user = query_res.first()
    query_res = await session.execute(
        select(models.Blog).where(
            models.Blog.id == id, models.Blog.user_id == blog_user.id
        )
    )
    blog = query_res.first()
    if not blog:
        return None
    query_res = await session.execute(
        update(models.Blog)
        .values(title=request.title, body=request.body)
        .where(models.Blog.id == id)
    )
    await session.commit()
    return True


async def destroy(user_mail: str, id: int, session: AsyncSession):
    query_res = await session.execute(
        select(models.User).where(models.User.email == user_mail)
    )
    blog_user = query_res.first()

    query_res = await session.execute(
        select(models.Blog).where(
            models.Blog.id == id, models.Blog.user_id == blog_user.id
        )
    )
    blog = query_res.first()
    if not blog:
        return None
    await session.execute(delete(models.Blog).where(models.Blog.id == id))
    await session.commit()
    return True
