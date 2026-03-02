import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from app.utility.text_split import split_text
from langchain_chroma import Chroma
import chromadb

import time
from chromadb.errors import ChromaError

CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma") 
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_chroma_client():
    retries = 5
    while retries > 0:
        try:
            client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
            client.heartbeat()
            return client
        except Exception as e:
            print(f"Chroma not ready yet... retrying ({retries} left). Error: {e}")
            time.sleep(3)
            retries -= 1
    raise Exception("Could not connect to ChromaDB after several retries.")


persistent_client = get_chroma_client()

vector_store = Chroma(
    client=persistent_client,
    collection_name="Docu_chat",
    embedding_function=embedding,
)

def create_vector_store(text: list) -> int:
    if isinstance(text, list):
        text = "\n".join(text)

    chunks = split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    vector_store.add_documents(docs)
    return len(chunks)

def similarity_search(query: str, k: int = 3) -> list[Document]:
    return vector_store.max_marginal_relevance_search(query, k=k)