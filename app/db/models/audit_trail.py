from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class AuditTrail(Base):
    __tablename__ = "audit_trails"

    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    entity_type = Column(String, nullable=False) 
    entity_id = Column(BigInteger, nullable=False)
    action = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
