from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yagmail
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

if not all([EMAIL_USER, EMAIL_PASS, TO_EMAIL]):
    raise ValueError("Missing EMAIL_USER, EMAIL_PASS, or TO_EMAIL in environment")

# Configure yagmail
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: str | None = None  # now normal string
    subject: str
    message: str

@app.post("/contact")
async def send_contact_form(data: ContactForm):
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

        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
