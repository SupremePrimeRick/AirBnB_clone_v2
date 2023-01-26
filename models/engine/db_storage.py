#!/usr/bin/python3
""" New storage engine for database storage """
from datetime import datetime
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.review import Review
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """ Creates an instance of DBStorage """

        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB),
            pool_pre_ping=True)

        env = getenv('HBNB_ENV')
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session all objs
        depending on the class name 'cls'
        """

        cls_dict = {}
        if cls is None:
            classes = [State, City, User]
            for clas in classes:
                objs = self.__session.query(clas).all()
                if objs:
                    for obj in objs:
                        key = obj.__class__.__name__+'.'+obj.id
                        cls_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__+'.'+obj.id
                cls_dict[key] = obj

        return cls_dict

    def new(self, obj):
        """ Add the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current db session """
        try:
            self.__session.commit()
        except Exception as err:
            print(err)

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            clas = type(obj)
            self.__session.query(clas).filter(clas.id == obj.id).delete()

    def reload(self):
        """ Creates all tables in the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
