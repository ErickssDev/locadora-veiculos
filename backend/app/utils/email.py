from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings


async def send_email(subject: str, recipient: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = settings.smtp_user
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
        start_tls=True,
    )
