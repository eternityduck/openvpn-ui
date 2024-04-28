import os


def try_parse_int(value: str):
    try:
        return int(value)
    except Exception:
        return None


OPENVPN_INDEX_TXT_PATH = os.getenv('OPENVPN_INDEX_TXT_PATH') or '../easyrsa/pki/index.txt'
OPENVPN_EASYRSA_PATH = os.getenv('OPENVPN_EASYRSA_PATH') or './easyrsa'
OPENVPN_CLIENT_CONFIG_PATH = os.getenv('OPENVPN_CLIENT_CONFIG_PATH')
OPENVPN_CLIENT_CONFIG_TEMPLATE_PATH = os.getenv('OPENVPN_CLIENT_CONFIG_TEMPLATE_PATH')
APP_HOST = os.getenv('APP_HOST') or '0.0.0.0'
APP_PORT = try_parse_int(os.getenv('APP_PORT')) or 8080
OPENVPN_LISTEN_HOST = os.getenv('OPENVPN_LISTEN_HOST') or '127.0.0.1'
OPENVPN_LISTEN_PORT = try_parse_int(os.getenv('OPENVPN_LIST')) or 1194
OPENVPN_PROTOCOL = os.getenv('OPENVPN_PROTOCOL') or 'tcp'