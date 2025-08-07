from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
# from dotenv import load_dotenv

# load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "postgresql://tor_user:your_secure_password@localhost:5432/tor_stats_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()