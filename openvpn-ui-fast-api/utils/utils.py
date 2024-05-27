import re
import subprocess
from typing import List

from jinja2 import Environment, FileSystemLoader

from config import OPENVPN_LISTEN_HOST, OPENVPN_LISTEN_PORT
from models.group import Group
from models.openvpn_client import OpenVpnClientStatus
import bcrypt
from datetime import datetime

from models.route import Route


# TODO add types
def parse_index_txt(index_txt: str) -> list:
    """
    Parse the index.txt file and return a list with the users data
    """
    data = []
    for line in index_txt.split("\n"):
        if line:
            line = line.split()
            if line[0] == "V":
                data.append(
                    {
                        "flag": line[0],
                        "expiration_date": line[1],
                        "serial_number": line[2],
                        "file_name": line[3],
                        "subject_name": line[4],
                        "id": line[4].split("=", 1)[1],
                    }
                )
            elif line[0] == "R":
                data.append(
                    {
                        "flag": line[0],
                        "expiration_date": line[1],
                        "revocation_date": line[2],
                        "serial_number": line[3],
                        "file_name": line[4],
                        "subject_name": line[5],
                        "id": line[5].split("=", 1)[1],
                    }
                )
    return data


def parse_mgmt_users(users_text: str) -> List[OpenVpnClientStatus]:
    """
    Parse the users from the management interface
    """
    users: List[OpenVpnClientStatus] = []
    client_list = False
    route_table = False

    for line in users_text.split("\n"):
        if "Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since" in line:
            client_list = True
            continue
        if "Virtual Address,Common Name,Real Address,Last Ref" in line:
            route_table = True
            continue
        if "ROUTING TABLE" in line:
            client_list = False
            continue
        if "GLOBAL STATS" in line:
            break

        if client_list:
            user_data = line.split(",")
            user_status = OpenVpnClientStatus(
                username=user_data[0],
                address=user_data[1],
                bytes_received=user_data[2],
                bytes_sent=user_data[3],
                connected_since=user_data[4],
                connected_to=f"{OPENVPN_LISTEN_HOST}:{OPENVPN_LISTEN_PORT}",
            )
            users.append(user_status)

        if route_table:
            route_data = line.split(",")
            for user in users:
                if user.username == route_data[1]:
                    user.virtual_address = route_data[0]
                    user.last_ref = route_data[3]
                    break

    return users


def generate_index_txt(data: list) -> str:
    index_txt = ""
    for user in data:
        if user["flag"] == "V":
            index_txt += f"{user['flag']}\t{user['expiration_date']}\t\t{user['serial_number']}\t{user['file_name']}\t{user['subject_name']}\n"
        elif user["flag"] == "R":
            index_txt += f"{user['flag']}\t{user['expiration_date']}\t{user['revocation_date']}\t{user['serial_number']}\t{user['file_name']}\t{user['subject_name']}\n"
    return index_txt


def file_reader(file_path: str) -> str:
    """
    Read a file and return the content
    """
    with open(file_path) as f:
        return f.read()


def file_writer(file_path: str, content: str):
    with open(file_path, "w") as f:
        f.write(content)


def validate_username(username: str) -> bool:
    regex = re.compile(r"^[a-zA-Z0-9]*$")
    return True if 0 < len(username) < 40 else False


def jinja_render(obj: dict, **kwargs) -> str:
    """
    Render a Jinja template
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("client.conf.j2")

    return template.render(**obj)


def fix_crl_connections(easyrsa_path: str):
    """
    Fix the CRL connections https://community.openvpn.net/openvpn/ticket/623
    """
    subprocess.run(
        f"chmod 0644 {easyrsa_path}/pki/crl.pem", shell=True, check=True, text=True
    )
    subprocess.run(f"chmod 0755 {easyrsa_path}/pki", shell=True, check=True, text=True)


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def map_groups(groups):
    groups_dict = {}
    for group, route in groups:
        if group.id not in groups_dict:
            groups_dict[group.id] = {"name": group.name, "routes": []}
        if route is not None:
            groups_dict[group.id]["routes"].append(
                Route(address=route.address, mask=route.mask)
            )

    groups_with_routes = []
    for group_id, group_data in groups_dict.items():
        groups_with_routes.append(
            Group(name=group_data["name"], routes=group_data["routes"])
        )
    return groups_with_routes


def parse_easyrsa_date(date: str) -> str:
    """
    Parse the date from easyrsa to a human-readable format
    """
    date_time_obj = datetime.strptime(date, "%y%m%d%H%M%S%fZ")

    human_readable_date = date_time_obj.strftime("%B %d, %Y, %I:%M:%S %p UTC")

    return human_readable_date
