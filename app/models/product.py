from datetime import datetime, timezone
import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Text,DateTime,Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "Product"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id", ondelete="CASCADE"), nullable=True)
    product_name = Column(String(),nullable=False)
    expiration_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="products")