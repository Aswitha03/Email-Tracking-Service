from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.tracking_service import track_email_open
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/track/{tracking_id}")
def track(tracking_id: str, db: Session = Depends(get_db)):

    email = track_email_open(db, tracking_id)

    if email is None:
        return {
            "message": "Tracking ID not found"
        }

    return FileResponse(
        "app/static/pixel.png",
        media_type="image/png"
    )