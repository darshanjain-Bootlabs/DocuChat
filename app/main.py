from fastapi import FastAPI,APIRouter
from app.api.routes import router
from app.database.session import engine, Base
from app.database.model import Document

def create_db_and_table():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_table()


app.include_router(router)
@app.get("/")
def read_root():
    return {"Hey Welcome to DocuChat!": "This is a simple RAG Pipline where you can upload any type of document and ask questions related to that document. The system will use the uploaded document as context to answer your questions."}