from settings import PG_HOST, PG_PORT, PG_USER, PG_PASS, PG_DB_NAME
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator




DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        yield session



#docker run --name pgdb1 -p 5432:5432 -e POSTGRES_USER=ewan -e POSTGRES_PASSWORD=myPassword1979 -e POSTGRES_DB=pgdb1 -d postgres:latest

# docker run --name pgdb1 -e POSTGRES_PASSWORD=myPassword1979 -e POSTGRES_USER=ewan -p 5432:5432 -p POSTGRES_HOST=127.0.0.1 -d postgres:latest