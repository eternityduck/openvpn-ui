from pydantic import BaseModel


class OpenVpnClientStatus(BaseModel):
    username: str
    address: str
    connected_since: str
    virtual_address: str = None
    last_ref: str = None
    bytes_sent: str
    bytes_received: str
    connected_to: str
