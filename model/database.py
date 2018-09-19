from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __table__ = Table('users', Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50), nullable=False, unique=True),
                    Column('fullname', String(50)),
                    Column('short_bio', String(255)),
                    Column('password_hash', String(64), nullable=False))

    def __repr__(self):
        return "<User(id={}, username={})>".format(self.userid, self.username)


class Estimator(Base):
    __table__ = Table('estimators', Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('title', String(50)),
                    Column('type', String(25)),
                    Column('n_features', Integer),
                    Column('n_targets', Integer),
                    Column('build_datetime', DateTime))

    def __repr__(self):
        return "<Estimator(id={}, title={}, type={})>".format(self.id, self.title, self.type)




class DB(object):
    def __init__(self, **kwargs):
        engine = create_engine('mysql+pymysql://root:abcd1234@localhost/ILPS', echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
