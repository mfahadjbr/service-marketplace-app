from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./service_marketplace.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get DB session
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session