from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.document import DocumentOut, DocumentListOut
from app.models.user import User
from app.models.document import Document
from app.api.deps import require_admin_staff, require_admin
from app.services.document_service import upload_document, search_document, list_all_documents, delete_document


router = APIRouter()


# ============================================
#  ADMIN & STAFF -> UPLOAD DOCUMENT
# ============================================
@router.post('/upload', response_model=DocumentOut)
def upload_doc(
    file: UploadFile = File(...), 
    access_level: int = Form(...), 
    db: Session = Depends(get_db), 
    user: User = Depends(require_admin_staff)
):
    return upload_document(file, access_level, db, user)


# ============================================
# ADMIN & STAFF -> SEARCH DOCUMENTS
# ============================================
@router.get('/search_docs/{doc_id}', response_model=DocumentOut)
def search_documents(
    doc_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(require_admin_staff)
):
    return search_document(doc_id, db, user)


# ============================================
# ADMIN & STAFF -> LIST DOCUMENTS
# ============================================
@router.get('/all_docs', response_model=DocumentListOut)
def list_documents(
    db: Session = Depends(get_db), 
    user: User = Depends(require_admin_staff)
):
    return list_all_documents(db, user)


# ============================================
#  ADMIN -> HARD DELETE DOCUMENT
# ============================================
@router.delete('/delete/{doc_id}')
def delete_doc(
    doc_id: int, 
    db: Session = Depends(get_db), 
    _: User = Depends(require_admin)
):
    return delete_document(doc_id, db)
