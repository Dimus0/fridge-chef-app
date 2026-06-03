from datetime import datetime, timezone
import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Text,DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Recipe(Base):
    __tablename__ = "Recipe"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id", ondelete="CASCADE"), nullable=True)
    
    title = Column(String(244), nullable=False)
    ingredients = Column(Text, nullable=False)
    instruction = Column(Text, nullable=False)
    prep_time = Column(Integer)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recipes")