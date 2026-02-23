from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from app.utility.text_split import split_text
from langchain_chroma import Chroma


### Plan for vector_service.py
#Create a Vector Database from a list of documents
#inject Documnet funtionality here
#which contain text_split and then create vector database from that text
#embedding is done in vector_store (we use sentence transformer for that)
BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(collection_name="Docu_chat", embedding_function=embedding, persist_directory=str(CHROMA_DIR))

def create_vector_store(text: list) -> int:
    if isinstance(text, list):
        text = "\n".join(text)

    chunks = split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector_store.add_documents(docs)
    return len(chunks)


def similarity_search(query: str, k: int =3) -> list[Document]:
    return vector_store.max_marginal_relevance_search(query, k=k)