from sqlmodel import Field, Session, select
from sqlmodel import Session
from sqlmodels.group import Group as GroupModel


class GroupRepository:
    session: Session

    def __init__(self, session):
        self.session = session

    def create_group(self, group):
        group = GroupModel(**group.dict())
        self.session.add(group)
        self.session.commit()
        self.session.close()

    def delete_group(self, groupname):
        group = self.session.exec(select(GroupModel).where(GroupModel.name == groupname)).first()
        self.session.delete(group)
        self.session.commit()
        self.session.close()