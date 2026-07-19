from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Email


def track_email_open(db: Session, tracking_id: str):
    """
    Marks an email as opened using its tracking ID.
    Returns the email object if found, otherwise None.
    """

    email = (
        db.query(Email)
        .filter(Email.tracking_id == tracking_id)
        .first()
    )

    if not email:
        return None

    # Update only the first time the email is opened
    if not email.opened:
        email.opened = True
        email.opened_at = datetime.utcnow()

        db.commit()
        db.refresh(email)

    return email