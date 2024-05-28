from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/main", tags=["Main"])


@router.get("/")
def index():
    response = {"ok": True}

    return JSONResponse(content=response)
