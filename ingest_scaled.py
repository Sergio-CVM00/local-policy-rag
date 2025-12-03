import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuration
DATA_PATH = "./data"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "policies"
EMBEDDING_MODEL = "nomic-embed-text"

def main():
    # 1. Load Documents
    print("Loading documents...")
    # glob="**/*.md" allows it to look in subfolders too
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader)
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} documents.")

    # 2. Advanced Chunking
    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # Size of each chunk (characters)
        chunk_overlap=200,     # Overlap to keep context between chunks
        separators=["\n\n", "\n", " ", ""] # Try to split by paragraph first
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Initialize Embeddings (Ollama)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # 4. Batch Process & Store
    # LangChain handles batching automatically here
    print("Vectorizing and storing in ChromaDB (this may take time on CPU)...")
    
    # This automatically persists to disk in the DB_PATH
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH
    )
    
    print("Ingestion complete! Database updated.")

if __name__ == "__main__":
    main()