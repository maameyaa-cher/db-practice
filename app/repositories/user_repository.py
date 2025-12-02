from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_id(session: Session, user_id: int):
    return (
        session.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        )
        .first()
    )

def get_user_by_email(session: Session, email: str):
    return (
        session.query(User)
        .filter(
            User.email == email,
            User.deleted_at.is_(None)
        )
        .first()
    )

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def soft_delete_user(session: Session, user: User):
    user.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
