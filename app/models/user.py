import uuid
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "User"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    username = Column(String(255),nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255),nullable=False)

    recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")
