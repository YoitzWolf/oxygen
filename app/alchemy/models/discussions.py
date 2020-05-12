import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

from app.alchemy.session import SqlAlchemyBase
from app.alchemy.models.base import Base

class Discussion(SqlAlchemyBase):
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
        self.personal_file = f"/discussion_{self.id}.json"
    
    def get_mrk_file(self):
        return f"./static/databases/frm_api-files/discussion_{self.id}.md"
    
    def get_tags(self):
        from app.alchemy import session as Session
        from app.alchemy.models.tags import Tag
        from json import loads
        session = Session.create_session()
        data = {}
        tags = []
        with open(f"./static/databases/frm_api-files{self.personal_file}", "r") as file:
            data = loads(file.read())
        q = session.query(Tag)
        for i in data['tag_ids']:
            tags.append(q.filter(Tag.id==i).first())
        print(tags)
        return tags
    
    def getBeautifulDate(self):
        data = (str(self.last_update_date)).split()
        
        data[0] = data[0].split('-')
        data[1] = data[1].split(':')[:2]
        
        return '.'.join(data[0]) + " at " + ":".join(data[1][:2])
    
    def to_dict(self):
        return {
            'personal_file': f"/discussion_{self.id}.json"
        }
    
    def to_dict_beauty(self):
        return {
            'id': self.id,
            'author': self.author,
            "header": self.header,
            'last_update': self.getBeautifulDate(),
            'answers': len(self.answers),
            'tags': self.get_tags(),
            'personal_file': f"/discussion_{self.id}.json"
        }
    
    def tagsfilter(self, tags):
        res = []
        from json import loads
        fullway = f"./static/databases/frm_api-files{self.personal_file}"
        with open(fullway, 'r') as file:
            data = loads(file.read())
            for tag in tags:
                if str(tag['id']) in data['tag_ids']: res.append(tag)
            file.close()
        print(res, "Filterd", data['tag_ids'])
        return res
    
    def set_file(self, data):
        dct = {
            "id": self.id,
            "header": self.header,
            "md-file": f"discussion_{self.id}.md",
            "tag_ids": data['tags']
        }
        from json import dumps
        fullway = f"./static/databases/frm_api-files{self.personal_file}"
        with open(fullway, 'w') as file:
            file.write(dumps(dct))
            file.close()
            
        fullway = f"./static/databases/frm_api-files/discussion_{self.id}.md"
        with open(fullway, 'w') as file:
            file.write(data['markdown'])
            file.close()
        print(f"Created file for {self} in {fullway}")
        