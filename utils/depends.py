from fastapi import Depends, HTTPException
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from models.db_engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
