import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
import flask
from app.alchemy.session import SqlAlchemyBase

class Answer(SqlAlchemyBase):
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
        
    def get_author_field(self):
        print(self.author, "DADADA")
        return flask.render_template(
            "block-templates/userfield.html",
            attr=self.author,
            )
    
    def getBeautifulDate(self):
        data = (str(self.last_update_date)).split()
        
        data[0] = data[0].split('-')
        data[1] = data[1].split(':')[:2]
        
        return '.'.join(data[0]) + " at " + ":".join(data[1][:2])
        