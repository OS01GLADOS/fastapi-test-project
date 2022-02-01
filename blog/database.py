from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLACHEMY_DATABASE_URL = 'sqlite:///./blog.db'

DB_HOST_SERVER = 'localhost'
DB_SERVER_PORT = '5432'
DB_DATABASE_NAME = 'postgres'
DB_USERNAME = 'username'
DB_PASSWORD = 'password'
POSTGRES_DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_SERVER}:{DB_SERVER_PORT}/{DB_DATABASE_NAME}'


engine = create_engine(POSTGRES_DB_URL)


SessionLocal = sessionmaker(bind=engine,
                            autocommit=False,
                            autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
