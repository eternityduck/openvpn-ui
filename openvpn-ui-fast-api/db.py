from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodels.user import User as UserModel
from sqlmodels.group import Group as GroupModel
from sqlmodels.route import Route as RouteModel


class DbContext:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:////opt/db/openvpn-ui.db",
            echo=True,
            connect_args={"check_same_thread": False},
        )
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            return session
