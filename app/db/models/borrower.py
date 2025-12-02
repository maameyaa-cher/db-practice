from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    email = Column(String)
    phone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String)
    date_of_birth = Column(String)
    credit_score = Column(BigInteger)
    credit_report_url = Column(String)
    ssn_last_4 = Column(String)
    income_annual = Column(String)
    employment_status = Column(String)
    linked_user = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
