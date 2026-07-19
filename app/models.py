from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    tracking_id = Column(String, unique=True, index=True)

    recipient_email = Column(String, nullable=False)

    subject = Column(String)

    body = Column(String)

    status = Column(String, default="draft")

    opened = Column(Boolean, default=False)

    opened_at = Column(DateTime, nullable=True)

    clicked = Column(Boolean, default=False)

    clicked_at = Column(DateTime, nullable=True)

    sent_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)