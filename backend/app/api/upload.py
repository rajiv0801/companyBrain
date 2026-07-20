from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.file_service import save_upload_file

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=DocumentResponse)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename, filepath = save_upload_file(file)

    document = Document(
        filename=filename,
        original_filename=file.filename,
        file_type=file.content_type,
        file_size=0,
        file_path=filepath,
        uploaded_by=None,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document