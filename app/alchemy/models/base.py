
import sqlalchemy
from app.alchemy.session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Base(SerializerMixin):
    pass