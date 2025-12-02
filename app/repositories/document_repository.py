from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.document import Document

def get_document_by_id(session: Session, doc_id: int):
    return (
        session.query(Document)
        .filter(
            Document.id == doc_id,
            Document.deleted_at.is_(None)
        )
        .first()
    )

def create_document(session: Session, doc: Document):
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

def soft_delete_document(session: Session, doc: Document):
    doc.deleted_at = datetime.now(datetime.timezone.utc)
    session.commit()
