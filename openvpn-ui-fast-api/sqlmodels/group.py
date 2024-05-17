from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel


from sqlmodels.user_group import UserGroup


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None

    users: list["User"] = Relationship(back_populates="groups", link_model=UserGroup)
