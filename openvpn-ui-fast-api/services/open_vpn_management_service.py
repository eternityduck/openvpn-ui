import socket
from utils.utils import parse_mgmt_users

class OpenVPNService:

    def read_mgmt(self, connection):
        out = ""
        while True:
            recv_data = connection.recv(32768)
            if not recv_data:
                break
            out += recv_data.decode()
            if "type 'help' for more info" in out or "END" in out or "SUCCESS:" in out or "ERROR:" in out:
                break
        return out

    def get_active_clients(self) -> list:
        """
        Get the list of active clients
        """
        active_clients = []
        try:
            connection = socket.create_connection(("127.0.0.1", 8989))
            connection.sendall(b"status\n")
            active_clients.extend(parse_mgmt_users(self.read_mgmt(connection)))
            connection.close()
        except:
            print("Error getting users statuses")


        return active_clients