from sqlalchemy import Column, String, Integer, BigInteger
from .database import Database

class Cars(Database.Base):
    __tablename__ = "Cars"

    url = Column(String, primary_key=True)
    title = Column(String)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(BigInteger)
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(String)