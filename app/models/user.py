
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="Viewer")
    created_at = Column(DateTime, server_default=func.now())
