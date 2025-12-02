from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.application import Application

def get_application_by_id(session: Session, app_id: int):
    return (
        session.query(Application)
        .filter(
            Application.id == app_id,
            Application.deleted_at.is_(None)
        )
        .first()
    )

def create_application(session: Session, application: Application):
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

def soft_delete_application(session: Session, application: Application):
    application.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
