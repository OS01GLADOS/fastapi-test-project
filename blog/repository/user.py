from sqlalchemy.orm import Session

from blog import models
from blog.hashing import Hash
from blog.schemas import User


def get(id: int, db: Session):
    user = db.query(models.User).get(id)
    if not user:
        return None
    return user

def create(request: User,db: Session):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user