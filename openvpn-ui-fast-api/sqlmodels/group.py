from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


from sqlmodels.user_group import UserGroup


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None

    routes: list["Route"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="group"
    )
    users: list["User"] = Relationship(back_populates="groups", link_model=UserGroup)
