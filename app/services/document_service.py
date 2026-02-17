import os
import shutil
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.rag.ingestion import ingest_document
from app.rag.ingestion import remove_document_from_vector_store


# ============================================
#  ADMIN & STAFF -> UPLOAD DOCUMENT
# ============================================
def upload_document(file: UploadFile, access_level: int, db: Session, user: User):
    ALLOWED_EXTENSIONS = ['.pdf', '.txt']
    
    # Extension Allowed or Not
    ext = os.path.splitext(file.filename)[1].lower()
    if not ext in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f'{ext} file Not Allowed')
    
    # visible to which users
    if access_level not in [0, 1, 2]:
        raise HTTPException(status_code=400, detail=f'Access level for user, staffs and admins')

    # Staff can not upload admin only document
    if user.role == 1 and access_level == 0:
        raise HTTPException(status_code=403, detail='Staff can not upload admin only document')
    
    existing = db.query(Document).filter(Document.filename == file.filename).first()
    if existing:
        raise HTTPException(status_code=400, detail='File already exists')
    
    # create destination location
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(name=UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    # create database record
    new_doc = Document(filename=file.filename, filepath=file_path, access_level=access_level, uploaded_by=user.id)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # CREATE VECTOR STORE WHILE UPLOAD DOCUMENT
    ingest_document(file_path, new_doc.id, access_level)

    return new_doc


# ============================================
# ADMIN & STAFF -> SEARCH DOCUMENTS
# ============================================
def search_document(doc_id: int, db: Session, user: User):
    query = db.query(Document).filter(Document.is_deleted == False, Document.id == doc_id)
    if user.role == 1:
        query = query.filter(Document.access_level != 0)
    doc = query.first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"'{doc_id}' Not Found")
    return doc


# ============================================
# ADMIN & STAFF -> LIST DOCUMENTS
# ============================================
def list_all_documents(db: Session, user: User):
    query = db.query(Document).filter(Document.is_deleted == False).order_by(Document.created_at.desc())
    if user.role == 1:
        query = query.filter(Document.access_level != 0)
    docs = query.all()
    total = query.count()
    if not docs:
        raise HTTPException(status_code=404, detail='No document Not Found')
    return {
        'total': total,
        'list_documents': docs
    }


# ============================================
#  ADMIN -> HARD DELETE DOCUMENT
# ============================================
def delete_document(doc_id: int, db: Session):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='Document Not Found')
    
    # Delete file from filesystem
    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)

    # delete database record
    db.delete(doc)
    db.commit()

    # DELETE DOCUMENT FROM VECTOR STORE
    remove_document_from_vector_store(doc_id)
    
    return {'message': f'{doc.filename} has been deleted successfully'}
