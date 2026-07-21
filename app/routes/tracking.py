from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.tracking_service import track_email_open
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/track/{tracking_id}")
def track(tracking_id: str, request: Request, db: Session = Depends(get_db)):

    user_agent = request.headers.get("user-agent", "")

    email = track_email_open(db, tracking_id, user_agent=user_agent)

    if email is None:
        return {
            "message": "Tracking ID not found"
        }

    response = FileResponse(
        "app/static/pixel.png",
        media_type="image/png"
    )

    # Ask Gmail/browsers not to cache the pixel. This won't always be
    # honored (Google may still cache server-side) but it helps reduce
    # cases where a real later open is silently served from cache and
    # never reaches this endpoint at all.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response