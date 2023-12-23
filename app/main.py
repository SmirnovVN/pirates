import logging

import uvicorn
from app.api.routes import router
from app.config import settings
from fastapi import FastAPI


logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
    handlers=[
        logging.FileHandler("log.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


@app.get("/")
async def root():
    logging.debug('Hello')
    return {"message": "Hello World"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
