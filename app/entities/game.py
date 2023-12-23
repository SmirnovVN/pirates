from typing import Optional, List

from app.entities.map import Map
from app.entities.ship import Ship
from app.service.game_service import get_map, scan
from app.utils.singleton import Singleton


class Game(metaclass=Singleton):
    def __init__(self):
        self.game_map: Optional[Map] = None
        self.ships: List[Ship] = []
        self.enemies: List[Ship] = []
        self.started = False

    @staticmethod
    def stop():
        game = Game()
        game.started = False
        Game._instances = {}

    async def start(self):
        self.game_map = await get_map()
        s = scan()
        # TODO run forever
        self.started = True
