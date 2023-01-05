#!/usr/bin/python3
""" New storage engine for database storage """
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


classes = {'State':State, 'User': User, 'City':City, 
            'Amenity':Amenity, 'Place':Place, 'Review':Review}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """ Creates an instance of DBStorage """
        
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HBNB_MYSQL_USER,
                                            HBNB_MYSQL_PWD,
                                            HBNB_MYSQL_HOST,
                                            HBNB_MYSQL_DB),
                                            pool_pre_ping=True)
    #if HBNB_ENV == 'test':
        #Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session all objs
        depending on the class name 'cls'
        """
        # Session = sessionmaker(bind=self.__engine)
        # self.__session = Session()

        if cls is not None:
            cls_dict = {}
            for obj in self.__session.query(cls).all():
                key = f"{cls}.{obj.id}"
                cls_dict.update({key:obj})
        else:
            cls_dict = {}
            for clas in classes.values():
                for obj in self.__session.query(clas).all():
                    key = f"{cls}.{obj.id}"
                    cls_dict.update({key:obj})
        return cls_dict
                
    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current db session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            clas = type(obj)
            self.__session.query(clas).filter(clas.id == obj.id).delete()

    def reload(self):
        """ Creates all tables in the database """

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()
