from models.open_vpn_server import OpenVPNServer


class OpenClientConf:
    server: OpenVPNServer
    cert: str
    key: str
    ca: str
    tls: str
