from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String, nullable=False)
    role = Column(String)
    is_active = Column(Boolean, server_default="true")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
