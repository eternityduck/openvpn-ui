from fastapi import FastAPI
from utils.utils import parse_index_txt
from config import (OPENVPN_INDEX_TXT_PATH, APP_HOST, APP_PORT)
from services.open_vpn_service import OpenVPNService
from models.user import User

app = FastAPI()
openvpnService = OpenVPNService()


# @app.get("/")
# async def root():
#
#     return {"message": result}


@app.get("/download/{username}")
async def download_config(name: str):
    return {"message": f"Hello {name}"}


@app.post("/user")
async def create_user(user: User):
    openvpnService.create_user(user.username)
    return {"message": f"Created user {user.username}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
