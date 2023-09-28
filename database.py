from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://postgres:helly@localhost:5432/pharmacy")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """provide db session to path operation functions"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
