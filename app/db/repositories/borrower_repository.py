from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models.borrower import Borrower

def get_borrower_by_id(session: Session, borrower_id: int):
    return (
        session.query(Borrower)
        .filter(
            Borrower.id == borrower_id,
            Borrower.deleted_at.is_(None)
        )
        .first()
    )

def create_borrower(session: Session, borrower: Borrower):
    session.add(borrower)
    session.commit()
    session.refresh(borrower)
    return borrower

def soft_delete_borrower(session: Session, borrower: Borrower):
    borrower.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
