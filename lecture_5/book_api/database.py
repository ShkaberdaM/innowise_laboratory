# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database (creates the file books.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a factory of sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basic class for models
Base = declarative_base()