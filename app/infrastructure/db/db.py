from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities.models import Base

DATABASE_URL = "postgresql://user:password@db:5432/analyzer"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
