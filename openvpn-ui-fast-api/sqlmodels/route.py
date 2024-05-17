from typing import Optional, List

from sqlmodel import Field, String, SQLModel, Column, ARRAY


class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    route: str
    mask: str
    group_id: int = Field(default=None, foreign_key="group.id")
