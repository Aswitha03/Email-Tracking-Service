from pydantic import BaseModel, EmailStr


class EmailCreate(BaseModel):
    recipient_email: EmailStr
    subject: str
    body: str