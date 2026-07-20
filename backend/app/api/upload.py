from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.file_service import save_upload_file

from app.services.text_extractor import extract_text

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=DocumentResponse)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename, filepath = save_upload_file(file)

    try:
        text = extract_text(filepath)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract text from the uploaded document."
        )

    document = Document(
        filename=filename,
        original_filename=file.filename,
        file_type=file.content_type,
        file_size=file.size if file.size else 0,
        file_path=filepath,
        text=text,
        uploaded_by=None,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document