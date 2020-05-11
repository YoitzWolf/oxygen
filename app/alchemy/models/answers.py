import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from app.alchemy.session import SqlAlchemyBase
from app.alchemy.models.base import Base

class Answer(SqlAlchemyBase, Base):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    text = sqlalchemy.Column(
        sqlalchemy.String
    )   
    
    discussion_id = sqlalchemy.Column(
       sqlalchemy.Integer, sqlalchemy.ForeignKey("discussions.id")
    )
    
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    
    author = orm.relation("User")
    discussion = orm.relation("Discussion")
    
    popularity = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
    
    last_update_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Answer> {self.id} from: {self.header} color: #{self.color} author: {self.author}"
    
    def init_file(self):
        self.personal_file = f"/{self.header.lower()[:min(2, len(self.header))]}/discussion_{self.id}.json"