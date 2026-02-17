from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Initialize vector store
vector_store = Chroma(
    collection_name='company_documents',
    embedding_function=HuggingFaceEmbeddings(),
    persist_directory='chroma_db'
)


def all_docs():
    """Get all documents from vector store"""
    results = vector_store.get(include=["documents", "metadatas"])
    documents = [
        {
            "content": content,
            "metadata": metadata
        }
        for content, metadata in zip(results["documents"], results["metadatas"])
    ]

    return {
        "total": len(documents),
        "documents": documents
    }
