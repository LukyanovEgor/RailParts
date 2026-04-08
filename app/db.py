from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app.config import db_url

engine = create_engine(db_url)

session_maker = sessionmaker(bind=engine)
Base = declarative_base()


if not database_exists(engine.url):
    create_database(engine.url)

def get_db():
    db = session_maker()
    return db
