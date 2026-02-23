from app.database.model import Document
from sqlalchemy.orm import Session

def create_document(db: Session, document_name: str):
    db_document = Document(filename=document_name)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document