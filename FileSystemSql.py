from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

import FileSystemClasses

Base = declarative_base()


class FileSql(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    md5 = Column(String)
    filename = Column(String)
    size = Column(Integer)
    atime = Column(Integer)
    mtime = Column(Integer)
    ctime = Column(Integer)
    extension = Column(String)

    def __init__(self, file_obj=None):
        if file_obj and file_obj.__class__ == FileSystemClasses.File:
            self.json_data = file_obj.__dict__
            self.load_from_simple_json()

    def load_from_simple_json(self):
        for key in ('path', 'size', 'atime', 'mtime', 'ctime', 'filename', 'md5', 'extension'):
            self.__dict__[key] = self.json_data[key]

    def add_to_db(self, session):

        if not self.id:
            session.add(self)
            session.commit()


def create_database(db_name):

    engine = create_engine('sqlite:///{}.sqlite'.format(db_name))
    sessionm = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    return sessionm
