import os


def try_parse_int(value: str):
    try:
        return int(value)
    except TypeError:
        return None


OPENVPN_INDEX_TXT_PATH = (
    os.getenv("OPENVPN_INDEX_TXT_PATH") or "../easyrsa/pki/index.txt"
)
OPENVPN_EASYRSA_PATH = os.getenv("OPENVPN_EASYRSA_PATH", "../easyrsa")
OPENVPN_CLIENT_CONFIG_PATH = os.getenv("OPENVPN_CLIENT_CONFIG_PATH")
OPENVPN_CLIENT_CONFIG_TEMPLATE_PATH = os.getenv("OPENVPN_CLIENT_CONFIG_TEMPLATE_PATH")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = try_parse_int(os.getenv("APP_PORT")) or 8080
OPENVPN_LISTEN_HOST = os.getenv("OPENVPN_LISTEN_HOST", "127.0.0.1")
OPENVPN_LISTEN_PORT = try_parse_int(os.getenv("OPENVPN_LISTEN_PORT")) or 1194
OPENVPN_PROTOCOL = os.getenv("OPENVPN_PROTOCOL", "tcp")
OPENVPN_CCD_PATH = os.getenv("OPENVPN_CCD_PATH", "../ccd")
OPENVPN_MGMT_HOST = os.getenv("OPENVPN_MGMT_HOST", "openvpn")
OPENVPN_MGMT_PORT = try_parse_int(os.getenv("OPENVPN_MGMT_PASSWORD")) or 8989
OPENVPN_PASSWORD_AUTH = os.getenv("OPENVPN_PASSWORD_AUTH", False) == "true"
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "/opt/db/openvpn-ui.db")
OPENVPN_CCD_CONFIG_PATH = os.getenv("OPENVPN_CCD_CONFIG_PATH", "/etc/openvpn/ccd")
