import io

from config import (
    OPENVPN_INDEX_TXT_PATH,
    OPENVPN_EASYRSA_PATH,
    OPENVPN_LISTEN_HOST,
    OPENVPN_LISTEN_PORT,
    OPENVPN_PROTOCOL
)
import subprocess
import json
import shutil


from models.open_vpn_server import OpenVPNServer
from models.openvpn_client_conf import OpenVPNClientConf
from utils.utils import (parse_index_txt, file_reader, jinja_render, fix_crl_connections)


class OpenVPNService:

    def create_user(self, username) -> (bool, str):
        if self.check_user_exist(username):
            return False, f"User {username} already exists"

        #TODO validate username
        subprocess.run(f'cd {OPENVPN_EASYRSA_PATH} && easyrsa --batch build-client-full {username} nopass', shell=True, check=True, text=True)

        return True, f"User {username} created"

    def revoke_user(self, username) -> (bool, str):
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"

        revoke_command = f'cd {OPENVPN_EASYRSA_PATH} && easyrsa --batch revoke {username}'
        subprocess.run(revoke_command, shell=True, check=True, text=True)

        gen_crl_command = f'cd {OPENVPN_EASYRSA_PATH} && easyrsa gen-crl'
        subprocess.run(gen_crl_command, shell=True, check=True, text=True)

        fix_crl_connections(OPENVPN_EASYRSA_PATH)

        return True, f"User {username} revoked"

    def unrevoke_user(self, username):
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"

        shutil.move(f"{OPENVPN_EASYRSA_PATH}/pki/revoked/private_by_serial/{username}.key", f"{OPENVPN_EASYRSA_PATH}/pki/private/{username}.key")
        subprocess.run(revoke_command, shell=True, check=True, text=True)

        gen_crl_command = f'cd {OPENVPN_EASYRSA_PATH} && easyrsa gen-crl'
        subprocess.run(gen_crl_command, shell=True, check=True, text=True)

        fix_crl_connections(OPENVPN_EASYRSA_PATH)

        return True, f"User {username} un-revoked"


    @staticmethod
    def check_user_exist(username) -> bool:
        file = file_reader(OPENVPN_INDEX_TXT_PATH)
        data = parse_index_txt(file)
        for user in data:
            if user['id'] == username:
                return True
        return False

    def generate_config(self, username) -> (bool, str):
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"
        openvpn_client_conf = OpenVPNClientConf()
        openvpn_client_conf.server = OpenVPNServer(host=OPENVPN_LISTEN_HOST, port=OPENVPN_LISTEN_PORT, protocol=OPENVPN_PROTOCOL)
        openvpn_client_conf.ca = file_reader(f"{OPENVPN_EASYRSA_PATH}/pki/ca.crt")
        openvpn_client_conf.tls = file_reader(f"{OPENVPN_EASYRSA_PATH}/pki/ta.key")
        openvpn_client_conf.key = file_reader(f"{OPENVPN_EASYRSA_PATH}/pki/private/{username}.key")
        openvpn_client_conf.cert = file_reader(f"{OPENVPN_EASYRSA_PATH}/pki/issued/{username}.crt")

        obj_dict = json.loads(json.dumps(openvpn_client_conf, default=lambda o: o.__dict__))

        return jinja_render(obj_dict)

    def users_list(self):
        file = file_reader(OPENVPN_INDEX_TXT_PATH)
        data = parse_index_txt(file)
        return data


    # def download_config(self, username):
    #     config = self.generate_config(username)
    #     with open(f"{username}.txt", "w") as f:
    #         return f.write(config)
    def download_config(self, username):
        config = self.generate_config(username)
        buffer = io.StringIO()
        buffer.write(config)
        buffer.seek(0)
        return buffer
