from pydantic import BaseModel, ConfigDict


class Ship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    x: float
    y: float
