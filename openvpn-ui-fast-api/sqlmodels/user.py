from sqlmodel import Field, Relationship, SQLModel, create_engine, select

from typing import Optional


from sqlmodels.user_group import UserGroup


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: Optional[str] = None
    revoked: Optional[bool] = False

    groups: list["Group"] = Relationship(back_populates="users", link_model=UserGroup)
