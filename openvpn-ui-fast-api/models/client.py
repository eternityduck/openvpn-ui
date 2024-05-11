from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    username: str
    connected: bool
    connected_since: Optional[str]
    revoked: bool
    revocation_date: Optional[str]
    expiration_date: str
