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
                    "revoke_date": line[2],
                    "serial_number": line[3],
                    "file_name": line[4],
                    "subject_name": line[5],
                    "id": line[5].split("=", 1)[1],
                })
    return data


def file_reader(file_path: str) -> str:
    """
    Read a file and return the content
    """
    with open(file_path) as f:
        return f.read()


def validate_username(username: str) -> bool:
    """
    Validate the username
    """
    return True if len(username) > 0 and len(username) < 30 else False