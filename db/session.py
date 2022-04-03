import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists


class DictMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class DBConnection:
    def __init__(self):

        # read params from .env file
        self.engine = create_engine(
            'postgresql://{}:{}@{}:{}/{}'.format(
                os.environ['DB_USER'],
                os.environ['DB_PASSWORD'],
                os.environ['DB_HOST'],
                os.environ['DB_PORT'],
                os.environ['DB_NAME']))
        # Create database if it does not exist.
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Session = sessionmaker(bind=self.engine)
        Base = declarative_base(bind=self.engine)

        class BaseModel(DictMixin, Base):
            __abstract__ = True
            pass

        self.base = BaseModel
        self.conn = self.engine.connect()
        self.session = Session()

    def create_metadata(self):
        self.base.metadata.create_all(self.engine)


load_dotenv()  # load environment variables from .env.
db_instance = DBConnection.Instance()
Base = db_instance.base
conn: Connection = db_instance.conn
session: Session = db_instance.session
