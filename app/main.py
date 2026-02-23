from fastapi import FastAPI,APIRouter
from app.api.routes import router

app = FastAPI()

app.include_router(router)
# @app.get("/")
# def read_root():
#     return {"Hey Welcome to DocuChat!": "This is a simple RAG Pipline where you can upload any type of document and ask questions related to that document. The system will use the uploaded document as context to answer your questions."}