from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from .config import config

Base=declarative_base()

engine=create_engine(url=config.DB_CONNECTION)

LocalSession=sessionmaker(bind=engine)

def get_db():
    session=LocalSession()
    try:
        yield session
    finally:
        session.close()