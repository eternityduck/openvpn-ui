from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from sqlmodels.group import Group


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    mask: str
    group_id: int = Field(default=None, foreign_key="group.id")
    group: Group = Relationship(back_populates="routes")
