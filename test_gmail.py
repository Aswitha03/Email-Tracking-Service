from app.services.gmail_service import send_email

send_email(
    "aswithakota@gmail.com",
    "Testing Gmail API",
    "<h1>Hello from Gmail API 🚀</h1>"
)

print("Done")