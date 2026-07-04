import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class ShoppingCart(Base):
    __tablename__ = "ShoppingCart"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(100), nullable=False)
    is_bought = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="shopping_items")