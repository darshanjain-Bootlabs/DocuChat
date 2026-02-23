from fastapi import FastAPI, APIRouter
from app.utility.upload import upload_router
from app.utility.rag import Rag_service_router

router = APIRouter()
router.include_router(upload_router, prefix="/upload", tags=["Upload"])
router.include_router(Rag_service_router, prefix="/rag", tags=["RAG Service"])
