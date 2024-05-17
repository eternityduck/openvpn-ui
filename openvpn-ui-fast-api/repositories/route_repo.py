from sqlmodel import Field, Session, select
from sqlmodel import Session
from sqlmodels.route import Route as RouteModel


class RouteRepository:
    session: Session

    def __init__(self, session):
        self.session = session

    def create_route(self, route):
        route = RouteModel(**route.dict())
        self.session.add(route)
        self.session.commit()
        self.session.close()

    def delete_route(self, routename):
        route = self.session.exec(select(RouteModel).where(RouteModel.name == routename)).first()
        self.session.delete(route)
        self.session.commit()
        self.session.close()

