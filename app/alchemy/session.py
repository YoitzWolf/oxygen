import sqlalchemy as alchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file, echo=False):

	global __factory

	if __factory:
		return "Some poblems with Factory"

	if not db_file or not db_file.strip():
		raise Exception(f"Problems with file {db_file}")

	conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False' # adress
	print(f"TRYING TO CONNECT TO {conn_str} DATABASE")

	engine = alchemy.create_engine(conn_str, echo=echo)
	__factory = orm.sessionmaker(bind=engine)

	from . import __all_models

	SqlAlchemyBase.metadata.create_all(engine)

	return "OK"


def create_session() -> Session:
	global __factory
	return __factory()
