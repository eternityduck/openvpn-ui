import io

from config import (
    OPENVPN_INDEX_TXT_PATH,
    OPENVPN_EASYRSA_PATH,
    OPENVPN_LISTEN_HOST,
    OPENVPN_LISTEN_PORT,
    OPENVPN_PROTOCOL,
    OPENVPN_CCD_PATH
)
import subprocess
import json
import shutil
import os


from models.open_vpn_server import OpenVPNServer
from models.openvpn_client_conf import OpenVPNClientConf
from utils.utils import (parse_index_txt, file_reader, jinja_render, fix_crl_connections, file_writer, generate_index_txt)


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

    def ratify_user(self, username) -> (bool, str):
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"
        index_file = file_reader(OPENVPN_INDEX_TXT_PATH)
        index_data = parse_index_txt(index_file)
        for i in range(len(index_data)):
            if index_data[i]['id'] == username:
                if index_data[i]['flag'] == "R":
                    user_serial = index_data[i]['serial_number']
                    shutil.move(f"{OPENVPN_EASYRSA_PATH}/pki/revoked/private_by_serial/{user_serial}.key", f"{OPENVPN_EASYRSA_PATH}/pki/private/{username}.key")
                    shutil.copy2(f"{OPENVPN_EASYRSA_PATH}/pki/revoked/certs_by_serial/{user_serial}.crt", f"{OPENVPN_EASYRSA_PATH}/pki/issued/{username}.crt")
                    shutil.move(f"{OPENVPN_EASYRSA_PATH}/pki/revoked/certs_by_serial/{user_serial}.crt", f"{OPENVPN_EASYRSA_PATH}/pki/certs_by_serial/{user_serial}.pem")
                    shutil.move(f"{OPENVPN_EASYRSA_PATH}/pki/revoked/reqs_by_serial/{user_serial}.req", f"{OPENVPN_EASYRSA_PATH}/pki/reqs/{username}.req")

                    index_data[i]['flag'] = "V"
                    index_data[i]['revocation_date'] = ""

                    file_writer(OPENVPN_INDEX_TXT_PATH, generate_index_txt(index_data))

                    gen_crl_command = f'cd {OPENVPN_EASYRSA_PATH} && easyrsa gen-crl'
                    subprocess.run(gen_crl_command, shell=True, check=True, text=True)

                    fix_crl_connections(OPENVPN_EASYRSA_PATH)
                else:
                    return False, f"User {username} is not revoked"

        return True, f"User {username} ratified(un-revoked)"

    def delete_user(self, username) -> (bool, str):
        #TODO
        pass


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

    @staticmethod
    def check_group_exist(groupname) -> bool:
        path = f"{OPENVPN_CCD_PATH}/groups/{groupname}"
        return os.path.exists(path)

    def groups_list(self) -> list:
        groups = []
        for group in os.listdir(f"{OPENVPN_CCD_PATH}/groups"):
            groups.append(group)
        return groups

    def create_group(self, groupname) -> (bool, str):
        if self.check_group_exist(groupname):
            return False, f"Group {groupname} already exists"

        os.makedirs(f"{OPENVPN_CCD_PATH}/groups", exist_ok=True)

        group_file_path = f"{OPENVPN_CCD_PATH}/groups/{groupname}"
        with open(group_file_path, 'w') as group_file:
            group_file.close()

        return True, f"Group {groupname} created"

    def delete_group(self, groupname):
        if not self.check_group_exist(groupname):
            return False, f"Group {groupname} does not exist"

        group_file_path = f"{OPENVPN_CCD_PATH}/groups/{groupname}"
        os.remove(group_file_path)

        return True, f"Group {groupname} deleted"

    def add_user_to_group(self, username, groupname):
        if not self.check_group_exist(groupname):
            return False, f"Group {groupname} does not exist"
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"

        with open(f"{OPENVPN_CCD_PATH}/{username}", 'w') as user_file:
            user_file.write(f"config {OPENVPN_CCD_PATH}/groups/{groupname}")

        return True, f"User {username} added to group {groupname}"

    def add_routes_to_group(self, groupname, routes):
        if not self.check_group_exist(groupname):
            return False, f"Group {groupname} does not exist"
        #TODO
        return True, f"Route {routes} added to group {groupname}"

    def remove_routes_from_group(self, groupname, routes):
        # TODO
        return True, f"Route {routes} removed from group {groupname}"

    def remove_user_from_group(self, username, groupname):
        if not self.check_group_exist(groupname):
            return False, f"Group {groupname} does not exist"
        if not self.check_user_exist(username):
            return False, f"User {username} does not exist"

        return True, f"User {username} removed from group {groupname}"

