"""
Database configuration and session management
"""
from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

# In-memory SQLite database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)


def init_hero_db() -> None:
    """Initialize the hero database tables"""
    SQLModel.metadata.create_all(engine)


def get_hero_session() -> Generator[Session, None, None]:
    """Get a database session"""
    with Session(engine) as session:
        yield session