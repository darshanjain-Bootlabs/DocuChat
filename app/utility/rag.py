from fastapi import APIRouter,Request
from app.services.rag_service import generate_response


Rag_service_router = APIRouter()

@Rag_service_router.post("/rag")
def rag_service(request: Request,query: str):
    return generate_response(query)
        
