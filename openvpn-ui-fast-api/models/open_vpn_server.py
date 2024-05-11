from pydantic import BaseModel


class OpenVPNServer(BaseModel):
    host: str
    port: int
    protocol: str
