import asyncio
from typing import Optional, List

from fastapi import BackgroundTasks

from app.core.navigation import decide
from app.entities.map import Map
from app.entities.ship import Ship
from app.schemas.scan import Scan
from app.service.game_service import get_map, scan, send_commands
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

    async def start(self, background_tasks: BackgroundTasks):
        self.game_map = await get_map()
        self.started = True
        print('Start play')
        background_tasks.add_task(self.play)

    async def play(self):
        print('Play')
        while self.started:
            s: Scan = await scan()
            self.ships = s.myShips
            self.enemies = s.enemyShips
            if not self.ships:
                Game.stop()
                return
            print('Map exist' if self.game_map else 'Map is None')
            print(f'We have {len(self.ships)} ships' if self.ships else 'No ships')
            print(f'We see {len(self.enemies)} ships' if self.enemies else 'No enemies')
            commands = []
            for ship in self.ships:
                command = decide(ship, self.game_map, self.enemies)
                if command:
                    commands.append(command)
            if commands:
                await send_commands(commands)
            await asyncio.sleep(3)  # todo how much time
