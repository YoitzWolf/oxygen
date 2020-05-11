import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

from app.alchemy.session import SqlAlchemyBase
from app.alchemy.models.base import Base

class Discussion(SqlAlchemyBase, Base):
    __tablename__ = 'discussions'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    header = sqlalchemy.Column(
        sqlalchemy.String
    )
    
    personal_file = sqlalchemy.Column(
        sqlalchemy.String, 
        unique=True
    )
    
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    
    author = orm.relation("User")

    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
    
    last_update_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    # posts      = orm.relation("Post", back_populates='author')
    answers = orm.relation("Answer", back_populates='discussion')
    answers_cnt = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    
    likes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    dislikes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # news       = orm.relation("News", back_populates='author')

    def __repr__(self):
        return f"<Discussion> {self.id} from: {self.creation_date} last: {self.last_update_date} author: {self.author}"
    
    def init_file(self):
        self.personal_file = f"/{self.header.lower()[:min(2, len(self.header))]}/discussion_{self.id}.json"