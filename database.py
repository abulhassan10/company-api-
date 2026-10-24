from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:2310@localhost:5432/company_api"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()