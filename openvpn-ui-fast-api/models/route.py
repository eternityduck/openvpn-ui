from pydantic import BaseModel


class Route(BaseModel):
    address: str
    mask: str
