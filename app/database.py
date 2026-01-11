import os

from load_dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


# database info
POSTGRE_SQL_USER=os.getenv("POSTGRE_SQL_USER")
POSTGRE_SQL_PASSWORD=os.getenv("POSTGRE_SQL_PASSWORD")
POSTGRE_SQL_HOST=os.getenv("POSTGRE_SQL_HOST")
POSTGRE_SQL_DB=os.getenv("POSTGRE_SQL_DB")

SQLALCHEMY_DB_URL = f"postgresql://{POSTGRE_SQL_USER}:{POSTGRE_SQL_PASSWORD}@{POSTGRE_SQL_HOST}/{POSTGRE_SQL_DB}"   # SQLALCHEMY database URL

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DB_URL)   # create the SQLAlchemy engine
SessionLocal = sessionmaker(        # create a configured "Session" class
    autocommit=False,               # disable autocommit mode, need to call session.commit() to save changes
    autoflush=False,                # disable autoflush mode, need to call session.flush() to flush changes to the database
    bind=engine                     # bind the engine to the session
) 
Base = declarative_base()           # create a base class for declarative class definitions, it will be inherited by all ORM models

# Dependency to get DB session
def get_db():
    db = SessionLocal()              # create a new database session
    try:
        yield db                     # yield the session to be used in the request
    finally:
        db.close()                   # close the session after the request is done

