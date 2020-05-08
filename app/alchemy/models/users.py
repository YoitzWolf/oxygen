import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.alchemy.session import SqlAlchemyBase


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    login = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True
    )
    
    public_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, default="./static/images/avatars/av/avatar_00.png")
    
    personal_file = sqlalchemy.Column(
        sqlalchemy.String, 
        unique=True
    )
    
    # premission_level_id = sqlalchemy.Column(
    #     sqlalchemy.Integer, sqlalchemy.ForeignKey("premissions.id"),
    #     default=0
    # )
    # 
    # premission_name = orm.relation("Premission")

    email = sqlalchemy.Column(sqlalchemy.String, unique=True)

    password_hash = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
    last_enter_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    # posts      = orm.relation("Post", back_populates='author')
    # anwers     = orm.relation("", back_populates='author')
    # news       = orm.relation("News", back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User> {self.id} {self.login} {self.email}"


def userFabric(data) -> User:
    user = User()
    return user