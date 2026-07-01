import asyncio
import logging
import traceback
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.audit_log import EmailLog, EmailStatus

logger = logging.getLogger("airp.email")

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "email"
_jinja_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)


class EmailService:
    """SMTP email sender with simple retry and optional DB logging via EmailLog."""

    def __init__(self, db: Optional[AsyncSession] = None, max_retries: int = 3, backoff_seconds: float = 1.0):
        self.db = db
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    async def _send_raw(self, *, to_email: str, subject: str, html_body: str) -> None:
        message = EmailMessage()
        message["From"] = f"{settings.smtp_from_display_name} <{settings.smtp_from_address}>"
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content("This email requires an HTML-capable client.")
        message.add_alternative(html_body, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_APP_PASSWORD,
        )

    def _render(self, template_name: str, **context) -> str:
        template = _jinja_env.get_template(template_name)
        return template.render(**context)

    async def _send_with_retries(self, *, to_email: str, subject: str, html_body: str) -> None:
        last_err = None
        for attempt in range(1, self.max_retries + 1):
            try:
                await self._send_raw(to_email=to_email, subject=subject, html_body=html_body)
                # log success if DB provided
                if self.db:
                    log = EmailLog(to_email=to_email, template_name=subject, subject=subject, status=EmailStatus.SENT, attempts=attempt)
                    self.db.add(log)
                    await self.db.flush()
                return
            except Exception as exc:
                last_err = exc
                logger.exception("Email send failed (attempt %s): %s", attempt, exc)
                # update/insert EmailLog as failed
                if self.db:
                    try:
                        log = EmailLog(to_email=to_email, template_name=subject, subject=subject, status=EmailStatus.FAILED, attempts=attempt, last_error=str(exc))
                        self.db.add(log)
                        await self.db.flush()
                    except Exception:
                        logger.exception("Failed to write EmailLog")

                if attempt < self.max_retries:
                    await asyncio.sleep(self.backoff_seconds * (2 ** (attempt - 1)))
        # If we reach here, all attempts failed
        raise last_err

    async def send_otp_email(self, *, to_email: str, full_name: str, otp_code: str) -> None:
        html = self._render(
            "otp.html",
            full_name=full_name,
            otp_code=otp_code,
            expire_minutes=settings.OTP_EXPIRE_MINUTES,
        )
        await self._send_with_retries(to_email=to_email, subject="Your AIRP login code", html_body=html)

    async def send_referral_status_email(
        self, *, to_email: str, full_name: str, candidate_name: str, status: str
    ) -> None:
        html = self._render(
            "referral_status_changed.html",
            full_name=full_name,
            candidate_name=candidate_name,
            status=status,
        )
        await self._send_with_retries(
            to_email=to_email,
            subject=f"Referral update: {candidate_name} — {status}",
            html_body=html,
        )

    async def send_referral_invitation(self, *, to_email: str, full_name: str, candidate_name: str, invite_link: str, expires_at: str) -> None:
        try:
            html = self._render(
                "referral_invite.html",
                full_name=full_name,
                candidate_name=candidate_name,
                invite_link=invite_link,
                expires_at=expires_at,
            )
        except Exception:
            html = f"<p>Hi {candidate_name},</p><p>You have been referred. Click <a href='{invite_link}'>here</a> to register. Link expires {expires_at}.</p>"

        await self._send_with_retries(
            to_email=to_email,
            subject=f"You're invited to join Agilisium Intern Portal",
            html_body=html,
        )

    async def send_employee_approval_request(self, *, to_email: str, full_name: str, candidate_name: str, approve_link: str, reject_link: str, expires_at: str) -> None:
        try:
            html = self._render(
                "employee_approval_request.html",
                full_name=full_name,
                candidate_name=candidate_name,
                approve_link=approve_link,
                reject_link=reject_link,
                expires_at=expires_at,
            )
        except Exception:
            html = f"<p>Hi {full_name},</p><p>{candidate_name} has registered. Approve: <a href='{approve_link}'>Approve</a> or <a href='{reject_link}'>Reject</a>. Expires {expires_at}.</p>"

        await self._send_with_retries(
            to_email=to_email,
            subject=f"Approval needed: {candidate_name} registration",
            html_body=html,
        )

    async def send_welcome_email(self, *, to_email: str, full_name: str, portal_link: str) -> None:
        try:
            html = self._render("welcome.html", full_name=full_name, portal_link=portal_link)
        except Exception:
            html = f"<p>Welcome {full_name}!</p><p>Access the portal: <a href=\"{portal_link}\">{portal_link}</a></p>"
        await self._send_with_retries(to_email=to_email, subject="Welcome to Agilisium Intern Portal", html_body=html)

    async def send_offer_email(self, *, to_email: str, full_name: str, position_title: str) -> None:
        html = self._render("offer_sent.html", full_name=full_name, position_title=position_title)
        await self._send_with_retries(to_email=to_email, subject="Your AIRP internship offer", html_body=html)
