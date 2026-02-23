from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return text_splitter.split_text(text)