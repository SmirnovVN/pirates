import asyncio
import logging
from typing import Optional, List

from app.config import settings
from app.core.navigation import decide
from app.entities.map import Map
from app.entities.ship import Ship
from app.schemas.scan import Scan
from app.service.game_service import scan, send_commands
from app.utils.singleton import Singleton


class Destination:
    def __init__(self, x: int, y: int, forced: bool = False):
        self.x = x
        self.y = y
        self.forced = forced


class Game(metaclass=Singleton):

    def __init__(self):
        self.game_map: Optional[Map] = None
        self.ships: List[Ship] = []
        self.enemies: List[Ship] = []
        self.started = False
        self.current_tick = None
        self.rendered = False
        self.image = None
        self.zone = None
        self.currentDestination = None

    @staticmethod
    def stop():
        logging.debug('Game stop')
        game = Game()
        game.started = False
        Game._instances = {}

    async def play(self):
        logging.debug('Play')
        while self.started:
            try:
                logging.debug('Scan')
                s: Scan = await scan()
                logging.debug(f'Current tick {s.tick}')
                if self.current_tick != s.tick:
                    self.current_tick = s.tick
                    self.rendered = False
                    self.ships = s.myShips
                    self.enemies = s.enemyShips
                    self.zone = s.zone
                    if not self.ships:
                        logging.debug('No ships')
                        Game.stop()
                        return
                    if not self.currentDestination and self.zone:
                        self.currentDestination = Destination(self.zone.x, self.zone.y)
                    elif not self.currentDestination:
                        self.currentDestination = Destination(1000, 1000)
                    logging.info(f'Our ships: {self.ships}')
                    logging.info(f'Enemy ships: {self.enemies}')
                    commands = []
                    for ship in self.ships:
                        command = decide(ship, self.game_map, self.enemies, self.currentDestination)
                        if command:
                            commands.append(command)
                    commandsass = "\n".join([str(d.to_dict()) for d in commands])
                    logging.info(f'Send {commandsass}')
                    if commands and settings.send_commands:
                        logging.info(f'Send {len(commands)} commands on tick: {self.current_tick}')
                        await send_commands(commands)
                    else:
                        logging.info(f'No commands on tick: {self.current_tick}')
                    await asyncio.sleep(3)
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(10)
