from sqlmodel import Field, Session, select
from sqlmodel import Session
from sqlmodels.group import Group as GroupModel
from sqlmodels.route import Route as RouteModel


class GroupRepository:
    session: Session

    def __init__(self, session):
        self.session = session

    def create_group(self, group_name):
        group = GroupModel(name=group_name)
        self.session.add(group)
        self.session.commit()
        self.session.close()

    def delete_group(self, group_name):
        group = self.session.exec(
            select(GroupModel).where(GroupModel.name == group_name)
        ).first()
        self.session.delete(group)
        self.session.commit()
        self.session.close()

    def get_groups(self):
        return self.session.exec(select(GroupModel)).all()

    def get_groups_with_routes(self):
        query = select(GroupModel, RouteModel).join(RouteModel, isouter=True)
        result = self.session.exec(query).all()
        return result

    def get_group(self, group_name):
        return self.session.exec(
            select(GroupModel, RouteModel)
            .where(GroupModel.name == group_name)
            .join(RouteModel, isouter=True)
        ).all()
