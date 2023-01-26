<<<<<<< HEAD
#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class Amenity(BaseModel):
    name = ""
=======
#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ''
>>>>>>> c2fd32adcec740605a2ebf6f6a2687b51aede372
