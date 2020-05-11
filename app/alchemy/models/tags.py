import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from app.alchemy.session import SqlAlchemyBase

class Tag(SqlAlchemyBase):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    header = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True
    )
    
    color = sqlalchemy.Column(
        sqlalchemy.String
    )
    
    bg_color = sqlalchemy.Column(
        sqlalchemy.String
    )
    
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    
    author = orm.relation("User")
    
    popularity = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
    
    last_using_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Tag> {self.id} from: {self.header} bg-color: {self.bg_color} color: {self.color} author: {self.author}"
    
    def to_dict(self):
        return {
            "type": "<Tag>",
            "repr": self.__repr__(),
            "id": self.id,
            "header": self.header,
            "bg_color": self.bg_color,
            "color": self.color,
            "author_id": self.author_id
        }