from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from config import (OPENVPN_INDEX_TXT_PATH, APP_HOST, APP_PORT)
from services.open_vpn_service import OpenVPNService
from models.user import User

app = FastAPI()
openvpnService = OpenVPNService()


@app.get("/")
async def root():
    return {"message": openvpnService.users_list()}


@app.get("/download/{username}")
async def download_config(username: str):
    file = openvpnService.download_config(username)
    return StreamingResponse(iter([file.getvalue()]), media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={username}.ovpn"})
    # return FileResponse(file.getvalue(), filename=f"{username}.ovpn")


@app.post("/user")
async def create_user(user: User):
    openvpnService.create_user(user.username)
    return {"message": f"Created user {user.username}"}


@app.get("/revoke/{username}")
async def revoke_user(username: str):
    openvpnService.revoke_user(username)
    return {"message": f"Revoked user {username}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
