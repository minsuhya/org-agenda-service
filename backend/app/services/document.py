from sqlmodel import Session, select
from app.models.document import Document
from app.schemas.org import OrgContent
from typing import List, Optional

def get_document(db: Session, document_id: int) -> Optional[Document]:
    statement = select(Document).where(Document.id == document_id)
    return db.exec(statement).first()

def get_user_documents(db: Session, user_id: int) -> List[Document]:
    statement = select(Document).where(Document.user_id == user_id)
    return db.exec(statement).all()

def create_document(db: Session, title: str, content: str, user_id: int) -> Document:
    db_document = Document(
        title=title,
        content=content,
        user_id=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def update_document(db: Session, document_id: int, title: str = None, content: str = None) -> Optional[Document]:
    db_document = get_document(db, document_id)
    if db_document:
        if title:
            db_document.title = title
        if content:
            db_document.content = content
        db.commit()
        db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    db_document = get_document(db, document_id)
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False 