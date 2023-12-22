import requests
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from ..config import settings


class Ship(Base):
    __tablename__ = "ship"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    x: Mapped[float]
    y: Mapped[float]
