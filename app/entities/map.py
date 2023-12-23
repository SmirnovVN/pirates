from typing import List

from app.entities.island import Island


class Map:
    def __init__(self, width: int, height: int, slug: str, islands: List[Island]):
        self.width = width
        self.height = height
        self.slug = slug
        self.islands = islands
