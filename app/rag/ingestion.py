import os
from fastapi import HTTPException
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_store import vector_store


# ============================================
#  UPLOAD DOCUMENT
# ============================================
def ingest_document(file_path: str, document_id: int, access_level: int) -> None:
    # Check file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f'Document not found at {file_path}')
    
    # Load the document
    ext = os.path.splitext(file_path)[1].lower()
    loader_class = {'.pdf': PyPDFLoader, '.txt': TextLoader}
    loader = loader_class.get(ext)(file_path)
    if not loader_class:
        raise Exception(f"Unsupported file type: {ext}")
    document = loader.load()
    if not document:
        raise Exception(f"No content extracted from the document")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,           # Smaller chunks for better retrieval
        chunk_overlap=200,         # Overlap to maintain context
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        length_function=len
    )
    chunks = splitter.split_documents(documents=document)
    if not chunks:
        raise Exception("No chunks created from document")
    
    # Add some extra metadata in each chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "document_id": document_id,
            "access_level": access_level,
            "chunk_index": i,
            "source": file_path
        })
    
    # Add metadata+content of every chunk in vector store
    added = vector_store.add_documents(documents=chunks)
    if not added:
        raise HTTPException(status_code=422, detail="Failed to add document to vector store")


# ============================================
#  DELETE DOCUMENT
# ============================================
def remove_document_from_vector_store(doc_id: int):
    try:
        vector_store.delete(where={'document_id': doc_id})
    except Exception as e:
        raise Exception(f"Failed to remove document from vector store: {str(e)}")
