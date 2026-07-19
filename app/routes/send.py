import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Email
from app.schemas import EmailCreate
from app.services.smtp_service import send_email

router = APIRouter()


@router.post("/send-email")
def create_email(email: EmailCreate, db: Session = Depends(get_db)):

    tracking_id = str(uuid.uuid4())

    new_email = Email(
        tracking_id=tracking_id,
        recipient_email=email.recipient_email,
        subject=email.subject,
        body=email.body,
        status="draft"
    )

    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    success = send_email(
    receiver_email=email.recipient_email,
    subject=email.subject,
    body=email.body,
    tracking_id=tracking_id
)
    if success:
        new_email.status = "sent"
    else:
        new_email.status = "failed"

    db.commit()
    db.refresh(new_email)

    return {
    "message": "Email processed",
    "status": new_email.status,
    "tracking_id": tracking_id,
}

    return {
        "message": "Email saved successfully",
        "tracking_id": tracking_id,
        "email_id": new_email.id
    }
from typing import List
@router.get("/emails")
def get_all_emails(db: Session = Depends(get_db)):

    emails = db.query(Email).all()

    return emails