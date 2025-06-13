from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


CONFIG = dotenv_values(".env")

class Database:
    __DATABASE_URL = CONFIG["DATABASE_URL"]
    engine = create_engine(__DATABASE_URL)
    session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    Base = declarative_base()


    @classmethod
    def setup(cls):
        cls.Base.metadata.create_all(bind=cls.engine)


    @classmethod
    def get_driver(cls):
        return cls.session()