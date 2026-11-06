from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:1982003@localhost/todos_litestar"

engine = create_async_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

async_session = async_sessionmaker(engine, expire_on_commit=False)