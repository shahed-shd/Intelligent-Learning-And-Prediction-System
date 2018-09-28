from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from .miscellaneous import get_next_free_id, get_sha256_hex_digest


Base = declarative_base()

user_estimator_association_table = Table('users_estimators_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('estimator_id', Integer, ForeignKey('estimators.id')),
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint('user_id', 'estimator_id', name='uix_1')
)


class User(Base):
    __table__ = Table('users', Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50), nullable=False, unique=True),
                    Column('fullname', String(50)),
                    Column('short_bio', String(255)),
                    Column('password_hash', String(64), nullable=False))

    estimators = relationship('Estimator', secondary=user_estimator_association_table, back_populates='users')

    def __repr__(self):
        return "<User(id={}, username={})>".format(self.id, self.username)


class Estimator(Base):
    __table__ = Table('estimators', Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('title', String(50)),
                    Column('type', String(25)),
                    Column('n_features', Integer),
                    Column('n_targets', Integer),
                    Column('build_datetime', DateTime))

    users = relationship('User', secondary=user_estimator_association_table, back_populates='estimators')

    def __repr__(self):
        return "<Estimator(id={}, title={}, type={})>".format(self.id, self.title, self.type)


class DB(object):
    def __init__(self, **kwargs):
        engine = create_engine('mysql+pymysql://root:abcd1234@localhost/ILPS', echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.engine = engine


    def create_new_session(self):
        self.session.close()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def add_user(self, user):
        # if user.id == None
        if not user.id:
            user.id = get_next_free_id(self.engine, user.__table__.name, 'id')

        self.session.add(user)
        self.session.commit()


    def add_user_by_attributes(self, *, user_id, username, fullname, short_bio, raw_password):
        user = User()

        user.id = user_id if user_id else get_next_free_id(self.engine, user.__table__.name, 'id')
        user.username = username
        user.fullname = fullname
        user.short_bio = short_bio
        user.password_hash = get_sha256_hex_digest(raw_password)

        self.session.add(user)
        self.session.commit()


    def add_estimator(self, estimator):
        # if estimator.id == None
        if not estimator.id:
            estimator.id = get_next_free_id(self.engine, estimator.__table__.name, 'id')

        self.session.add(estimator)
        self.session.commit()


    def get_users(self):
        res = self.session.query(User)
        return res


    def get_user_by_id(self, userid):
        user = self.session.query(User).filter_by(id=userid).one()
        return user


    def get_user_by_username(self, username):
        try:
            user = self.session.query(User).filter_by(username=username).one()
        except:
            user = None

        return user


    def get_user_by_fullname(self, userfullname):
        try:
            user = self.session.query(User).filter_by(fullname=userfullname).one()
        except:
            user = None

        return user


    def delete_user(self, user):
        self.session.delete(user)
        self.session.commit()


    def update_user(self, ob, attr_val_dict):
        for key, val in attr_val_dict.items():
            setattr(ob, key, val)
        self.session.commit()

    def get_estimators(self):
        res = self.session.query(Estimator)
        return res


    def get_estimator_by_id(self, estimator_id):
        estimator = self.session.query(Estimator).filter_by(id=estimator_id).one()
        return estimator


    def get_users_estimators_access_list(self):
        res = self.session.query(User, Estimator).filter(User.estimators).all()
        return res
