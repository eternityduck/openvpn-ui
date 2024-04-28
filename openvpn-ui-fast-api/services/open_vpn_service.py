from config import (
    OPENVPN_INDEX_TXT_PATH,
    OPENVPN_EASYRSA_PATH
)
import subprocess

from utils.utils import (parse_index_txt, file_reader)


class OpenVPNService:

    def create_user(self, username) -> (bool, str):
        if self.check_user_exist(username):
            return False, f"User {username} already exists"

        #TODO validate username
        subprocess.run(f'cd {OPENVPN_EASYRSA_PATH} && easyrsa --batch build-client-full {username} nopass', shell=True, check=True, text=True)




        return True, f"User {username} created"




    @staticmethod
    def check_user_exist(username):
        file = file_reader(OPENVPN_INDEX_TXT_PATH)
        data = parse_index_txt(file)
        for user in data:
            if user['id'] == username:
                return True
        return False

    def generateConfig(self, username):



    def downloadConfig(self, username):
