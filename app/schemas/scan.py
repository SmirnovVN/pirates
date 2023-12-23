from typing import List, Optional

from app.entities.ship import Ship


class Scan:
    def __init__(self, myShips: List[Ship], enemyShips: List[Ship], zone: Optional[str], tick: int):
        self.myShips = myShips
        self.enemyShips = enemyShips
        self.zone = zone
        self.tick = tick
