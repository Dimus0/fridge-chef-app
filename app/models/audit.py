from datetime import datetime, timezone
import uuid

from sqlalchemy import UUID, Column, DateTime, String, Text

from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "AuditLog"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
