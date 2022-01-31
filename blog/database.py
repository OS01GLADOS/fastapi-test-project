from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLACHEMY_DATABASE_URL = 'sqlite:///./blog.db'

DB_HOST_SERVER = 'localhost'
DB_SERVER_PORT = '5432'
DB_DATABASE_NAME = 'postgres'
DB_USERNAME = 'username'
DB_PASSWORD = 'password'
POSTGRES_DB_URL = f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_SERVER}:{DB_SERVER_PORT}/{DB_DATABASE_NAME}'


Base = declarative_base()

engine = create_async_engine(POSTGRES_DB_URL,
                             echo=True
                             )

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
