import asyncio
import logging

import uvicorn
from app.api.routes import router
from app.config import settings
from fastapi import FastAPI

from app.entities.game import Game
from app.service.game_service import scan, get_map

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


@app.on_event("startup")
async def startup_event():
    print("Startup")
    res = await scan()
    if res:
        game = Game()
        game.game_map = await get_map()
        game.started = True
        asyncio.create_task(game.play())


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, port=8000, reload_excludes=["*.log"])
