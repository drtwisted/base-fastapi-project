import http
import re
from typing import Annotated

from fastapi import APIRouter, Response
from fastapi.params import Query
from fastapi.responses import JSONResponse
from services.db.mongo import AsyncMongoDbClientDep

router = APIRouter(prefix="/secondary", tags=["Secondary"])


@router.post("/create-collection")
async def create_collection(mongo: AsyncMongoDbClientDep) -> Response:
    persons = mongo["test"]["persons"]

    await persons.delete_many({})

    await persons.insert_many(
        (
            {
                "first_name": "John",
                "last_name": "Connor",
                "age": 13,
            },
            {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
            },
            {
                "first_name": "Quentin",
                "last_name": "Tarantino",
                "age": 61,
            },
            {
                "first_name": "Satoru",
                "last_name": "Iwata",
                "age": 56,
            },
        ),
    )

    return Response(status_code=http.HTTPStatus.CREATED)


@router.get("/")
async def secondary(mongo: AsyncMongoDbClientDep, count: Annotated[int, Query(ge=0)] = 100) -> JSONResponse:
    persons = mongo["test"]["persons"]
    # results = await persons.find({}).to_list(1)
    results = await persons.find(
        {},
        {
            "_id": False,
            "id": {
                "$toString": "$_id",
            },
            "first_name": True,
            "last_name": True,
            "full_name": {"$concat": ["$first_name", " ", "$last_name"]},
            "age": True,
            "status": {
                "$switch": {
                    "branches": [
                        {"case": {"$gt": ["$age", 50]}, "then": "Old"},
                        {"case": {"$lte": ["$age", 50]}, "then": "Young"},
                    ],
                },
            },
        },
    ).to_list(count)

    return JSONResponse(results)


@router.get("/person")
async def get_person(
    mongo: AsyncMongoDbClientDep,
    first_name: Annotated[str | None, Query(max_length=50)] = None,
    last_name: Annotated[str | None, Query(max_length=50)] = None,
    age: Annotated[int | None, Query(ge=0)] = None,
    count: Annotated[int, Query(ge=0)] = 100,
) -> JSONResponse:
    persons_filter = {}

    if first_name:
        persons_filter["first_name"] = {
            "$regex": re.compile(first_name, re.IGNORECASE),
        }

    if last_name:
        persons_filter["last_name"] = {
            "$regex": re.compile(last_name, re.IGNORECASE),
        }

    if age:
        persons_filter["age"] = age

    persons = mongo["test"]["persons"]

    results = await persons.find(
        persons_filter,
        {
            "_id": False,
            "id": {"$toString": "$_id"},
            "first_name": True,
            "last_name": True,
            "age": True,
        },
    ).to_list(count)

    return JSONResponse(results)
