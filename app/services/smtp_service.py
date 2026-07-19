import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
)


def send_email(receiver_email: str, subject: str, body: str, tracking_id: str):

    try:

        # Create Email Object
        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        message["Subject"] = subject

        # Email Body
        from app.services.template_service import render_email
        tracking_url = (
            f"https://email-tracking-service-1.onrender.com/track/{tracking_id}"
        )

        html_body = render_email(tracking_url)

        message.attach(
            MIMEText(html_body, "html")
    )

        # Connect SMTP Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        # Secure Connection
        server.starttls()

        # Login
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send
        server.send_message(message)

        # Disconnect
        server.quit()

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:

        print("SMTP ERROR :", e)

        return {
            "success": False,
            "message": str(e)
        }