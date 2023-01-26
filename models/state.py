#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type
# from models.city  import City


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City',
                          backref='state',
                          cascade='all, delete')

    @property
    def cities(self):
        """ Returns a list of City instances with state_id ==
        current state_id
        """
        from models import storage
        from models.city import City
        filtered_cities = []

        # Returns a dict of class City
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                filtered_cities.append(city)
        return filtered_cities
