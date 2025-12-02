from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, index=True)

    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False, index=True)
    application_id = Column(BigInteger, ForeignKey("applications.id"), nullable=False, index=True)
    borrower_id = Column(BigInteger, ForeignKey("borrowers.id"), nullable=True, index=True)
    uploaded_by = Column(BigInteger, ForeignKey("users.id"))
    file_name = Column(String)
    file_type = Column(String)
    file_size = Column(BigInteger)
    storage_url = Column(String)
    storage_provider = Column(String)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
