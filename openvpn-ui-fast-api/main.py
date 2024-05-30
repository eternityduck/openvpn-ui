from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import Response, StreamingResponse

from config import APP_HOST, APP_PORT
from db import DbContext
from repositories.group_repo import GroupRepository
from repositories.route_repo import RouteRepository
from repositories.user_repo import UserRepository
from services.open_vpn_management_service import OpenVpnManagementService
from services.open_vpn_service import OpenVPNService
from models.user import User
from models.group import Group
from models.route import Route
from apscheduler.schedulers.background import BackgroundScheduler
from models.client import Client
from utils.utils import map_groups

from fastapi.middleware.cors import CORSMiddleware

from sqlmodels.user import User as UserModel
from sqlmodels.group import Group as GroupModel
from sqlmodels.route import Route as RouteModel


@asynccontextmanager
async def lifespan(app_fast_api: FastAPI):
    scheduler = BackgroundScheduler({"apscheduler.job_defaults.max_instances": 2})
    scheduler.add_job(mgmtService.update_active_clients, "interval", seconds=20)
    scheduler.start()
    yield


dbContext = DbContext()
app = FastAPI(lifespan=lifespan)
# app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mgmtService = OpenVpnManagementService()
userRepo = UserRepository(dbContext.get_session())
groupRepo = GroupRepository(dbContext.get_session())
routeRepo = RouteRepository(dbContext.get_session())
openvpnService = OpenVPNService(mgmtService, userRepo, groupRepo, routeRepo)


@app.get("/")
async def root() -> List[Client]:
    result = openvpnService.users_list()
    return result


@app.post("/create")
async def create_user(user: UserModel):
    result = userRepo.create_user(user)
    return result


@app.get("/auth")
async def auth_user(user: UserModel):
    print(user)
    return userRepo.auth_user(user)


@app.get("/download/{username}")
async def download_config(username: str):
    file = openvpnService.download_config(username)
    return StreamingResponse(
        iter([file.getvalue()]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={username}.ovpn"},
    )
    # return FileResponse(file.getvalue(), filename=f"{username}.ovpn")


@app.post("/users")
async def create_user(user: User, response: Response):
    if user.username.strip() == "":
        response.status_code = 400
        return {"message": "Username cannot be empty"}
    result = openvpnService.create_user(user)
    response.status_code = 201 if result[0] else 400
    return {"message": result[1]}


@app.get("/revoke/{username}")
async def revoke_user(username: str, response: Response):
    result = openvpnService.revoke_user(username)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.get("/ratify/{username}")
async def ratify_user(username: str, response: Response):
    result = openvpnService.ratify_user(username)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.post("/groups")
async def create_group(group: Group, response: Response):
    if group.name.strip() == "":
        response.status_code = 400
        return {"message": "Group name cannot be empty"}
    result = openvpnService.create_group(group.name)
    response.status_code = 201 if result[0] else 400
    return {"message": result[1]}


@app.get("/groups")
async def groups_list() -> List[Group]:
    return openvpnService.groups_list()


@app.get("/groups/{groupname}")
async def get_group_with_routes(groupname: str) -> Group:
    result = groupRepo.get_group(groupname)
    print(result)
    return map_groups(result)[0]


@app.get("/groupsfull")
async def group_detail() -> List[Group]:
    result = groupRepo.get_groups_with_routes()
    print(result)
    return map_groups(result)


@app.get("/groups/{groupname}/users/{username}")
async def add_user_to_group(username: str, groupname: str, response: Response):
    result = openvpnService.add_user_to_group(username, groupname)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.delete("/groups/{groupname}/users/{username}")
async def delete_user_from_group(username: str, groupname: str, response: Response):
    result = openvpnService.remove_user_from_group(username, groupname)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.delete("/groups/{groupname}")
async def delete_group(groupname: str, response: Response):
    result = openvpnService.delete_group(groupname)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.post("/groups/{groupname}/routes")
async def add_routes_group(groupname: str, routes: List[Route], response: Response):
    result = openvpnService.add_routes_to_group(groupname, routes)
    response.status_code = 201 if result[0] else 404
    return result[1]


@app.delete("/groups/{groupname}/routes")
async def delete_routes_group(groupname: str, routes: List[Route], response: Response):
    result = openvpnService.remove_routes_from_group(groupname, routes)
    response.status_code = 200 if result[0] else 404
    return {"message": result[1]}


@app.get("/groups/{groupname}/users")
async def get_group_users(groupname: str) -> list:
    return openvpnService.get_users_for_group(groupname)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
