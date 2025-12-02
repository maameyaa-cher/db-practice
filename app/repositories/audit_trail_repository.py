from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.audit_trail import AuditTrail

def create_audit_entry(session: Session, entry: AuditTrail):
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

def soft_delete_audit_entry(session: Session, entry: AuditTrail):
    entry.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
