from sqlalchemy import Column, BigInteger, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False, index=True)
    borrower_id = Column(BigInteger, ForeignKey("borrowers.id"), nullable=False, index=True)
    loan_officer_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    loan_amount = Column(Numeric)
    loan_type = Column(String)
    loan_purpose = Column(String)
    property_address_line1 = Column(String)
    property_address_line2 = Column(String)
    property_city = Column(String)
    property_state = Column(String)
    property_postal_code = Column(String)
    property_country = Column(String)
    employment_income_annual = Column(Numeric)
    employment_status = Column(String)
    application_status = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
