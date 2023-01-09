#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import (Column,
                        String,
                        ForeignKey,
                        Integer,
                        Float)
from models import storage_type
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table


if storage_type == 'db':
    metadata = Base.metadata
    place_amenity = Table('place_amenity', metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 nullable=False,
                                 primary_key=True),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 nullable=False,
                                 primary_key=True))

    class Place(BaseModel, Base):
        """ A place to stay """
        __tablename__ = 'places'
        city_id = Column(String(60),
                         ForeignKey('cities.id'),
                         nullable=False)

        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)

        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)

        number_bathrooms = Column(Integer,
                                  nullable=False,
                                  default=0)

        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship('Review',
                               backref='place',
                               cascade='all, delete')
        amenities = relationship('Amenity',
                                 secondary=place_amenity,
                                 viewonly=False,
                                 backref='place_amenities')
else:
    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    @property
    def reviews(self):
        """"""
        from models import storage
        revs = storage.all(Review)
        reviews = []
        for rev in revs.values():
            if self.id == rev.place_id:
                reviews.append(rev)
        return reviews

    @property
    def amenities(self):
        """Returns a list of amenity instances based on
        the attribute amenity_ids that contains all
        Amenity.id linked to the Place"""
        from models import storage
        filtered_amenities = []
        all_amen = storage.all(Amenity)
        for amenity in all_amen.values():
            if ameneity.id in self.amenity_ids:
                filtered_amenities.append(amenity)
        return filtered_amenities

    @amenities.setter
    def amenities(self, obj):
        """Append method that handles adding Amenity.id
        to the attribute amenity_ids. Accepts only Amenity
        object, otherwise do nothing"""
        if obj:
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
