import http

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from services.db.sqlite import AsyncSessionDep
from sqlalchemy import text

router = APIRouter(prefix="/main", tags=["Main"])


@router.get("/")
def index():
    response = {"ok": True}

    return JSONResponse(content=response)


@router.post("/create-table")
async def create_table(session: AsyncSessionDep) -> Response:
    await session.execute(text("DROP INDEX IF EXISTS ids_id;"))
    await session.execute(text("DROP TABLE IF EXISTS persons;"))

    await session.execute(
        text(
            """CREATE TABLE persons (
                    id INT PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100)
                );""",
        ),
    )
    await session.execute(
        text("CREATE INDEX ids_id ON persons (id);"),
    )
    persons = (
        (1, "John", "Doe"),
        (2, "Sarah", "Conor"),
        (3, "Bruce", "Lee"),
    )
    await session.execute(
        text(
            f"""INSERT INTO persons (id, first_name, last_name)
            VALUES
                {', '.join([str(p) for p in persons])};""",
        ),
    )
    await session.commit()

    return Response(status_code=http.HTTPStatus.CREATED)


@router.get("/persons")
async def get_persons(session: AsyncSessionDep) -> JSONResponse:
    results = await session.execute(text("SELECT id, first_name, last_name FROM persons;"))

    response = [{name: value for name, value in zip(("id", "first_name", "last_name"), row)} for row in results.all()]

    return JSONResponse(response)


@router.get("/person/{id}")
async def get_presons(id: int, session: AsyncSessionDep) -> JSONResponse:
    result = await session.execute(text(f"SELECT id, first_name, last_name FROM persons WHERE id={id};"))

    response = {name: value for name, value in zip(("id", "first_name", "last_name"), result.first())}

    return JSONResponse(response)
