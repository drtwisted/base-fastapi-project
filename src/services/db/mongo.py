from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

__CLIENT = AsyncIOMotorClient("mongodb://mongodb:27017")


def get_db_client() -> AsyncIOMotorClient:
    return __CLIENT


AsyncMongoDbClientDep = Annotated[AsyncIOMotorClient, Depends(get_db_client)]
