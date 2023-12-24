import logging
from typing import Optional, List

from fastapi import BackgroundTasks

from app.core.navigation import decide
from app.entities.map import Map
from app.entities.ship import Ship
from app.schemas.scan import Scan
from app.service.game_service import get_map, scan, send_commands
from app.utils.singleton import Singleton


class Destination:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Game(metaclass=Singleton):
    currentDestination: Optional[Destination] = None

    def __init__(self):
        self.game_map: Optional[Map] = None
        self.ships: List[Ship] = []
        self.enemies: List[Ship] = []
        self.started = False
        self.current_tick = None
        self.rendered = False
        self.image = None
        self.zone = None

    @staticmethod
    def stop():
        logging.debug('Game stop')
        game = Game()
        game.started = False
        Game._instances = {}

    async def play(self):
        logging.debug('Play')
        while self.started:
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
                logging.debug(f'We have {len(self.ships)} ships')
                logging.debug(f'We see {len(self.enemies)} enemies' if self.enemies else 'No enemies')
                commands = []
                if self.enemies:
                    self.currentDestination = None
                dest_x = self.currentDestination.x if self.currentDestination else None
                dest_y = self.currentDestination.y if self.currentDestination else None
                for ship in self.ships:
                    command = decide(ship, self.game_map, self.enemies, dest_x, dest_y)
                    if command:
                        commands.append(command)
                if commands:
                    logging.info(f'Send {len(commands)} commands on tick: {self.current_tick}')
                    await send_commands(commands)
                else:
                    logging.info(f'No commands on tick: {self.current_tick}')
