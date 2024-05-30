import socket
from typing import List

from config import OPENVPN_MGMT_PORT, OPENVPN_MGMT_HOST
from models.openvpn_client import OpenVpnClientStatus
from utils.utils import parse_mgmt_users


class OpenVpnManagementService:
    active_clients: List[OpenVpnClientStatus] = []

    @staticmethod
    def read_mgmt(connection) -> str:
        out = ""
        while True:
            recv_data = connection.recv(32768)
            if not recv_data:
                break
            out += recv_data.decode()
            if "END" in out or "SUCCESS:" in out or "ERROR:" in out:
                break
        return out

    def get_active_clients(self) -> List[OpenVpnClientStatus]:
        active_clients = []

        connection = socket.create_connection((OPENVPN_MGMT_HOST, OPENVPN_MGMT_PORT))
        connection.sendall(b"status\n")
        read_mgmt = self.read_mgmt(connection)
        active_clients.extend(parse_mgmt_users(read_mgmt))
        connection.close()

        self.active_clients = active_clients
        print(f"Connected clients: {self.active_clients}")

        return self.active_clients

    def update_active_clients(self) -> List[OpenVpnClientStatus]:
        """
        Update the list of active clients for cron job
        """
        self.get_active_clients()
        return self.active_clients

    def is_user_active(self, username: str) -> (bool, str):
        for client in self.active_clients:
            if client.username == username:
                return True, client.connected_since
        return False, "User is not active"

    def kill_user(self, username: str):
        """
        Kills a user connection after revocation/deleting
        """
        connection = socket.create_connection((OPENVPN_MGMT_HOST, OPENVPN_MGMT_PORT))
        connection.sendall(f"kill {username}\n".encode())
        self.read_mgmt(connection)
        connection.close()
