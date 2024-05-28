from os import environ

import uvicorn
from fastapi import FastAPI

from services.main import router as main_router

import debugpy

debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()
app.include_router(main_router)


if __name__ == "__main__":
    port = environ.get("PORT")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
