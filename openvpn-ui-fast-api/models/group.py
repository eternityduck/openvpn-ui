from typing import List, Optional

from pydantic import BaseModel


class Group(BaseModel):
    name: str
    routes: Optional[List[str]] = None
