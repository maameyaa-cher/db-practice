from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(BigInteger, primary_key = True)
    name = Column(String, nullable = False)
    created_at = Column(DateTime, server_default = func.now())
    updated_at = Column(DateTime, server_default = func.now(), onupdate = func.now())
    deleted_at = Column(DateTime, nullable = True)