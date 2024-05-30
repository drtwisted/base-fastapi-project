from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

__ENGINE = create_async_engine(
   "sqlite+aiosqlite:///test.db",
   echo=True,
)
__async_session_factory = async_sessionmaker(bind=__ENGINE, expire_on_commit=True)


async def get_sesssion() -> AsyncGenerator[AsyncSession, None]:
   async with __async_session_factory() as session:
      yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_sesssion)]
