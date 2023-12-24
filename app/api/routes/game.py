import random
import time
from io import BytesIO

from PIL import Image, ImageDraw
from fastapi import APIRouter, HTTPException, BackgroundTasks, Response, Query

from app.entities.map import Map
from app.enums.direction import Direction
from app.entities.game import Game, Destination
from app.enums.game_type import GameType
from app.service.game_service import leave_deathmatch, register_battle_royal, \
    register_deathmatch, get_map
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter()


@router.get("/start/{game_type}")
async def game_new(game_type: GameType, background_tasks: BackgroundTasks):
    game = Game()
    if game.started:
        return 'Game started already. Call game/stop to stop game'
    if game_type == GameType.BATTLE_ROYAL:
        success = await register_battle_royal()
    elif game_type == GameType.DEATHMATCH:
        success = await register_deathmatch()
    else:
        raise HTTPException(400,
                            detail=f'Bad game type: {game_type} . Pass battle_royal or deathmatch')
    if success:
        game.game_map = await get_map()
        game.started = True
        background_tasks.add_task(game.play)
        return 'Game started'
    return f'Game {game_type} was not started'


@router.get("/destination/{x}/{y}")
async def set_destination(x: int, y: int):
    Game.currentDestination = Destination(x, y)
    return 'Destination set'


@router.get("/stop")
async def game_stop():
    Game.stop()
    await leave_deathmatch()
    return 'Game stopped'


def draw(image, enlarge, ship, color):
    if ship.direction in {Direction.EAST, Direction.WEST}:
        width = ship.size * enlarge
        height = enlarge
    else:
        width = enlarge
        height = ship.size * enlarge
    draw_x, draw_y = ship.x * enlarge, ship.y * enlarge
    img = Image.new("RGB", (width, height), color)
    image.paste(img, (draw_x - (width if ship.direction == Direction.EAST else 0),
                      draw_y - (height if ship.direction == Direction.SOUTH else 0)))
    img = Image.new("RGB", (enlarge, enlarge), tuple([c + 50 for c in color]))
    image.paste(img, (draw_x, draw_y))
    idraw = ImageDraw.Draw(image)
    if ship.cannonRadius:
        radius = ship.cannonRadius
    else:
        radius = 20 # todo settings.deafult_cannon_radius
    idraw.ellipse(
        [
            draw_x - radius * enlarge,
            draw_y - radius * enlarge,
            draw_x + radius * enlarge,
            draw_y + radius * enlarge,
        ],
        outline=(235, 200, 200),
    )
    if ship.scanRadius:
        radius = ship.scanRadius
    else:
        radius = 20  # todo settings.deafult_cannon_radius
    idraw.ellipse(
        [
            draw_x - radius * enlarge,
            draw_y - radius * enlarge,
            draw_x + radius * enlarge,
            draw_y + radius * enlarge,
        ],
        outline=(180, 235, 180),
    )


def draw_coordinate_grid(image, cell_size, enlarge, width, height):
    idraw = ImageDraw.Draw(image)

    grid_color = (200, 200, 200)

    for y in range(0, height, cell_size):
        idraw.line([(0, y * enlarge), (width * enlarge, y * enlarge)], fill=grid_color)

    for x in range(0, width, cell_size):
        idraw.line([(x * enlarge, 0), (x * enlarge, height * enlarge)], fill=grid_color)

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            idraw.text((x * enlarge + 2, y * enlarge + 2), f"({x},{y})", fill=grid_color)


@router.get("/map/image/{enlarge}")
async def get_game_map(enlarge: int,
                       _: int = Query(int(time.time()))):
    game = Game()
    if game.started:
        if game.rendered:
            response = Response(content=game.image.getvalue(), media_type="image/png")
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            return response
        game_map: Map = game.game_map
        ships = game.ships
        enemies = game.enemies
        # import json
        # with open('map.json', 'r') as f:
        #     map_dict = json.loads(f.read())
        #     from app.entities.island import Island
        #     islands = [Island(**d) for d in map_dict['islands']]
        #     game_map = Map(width=map_dict['width'],
        #                    height=map_dict['height'],
        #                    slug=map_dict['slug'],
        #                    islands=islands)
        # with open('firstscan_example.json', 'r') as f:
        #     map_dict = json.loads(f.read())
        #     from app.entities.ship import Ship
        #     ships = [Ship(**d) for d in map_dict['scan']['myShips']]
        #     enemies = [Ship(**d) for d in map_dict['scan']['myShips']]
        #     for d in enemies:
        #         d.x = d.x + 100

        image = Image.new("RGB", (game_map.width * enlarge, game_map.height * enlarge), (226, 245, 226))

        for island in game_map.islands:
            island_map = island.map
            start_x, start_y = island.start
            for y, row in enumerate(island_map):
                for x, cell in enumerate(row):
                    if cell == 1 and x < game_map.width and y < game_map.height:
                        draw_x, draw_y = (start_x + x) * enlarge, (start_y + y) * enlarge
                        img = Image.new("RGB", (enlarge, enlarge), (107, 129, 109))
                        image.paste(img, (draw_x, draw_y))

        for ship in ships:
            draw(image, enlarge, ship, (20, 133, 165))

        for ship in enemies:
            draw(image, enlarge, ship, (183, 7, 43))

        draw_coordinate_grid(image, 100, enlarge, game_map.width, game_map.height)

        img_byte_array = BytesIO()
        image.save(img_byte_array, format="PNG")
        game.image = img_byte_array
        game.rendered = True

        response = Response(content=img_byte_array.getvalue(), media_type="image/png")
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response
    else:
        img_byte_array = BytesIO()
        image = Image.new("RGB", (2000, 2000),
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        image.save(img_byte_array, format="PNG")

        response = Response(content=img_byte_array.getvalue(), media_type="image/png")
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response


templates = Jinja2Templates(directory="templates")


# Endpoint to serve the HTML page
@router.get("/map/{enlarge}", response_class=HTMLResponse)
async def get_map_page(request: Request, enlarge: int):
    return templates.TemplateResponse("map.html",
                                      {"request": request, "enlarge": enlarge})
