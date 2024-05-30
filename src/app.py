from os import environ

import uvicorn
from fastapi import FastAPI
from services.main import router as main_router
from services.secondary import router as secondary_router

app = FastAPI()
app.include_router(main_router)
app.include_router(secondary_router)


if __name__ == "__main__":
    port = int(environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
