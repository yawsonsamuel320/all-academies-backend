import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import BackgroundTasks
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

async def send_invite_email(email: str, school_name: str, invite_link: str, first_name: str, role: str, class_level=None, subjects_taught=None):
    """Sends an email invitation to a user (teacher or student)."""
    message = MIMEMultipart()
    message["From"] = SMTP_USERNAME
    message["To"] = email
    message["Subject"] = f"{role.capitalize()} Invitation - Join {school_name}"

    if role == "teacher" and subjects_taught:
        subjects_list = "".join(
            [f"<li>{subject.subject_name} for {subject.class_level}</li>" for subject in subjects_taught]
        )
        email_body = f"""
        <html>
        <body>
            <p>Hello {first_name},</p>
            <p>You have been invited to join {school_name} on All Academies as a teacher.</p>
            <p>You will be teaching:</p>
            <ul>
                {subjects_list}
            </ul>
            <p>Click <a href="{invite_link}">here</a> to accept the invitation.</p>
            <p>This link will expire in 48 hours.</p>
        </body>
        </html>
        """
    else:
        email_body = f"""
        <html>
        <body>
            <p>Hello {first_name},</p>
            <p>You have been invited to join {school_name} on All Academies as a student in {class_level}.</p>
            <p>Click <a href="{invite_link}">here</a> to complete your registration.</p>
            <p>This link will expire in 48 hours.</p>
        </body>
        </html>
        """

    message.attach(MIMEText(email_body, "html"))

    def send_email():
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SMTP_USERNAME, email, message.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")

    send_email()  

