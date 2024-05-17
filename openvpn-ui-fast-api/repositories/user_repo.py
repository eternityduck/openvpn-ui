from sqlmodel import Field, Session, select

from config import OPENVPN_PASSWORD_AUTH
from sqlmodels.user import User as UserModel
from utils.utils import hash_password, check_password


class UserRepository:
    session: Session

    def __init__(self, session):
        self.session = session

    def create_user(self, user):
        user = UserModel(**user.dict())
        if OPENVPN_PASSWORD_AUTH:
            user.password = hash_password(user.password)
        self.session.add(user)
        self.session.commit()
        self.session.close()

    def auth_user(self, user):
        user_model = self.session.exec(select(UserModel).where(UserModel.username == user.username)).first()
        print(user_model)
        if user_model is None:
            return None
        if not check_password(user.password, user_model.password):
            return "not authorized"
        self.session.close()
        return "Authorized"

    def change_revocation_status(self, username):
        user_model = self.session.exec(select(UserModel).where(UserModel.username == username)).first()
        user_model.revoked = not user_model.revoked
        self.session.commit()
        self.session.close()

    def is_revoked(self, username):
        user_model = self.session.exec(select(UserModel).where(UserModel.username == username)).first()
        return user_model.revoked