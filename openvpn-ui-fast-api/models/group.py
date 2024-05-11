from typing import List, Optional

from pydantic import BaseModel


class Group(BaseModel):
    name: Optional[str] = None
    routes: Optional[List[str]] = None
