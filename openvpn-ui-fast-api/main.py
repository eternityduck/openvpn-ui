from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from config import APP_HOST, APP_PORT
from services.open_vpn_management_service import OpenVpnManagementService
from services.open_vpn_service import OpenVPNService
from models.user import User
from models.group import Group
from apscheduler.schedulers.background import BackgroundScheduler
from models.client import Client


@asynccontextmanager
async def lifespan(app_fast_api: FastAPI):
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2})
    scheduler.add_job(mgmtService.update_active_clients, "interval", seconds=20)
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)
mgmtService = OpenVpnManagementService()
openvpnService = OpenVPNService(mgmtService)


@app.get("/")
async def root() -> List[Client]:
    result = openvpnService.users_list()
    return result


@app.get("/download/{username}")
async def download_config(username: str):
    file = openvpnService.download_config(username)
    return StreamingResponse(
        iter([file.getvalue()]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={username}.ovpn"},
    )
    # return FileResponse(file.getvalue(), filename=f"{username}.ovpn")


@app.post("/user")
async def create_user(user: User):
    result = openvpnService.create_user(user.username)
    return {"message": result[1]}


@app.get("/revoke/{username}")
async def revoke_user(username: str):
    openvpnService.revoke_user(username)
    return {"message": f"Revoked user {username}"}


@app.get("/ratify/{username}")
async def ratify_user(username: str):
    openvpnService.ratify_user(username)
    return {"message": f"Ratified user {username}"}


@app.post("/group")
async def create_group(group: Group):
    result = openvpnService.create_group(group.name)
    return {"message": result[1]}


@app.get("/group")
async def groups_list():
    return {"result": openvpnService.groups_list()}


@app.get("/group/{groupname}/user/{username}")
async def add_user_to_group(username: str, groupname: str):
    result = openvpnService.add_user_to_group(username, groupname)
    return {"message": result[1]}


@app.delete("/group/{groupname}/user/{username}")
async def add_user_to_group(username: str, groupname: str):
    result = openvpnService.remove_user_from_group(username, groupname)
    return {"message": result[1]}


@app.delete("/group/{groupname}")
async def delete_group(groupname: str):
    result = openvpnService.delete_group(groupname)
    return {"message": result[1]}


@app.post("/group/{groupname}/routes")
async def add_routes_group(groupname: str, group: Group):
    result = openvpnService.add_routes_to_group(groupname, group.routes)
    return {"message": result[1]}


@app.delete("/group/{groupname}/routes")
async def delete_routes_group(groupname: str, group: Group):
    result = openvpnService.remove_routes_from_group(groupname, group.routes)
    return {"message": result[1]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
