from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yagmail
import os
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

if not all([EMAIL_USER, EMAIL_PASS, TO_EMAIL]):
    raise ValueError("Missing EMAIL_USER, EMAIL_PASS, or TO_EMAIL in environment")

yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: str | None = None
    subject: str
    message: str

def send_email(data: ContactForm):
    """Send email in a separate thread"""
    try:
        body = f"""
        📩 New contact form submission

        👤 Name: {data.name}
        📧 Email: {data.email if data.email else "Not Provided"}
        📝 Subject: {data.subject}

        💬 Message:
        {data.message}
        """
        yag.send(
            to=TO_EMAIL,
            subject=f"Contact Form: {data.subject}",
            contents=body
        )
    except Exception as e:
        print(f"Error sending email in background thread: {e}")

@app.post("/contact")
async def send_contact_form(data: ContactForm):
    try:
        # Run email sending in a separate thread
        threading.Thread(target=send_email, args=(data,), daemon=True).start()
        return {"status": "success", "message": "Email is being sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling email: {str(e)}")
