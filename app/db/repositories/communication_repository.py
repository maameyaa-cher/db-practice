from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models.communication_log import CommunicationLog

def get_log_by_id(session: Session, log_id: int):
    return (
        session.query(CommunicationLog)
        .filter(
            CommunicationLog.id == log_id,
            CommunicationLog.deleted_at.is_(None)
        )
        .first()
    )

def create_log(session: Session, log: CommunicationLog):
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

def soft_delete_log(session: Session, log: CommunicationLog):
    log.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
