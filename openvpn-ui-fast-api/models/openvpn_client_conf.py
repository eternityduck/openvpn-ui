from models.open_vpn_server import OpenVPNServer


class OpenVPNClientConf:
    server: OpenVPNServer
    cert: str
    key: str
    ca: str
    tls: str
    pass_auth: bool
