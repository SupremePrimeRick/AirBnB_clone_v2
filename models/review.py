<<<<<<< HEAD
#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60),
                      ForeignKey('places.id'),
                      nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
=======
#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60),
                      ForeignKey('places.id'),
                      nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
>>>>>>> c2fd32adcec740605a2ebf6f6a2687b51aede372
