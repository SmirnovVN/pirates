from typing import List

from app.entities.map import Map
from app.schemas.response import Response
from app.schemas.scan import Scan
from app.entities.ship import Ship


class GameService:

    def register_deathmatch(self) -> bool:
        pass

    def leave_deathmatch(self) -> bool:
        pass

    def register_battle_royal(self) -> bool:
        pass

    def get_map(self) -> Map:
        pass

    def scan(self) -> Scan:
        pass

    def long_scan(self) -> Scan:
        pass

    def send_commands(self, ships: List[Ship]) -> Response:
        pass
