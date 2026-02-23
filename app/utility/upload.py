import tempfile
from fastapi import APIRouter,UploadFile,File,HTTPException,Request,Depends
from pathlib import Path

from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.model import Document

from app.services.audio_services import text_from_audio
from app.services.ocr_service import text_from_image
from app.services.pdf_util import text_from_pdf

from app.services.vector_service import create_vector_store
from app.services.upload_service import create_document


upload_router = APIRouter()
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg", ".wav", ".mp3", ".m4a"}

@upload_router.post("/")
async def upload_file(request: Request,file: UploadFile = File(...),db: Session = Depends(get_db)):
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if file_extension == ".pdf":
        text = text_from_pdf(await file.read())

    elif file_extension in {".txt"}:
        text = (await file.read()).decode("utf-8")

    elif file_extension in {".png", ".jpg", ".jpeg"}:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(await file.read())
            text = text_from_image(Path(temp_file.name))
            Path(temp_file.name).unlink()

    elif file_extension in {".wav", ".mp3", ".m4a"}:
        text = await text_from_audio(file)

    else:
        raise HTTPException(status_code=400, detail="File Handling Error")
    
    chunks = create_vector_store(text) 
    
    try:
        create_document(
            db, 
            document_name=file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    
    return {"message": f"File '{file.filename}' uploaded successfully with {chunks} chunks."}


@upload_router.get("/get_doc")
async def get_documents(request: Request,db: Session = Depends(get_db)):
    try:
        documents = db.query(Document).all()
        return {"documents": [doc.filename for doc in documents]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    

    