"""Compatibility helper for SMTP-based email automation."""

from app.services.email_service import EmailService


async def send_otp_email_task(*args, **kwargs) -> None:
    await EmailService().send_otp_email(**kwargs)


async def send_referral_status_email_task(*args, **kwargs) -> None:
    await EmailService().send_referral_status_email(**kwargs)


async def send_offer_email_task(*args, **kwargs) -> None:
    await EmailService().send_offer_email(**kwargs)
