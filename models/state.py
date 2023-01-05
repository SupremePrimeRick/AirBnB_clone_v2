#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type

class State(BaseModel):
    """ State class """

    __tablename__ = 'states'
    

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', 
                                backref='State', 
                                cascade='all, delete')

    else:
        name = ""
        
        @property
        def cities(self):
            """ Returns a list of City instances with state_id ==
            current state_id
            """
            from models import storage
            filtered_cities = []

            # Returns a dict of class City
            cities = storage.all(City)
            for city in cities:
                if city.state_id == self.id:
                    filtered_cities.append(city)

            return filtered_cities
        

