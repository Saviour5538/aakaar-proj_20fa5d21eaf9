from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.models import Document
from database.config import get_db
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/api/documents")

class DocumentResponse(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    filename: str
    status: str
    chunk_count: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

@router.post("/upload", operation_id="upload_document", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    
    try:
        # Simulate processing the uploaded document
        new_document = Document(
            user_id=current_user.id,
            filename=file.filename,
            status="processing",
            chunk_count=0,
            created_at=datetime.utcnow()
        )
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[DocumentResponse], operation_id="list_documents")
async def list_documents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@router.delete("/{id}", operation_id="delete_document", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    document = db.query(Document).filter(Document.id == id, Document.user_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    try:
        db.delete(document)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))