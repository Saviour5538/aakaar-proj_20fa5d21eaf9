import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from contextlib import contextmanager
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase

# Read DATABASE_URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# SQLAlchemy engine configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Session factory
SessionLocal = scoped_session(sessionmaker(bind=engine))

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()