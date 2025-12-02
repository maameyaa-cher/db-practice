from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CommunicationLog(Base):
    __tablename__ = "communication_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    application_id = Column(BigInteger, ForeignKey("applications.id"), nullable=True)
    borrower_id = Column(BigInteger, ForeignKey("borrowers.id"), nullable=True)
    sender_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    sender_type = Column(String)
    message = Column(String)
    message_type = Column(String)
    channel = Column(String)  
    ai_model = Column(String) 
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
