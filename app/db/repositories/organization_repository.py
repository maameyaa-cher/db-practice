from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models.organization import Organization

def get_organization_by_id(session: Session, org_id: int):
    return (
        session.query(Organization)
        .filter(
            Organization.id == org_id,
            Organization.deleted_at.is_(None)
        )
        .first()
    )

def create_organization(session: Session, org: Organization):
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

def soft_delete_organization(session: Session, org: Organization):
    org.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
