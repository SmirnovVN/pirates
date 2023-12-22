import logging
import sys

import uvicorn
from app.api.routes import router
from app.config import settings
from fastapi import FastAPI

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug else logging.INFO)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
