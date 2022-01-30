from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLACHEMY_DATABASE_URL = 'sqlite:///./blog.db'


engine = create_engine(SQLACHEMY_DATABASE_URL,
                       connect_args={'check_same_thread': False})


SessionLocal = sessionmaker(bind=engine,
                            autocommit=False,
                            autoflush=False)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
