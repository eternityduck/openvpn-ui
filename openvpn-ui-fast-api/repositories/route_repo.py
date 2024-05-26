from typing import List, Tuple

from sqlmodel import select, Session
from sqlmodels.route import Route as RouteModel
from sqlmodels.group import Group as GroupModel


class RouteRepository:
    session: Session

    def __init__(self, session):
        self.session = session

    def delete_routes(self, routes: List[Tuple[str, str]]):
        for route in routes:
            self.session.delete(route)
        self.session.commit()
        self.session.close()

    def get_routes_by_group_name(self, group_name):
        group = self.session.exec(
            select(GroupModel).where(GroupModel.name == group_name)
        ).first()
        return group.routes

    def add_routes_to_group(self, group_name, routes: List[Tuple[str, str]]):
        group_id = (
            self.session.exec(select(GroupModel).where(GroupModel.name == group_name))
            .first()
            .id
        )
        route_models = [
            RouteModel(mask=route[1], address=route[0], group_id=group_id)
            for route in routes
        ]
        self.session.add_all(route_models)
        self.session.commit()
        self.session.close()

    def remove_routes_grom_group(self, group_name, routes: List[Tuple[str, str]]):
        group_id = (
            self.session.exec(select(GroupModel).where(GroupModel.name == group_name))
            .first()
            .id
        )
        for route in routes:
            route = select(RouteModel).where(RouteModel.address == route[0],
                                             RouteModel.mask == route[1],
                                             RouteModel.group_id == group_id)
            result = self.session.exec(route).first()
            self.session.delete(result)
        self.session.commit()
        self.session.close()
