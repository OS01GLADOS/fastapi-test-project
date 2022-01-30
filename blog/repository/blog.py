import email
from sqlalchemy.orm import Session

from blog import models
from blog.schemas import Blog, User


async def get(id: int, db: Session):
    blog = db.query(models.Blog).get(id)
    if not blog:
        return None
    return blog


async def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


async def create(user_mail: str, request: Blog, db: Session):
    blog_user = db.query(models.User).filter(models.User.email
                                             == user_mail).first()
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=blog_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


async def update(user_mail: str, id: int, request: Blog, db: Session):
    blog_user = db.query(models.User).filter(models.User.email
                                             == user_mail).first()
    blog = db.query(models.Blog).filter(models.Blog.id == id,
                                        models.Blog.author == blog_user)
    if not blog.first():
        return None
    blog.update(dict(request))
    db.commit()
    return True


async def delete(user_mail: str, id: int, db: Session):
    blog_user = db.query(models.User).filter(models.User.email
                                             == user_mail).first()
    blog = db.query(models.Blog).filter(models.Blog.id == id,
                                        models.Blog.author == blog_user)
    if not blog.first():
        return None
    blog.delete(synchronize_session=False)
    db.commit()
    return True
