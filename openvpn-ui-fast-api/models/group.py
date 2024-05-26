from typing import List, Optional

from pydantic import BaseModel

from models.route import Route


class Group(BaseModel):
    name: Optional[str] = None
    routes: Optional[List[Route]] = None
