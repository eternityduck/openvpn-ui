import re
import subprocess

from jinja2 import Environment, FileSystemLoader


def parse_index_txt(index_txt: str) -> list:
    """
    Parse the index.txt file and return a list with the data
    """
    data = []
    for line in index_txt.split("\n"):
        if line:
            line = line.split()
            if line[0] == "V":
                data.append({
                    "flag": line[0],
                    "expiration_date": line[1],
                    "serial_number": line[2],
                    "file_name": line[3],
                    "subject_name": line[4],
                    "id": line[4].split("=", 1)[1],
                })
            elif line[0] == "R":
                data.append({
                    "flag": line[0],
                    "expiration_date": line[1],
                    "revocation_date": line[2],
                    "serial_number": line[3],
                    "file_name": line[4],
                    "subject_name": line[5],
                    "id": line[5].split("=", 1)[1],
                })
    return data

def generate_index_txt(data: list) -> str:
    """
    Generate the index.txt file content
    """
    index_txt = ""
    for user in data:
        if user['flag'] == "V":
            index_txt += f"{user['flag']}\t{user['expiration_date']}\t\t{user['serial_number']}\t{user['file_name']}\t{user['subject_name']}\n"
        elif user['flag'] == "R":
            index_txt += f"{user['flag']}\t{user['expiration_date']}\t{user['revocation_date']}\t{user['serial_number']}\t{user['file_name']}\t{user['subject_name']}\n"
    return index_txt


def file_reader(file_path: str) -> str:
    """
    Read a file and return the content
    """
    with open(file_path) as f:
        return f.read()


def file_writer(file_path: str, content: str):
    """
    Write a file
    """
    with open(file_path, "w") as f:
        f.write(content)


def validate_username(username: str) -> bool:
    """
    Validate the username
    """
    regex = re.compile(r'^[a-zA-Z0-9]*$')
    return True if 0 < len(username) < 40 else False


def jinja_render(obj: dict, **kwargs) -> str:
    """
    Render a Jinja template
    """
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('client.conf.j2')

    return template.render(**obj)


def fix_crl_connections(earysa_path: str):
    """
    Fix the CRL connections https://community.openvpn.net/openvpn/ticket/623
    """
    subprocess.run(f'chmod 0644 {earysa_path}/pki/crl.pem', shell=True, check=True, text=True)
    subprocess.run(f'chmod 0755 {earysa_path}/pki', shell=True, check=True, text=True)
