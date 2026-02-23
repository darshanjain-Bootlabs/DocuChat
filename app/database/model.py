from app.database.session import Base
from app.database.session import engine
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)

class DocumentCreate(BaseModel):
    filename: str   
