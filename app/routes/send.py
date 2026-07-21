import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Email
from app.schemas import EmailCreate
from app.services.gmail_service import send_email
from app.services.template_service import render_email

router = APIRouter()


@router.post("/send-email")
def create_email(email: EmailCreate, db: Session = Depends(get_db)):

    tracking_id = str(uuid.uuid4())

    tracking_url = f"https://email-tracking-service-1.onrender.com/track/{tracking_id}"

    html_body = render_email(email.body, tracking_url)

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

    try:

        send_email(
            receiver_email=email.recipient_email,
            subject=email.subject,
            html_body=html_body
        )

        new_email.status = "sent"

    except Exception as e:

        print(e)

        new_email.status = "failed"

    db.commit()
    db.refresh(new_email)

    return {
        "message": "Email processed successfully",
        "status": new_email.status,
        "tracking_id": tracking_id
    }
@router.get("/emails")
def get_all_emails(db: Session = Depends(get_db)):

    emails = db.query(Email).all()

    return emails