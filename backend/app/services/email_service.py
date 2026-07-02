import asyncio
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models import Setting

logger = logging.getLogger("airp.email")

def get_smtp_setting(db: Session, key: str, default_val: str) -> str:
    db_setting = db.query(Setting).filter(Setting.key == key).first()
    return db_setting.value if db_setting else default_val

async def send_email_async(
    db: Session,
    recipient_email: str,
    subject: str,
    html_content: str
):
    host = get_smtp_setting(db, "smtp_host", settings.SMTP_HOST)
    port = int(get_smtp_setting(db, "smtp_port", str(settings.SMTP_PORT)))
    user = get_smtp_setting(db, "smtp_user", settings.SMTP_USER)
    password = get_smtp_setting(db, "smtp_pass", settings.SMTP_PASS)
    from_email = get_smtp_setting(db, "smtp_from", settings.SMTP_FROM)

    message = MIMEMultipart("alternative")
    message["From"] = from_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    try:
        # Check if we should use TLS or not
        # Typically 587 is STARTTLS
        if port == 587:
            await aiosmtplib.send(
                message,
                hostname=host,
                port=port,
                username=user,
                password=password,
                starttls=True
            )
        else:
            await aiosmtplib.send(
                message,
                hostname=host,
                port=port,
                username=user,
                password=password,
                use_tls=True if port == 465 else False
            )
        logger.info(f"Email sent successfully to {recipient_email}")
        print(f"SMTP Success: Email sent to {recipient_email} - Subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        # Print for local diagnostics
        print(f"SMTP Error: Failed to send email to {recipient_email}. Reason: {e}")

def send_email_background(
    background_tasks,
    db: Session,
    recipient_email: str,
    subject: str,
    html_content: str
):
    background_tasks.add_task(
        send_email_async,
        db,
        recipient_email,
        subject,
        html_content
    )
