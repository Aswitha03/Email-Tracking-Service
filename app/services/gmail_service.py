import base64

from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import app.config as config


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_email(receiver_email, subject, html_body):

    creds = Credentials(
        token=None,
        refresh_token=config.GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES,
    )

    creds.refresh(Request())

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(html_body, "html")

    message["to"] = receiver_email
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {
        "raw": raw
    }

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()

    return True