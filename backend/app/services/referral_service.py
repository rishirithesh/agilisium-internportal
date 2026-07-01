import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from app.core.permissions import Action, Role, can
from app.models.audit_log import NotificationType
from app.models.referral import Referral, ReferralStatus, ReferralTimelineEvent
from app.repositories.referral_repository import ReferralRepository
from app.repositories.user_repository import UserRepository
from app.schemas.referral import ReferralCreateRequest
from app.services.audit_service import AuditService
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from app.workflows.referral_state_machine import assert_valid_transition
from app.repositories.pending_registration_repository import PendingRegistrationRepository
from app.models.pending_registration import PendingInternRegistration
from app.core.security import hash_password, verify_password
import secrets
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import json


class ReferralService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.referrals = ReferralRepository(db)
        self.users = UserRepository(db)
        self.audit = AuditService(db)
        self.notifications = NotificationService(db)
        self.email = EmailService(db=self.db)
        self.pending = PendingRegistrationRepository(db)
        # repositories for creating intern profile and users are available

    async def create_referral(
        self, *, employee_id: uuid.UUID, role: Role, payload: ReferralCreateRequest
    ) -> Referral:
        if not can(role, Action.CREATE_REFERRAL):
            raise AuthorizationError("You are not permitted to create referrals")
        candidate_email = str(payload.candidate_email).strip().lower()

        # Prevent referring Agilisium internal emails for interns
        if candidate_email.endswith("@agilisium.com"):
            from app.core.exceptions import ValidationError

            raise ValidationError("Candidate email must not be an @agilisium.com address")

        # Prevent creating referrals when a user already exists with that email
        existing_user = await self.users.get_by_email(candidate_email)
        if existing_user:
            from app.core.exceptions import ConflictError

            raise ConflictError("A user with this email already exists")

        # Prevent duplicate active referrals
        active = await self.referrals.get_active_by_email(candidate_email)
        if active:
            from app.core.exceptions import ConflictError

            raise ConflictError("An active referral for this email already exists")

        referral = Referral(
            referred_by_id=employee_id,
            candidate_full_name=payload.candidate_full_name,
            candidate_email=candidate_email,
            candidate_phone=payload.candidate_phone,
            position_applied=payload.position_applied,
            relationship_to_candidate=payload.relationship_to_candidate,
            referral_notes=payload.referral_notes,
            status=ReferralStatus.REFERRED,
            created_by=employee_id,
            updated_by=employee_id,
        )
        referral = await self.referrals.create(referral)

        await self.referrals.add_timeline_event(
            ReferralTimelineEvent(
                referral_id=referral.id,
                from_status=None,
                to_status=ReferralStatus.REFERRED,
                actor_id=employee_id,
                note="Referral created",
            )
        )
        await self.audit.log(
            actor_id=employee_id,
            action="REFERRAL_CREATED",
            resource_type="Referral",
            resource_id=str(referral.id),
        )

        # Generate secure invitation token (store hashed) and expiry
        token = secrets.token_urlsafe(32)
        referral.invitation_token_hash = hash_password(token)
        referral.invitation_expires_at = (
            datetime.now(timezone.utc) + timedelta(days=7)
        )
        await self.db.flush()

        # Send invitation email asynchronously (best-effort)
        try:
            invite_link = f"{settings.FRONTEND_BASE_URL}/invite?referral_id={referral.id}&token={token}"
            await self.email.send_referral_invitation(
                to_email=referral.candidate_email,
                full_name=(await self.users.get_by_id(employee_id)).full_name,
                candidate_name=referral.candidate_full_name,
                invite_link=invite_link,
                expires_at=referral.invitation_expires_at.isoformat(),
            )
        except Exception:
            pass
        return referral

    async def register_intern(self, *, referral_id: uuid.UUID, token: str, email: str, password: str, entered_details: dict) -> PendingInternRegistration:
        referral = await self.referrals.get_by_id(referral_id)
        if not referral:
            raise NotFoundError("Referral not found")

        if not referral.invitation_token_hash or not referral.invitation_expires_at:
            raise AuthorizationError("Invitation not found or already used")

        if datetime.now(timezone.utc) > referral.invitation_expires_at:
            raise AuthorizationError("Invitation has expired")

        if not verify_password(token, referral.invitation_token_hash):
            raise AuthorizationError("Invalid invitation token")

        # Ensure email matches referral candidate email
        if email.strip().lower() != referral.candidate_email:
            raise ValidationError("Registration email must match invited email")

        # Create pending registration record
        pending = PendingInternRegistration(
            referral_id=referral.id,
            email=email.strip().lower(),
            password_hash=hash_password(password),
            entered_details=json.dumps(entered_details) if entered_details else None,
            expires_at=referral.invitation_expires_at,
            created_by=referral.referred_by_id,
            updated_by=referral.referred_by_id,
        )
        pending = await self.pending.create(pending)

        # Invalidate invitation token (single use)
        referral.invitation_token_hash = None
        await self.db.flush()

        # Update referral status to INTERN_REGISTERED and add timeline
        previous = referral.status
        referral.status = ReferralStatus.INTERN_REGISTERED
        referral.updated_by = referral.referred_by_id
        await self.db.flush()

        await self.referrals.add_timeline_event(
            ReferralTimelineEvent(
                referral_id=referral.id,
                from_status=previous,
                to_status=ReferralStatus.INTERN_REGISTERED,
                actor_id=None,
                note="Intern completed registration (pending employee approval)",
            )
        )

        await self.audit.log(
            actor_id=referral.referred_by_id,
            action="INTERN_REGISTERED",
            resource_type="Referral",
            resource_id=str(referral.id),
        )

        # Notify referring employee
        await self.notifications.create(
            user_id=referral.referred_by_id,
            type_=NotificationType.REFERRAL_STATUS_CHANGED,
            title=f"{referral.candidate_full_name} has completed registration",
            body=f"{referral.candidate_full_name} registered and is awaiting your approval.",
            link_url=f"/referrals/{referral.id}",
        )

        # Generate employee action token (one-tap approve/reject) and send approval-request email
        try:
            action_token = secrets.token_urlsafe(24)
            referral.employee_action_token_hash = hash_password(action_token)
            referral.employee_action_expires_at = datetime.now(timezone.utc) + timedelta(days=7)
            await self.db.flush()

            approve_link = f"{settings.FRONTEND_BASE_URL}/admin/referrals/{referral.id}/approve?token={action_token}"
            reject_link = f"{settings.FRONTEND_BASE_URL}/admin/referrals/{referral.id}/reject?token={action_token}"
            await self.email.send_employee_approval_request(
                to_email=(await self.users.get_by_id(referral.referred_by_id)).email,
                full_name=(await self.users.get_by_id(referral.referred_by_id)).full_name,
                candidate_name=referral.candidate_full_name,
                approve_link=approve_link,
                reject_link=reject_link,
                expires_at=referral.employee_action_expires_at.isoformat(),
            )
        except Exception:
            pass

        return pending

    async def approve_pending_registration(self, *, referral_id: uuid.UUID, actor_id: uuid.UUID, role: Role) -> Referral:
        # Only the referring employee may approve their pending referral, or admins may approve
        referral = await self.referrals.get_by_id(referral_id)
        if not referral:
            raise NotFoundError("Referral not found")

        # Authorization: employee who referred or admins
        is_owner = referral.referred_by_id == actor_id
        if not (is_owner or can(role, Action.VIEW_ALL_REFERRALS)):
            raise AuthorizationError("You are not permitted to approve this referral")

        # Load pending registration
        pending = await self.pending.get_by_email(referral.candidate_email)
        if not pending:
            raise NotFoundError("No pending registration found for this referral")

        # Create user record
        from app.models.user import User
        from app.models.intern_profile import InternProfile

        user = User(
            email=pending.email,
            full_name=referral.candidate_full_name,
            hashed_password=pending.password_hash,
            role=Role.INTERN,
            is_email_verified=True,
            is_active=True,
            created_by=actor_id,
            updated_by=actor_id,
        )
        user = await self.users.create(user)

        # Create intern profile using entered details where available
        details = {}
        try:
            details = json.loads(pending.entered_details) if pending.entered_details else {}
        except Exception:
            details = {}

        intern_profile = InternProfile(
            referral_id=referral.id,
            user_id=user.id,
            college_name=details.get("college", ""),
            degree=details.get("degree", ""),
            graduation_year=int(details.get("graduation_year", 0)) if details.get("graduation_year") else 0,
            created_by=actor_id,
            updated_by=actor_id,
        )
        self.db.add(intern_profile)
        await self.db.flush()

        # Link intern to referral and update status
        previous = referral.status
        referral.intern_user_id = user.id
        referral.status = ReferralStatus.EMPLOYEE_APPROVED
        referral.employee_approved_at = datetime.now(timezone.utc)
        referral.updated_by = actor_id
        await self.db.flush()

        await self.referrals.add_timeline_event(
            ReferralTimelineEvent(
                referral_id=referral.id,
                from_status=previous,
                to_status=ReferralStatus.EMPLOYEE_APPROVED,
                actor_id=actor_id,
                note="Employee approved referral and intern account created",
            )
        )

        # Delete pending registration
        await self.pending.delete(pending)

        # Audit + notifications + welcome email
        await self.audit.log(
            actor_id=actor_id,
            action="EMPLOYEE_APPROVED",
            resource_type="Referral",
            resource_id=str(referral.id),
        )

        await self.notifications.create(
            user_id=actor_id,
            type_=NotificationType.REFERRAL_STATUS_CHANGED,
            title=f"You approved {referral.candidate_full_name}",
            body=f"Intern account created for {referral.candidate_full_name}.",
            link_url=f"/referrals/{referral.id}",
        )

        try:
            await self.email.send_welcome_email(
                to_email=user.email,
                full_name=user.full_name,
                portal_link=settings.FRONTEND_BASE_URL,
            )
        except Exception:
            pass

        return referral

    async def reject_pending_registration(self, *, referral_id: uuid.UUID, actor_id: uuid.UUID, role: Role, reason: str) -> Referral:
        if not reason or len(reason.strip()) < 20:
            from app.core.exceptions import ValidationError

            raise ValidationError("Rejection reason must be at least 20 characters")

        referral = await self.referrals.get_by_id(referral_id)
        if not referral:
            raise NotFoundError("Referral not found")

        is_owner = referral.referred_by_id == actor_id
        if not (is_owner or can(role, Action.VIEW_ALL_REFERRALS)):
            raise AuthorizationError("You are not permitted to reject this referral")

        pending = await self.pending.get_by_email(referral.candidate_email)
        if pending:
            await self.pending.delete(pending)

        previous = referral.status
        referral.status = ReferralStatus.REJECTED
        referral.updated_by = actor_id
        await self.db.flush()

        await self.referrals.add_timeline_event(
            ReferralTimelineEvent(
                referral_id=referral.id,
                from_status=previous,
                to_status=ReferralStatus.REJECTED,
                actor_id=actor_id,
                note=reason,
            )
        )

        await self.audit.log(
            actor_id=actor_id,
            action="EMPLOYEE_REJECTED",
            resource_type="Referral",
            resource_id=str(referral.id),
            metadata={"reason": reason},
        )

        # Notify intern (best-effort) and referring employee
        try:
            await self.email.send_referral_status_email(
                to_email=referral.candidate_email,
                full_name=referral.candidate_full_name,
                candidate_name=referral.candidate_full_name,
                status=ReferralStatus.REJECTED.value,
            )
        except Exception:
            pass

        await self.notifications.create(
            user_id=referral.referred_by_id,
            type_=NotificationType.REFERRAL_STATUS_CHANGED,
            title=f"Referral for {referral.candidate_full_name} rejected",
            body=reason,
            link_url=f"/referrals/{referral.id}",
        )

        return referral

    async def get_referral(self, referral_id: uuid.UUID, *, actor_id: uuid.UUID, role: Role) -> Referral:
        referral = await self.referrals.get_by_id(referral_id, with_timeline=True)
        if not referral:
            raise NotFoundError("Referral not found")

        is_owner = referral.referred_by_id == actor_id or referral.intern_user_id == actor_id
        if not is_owner and not can(role, Action.VIEW_ALL_REFERRALS):
            raise AuthorizationError("You do not have access to this referral")
        return referral

    async def transition_status(
        self,
        *,
        referral_id: uuid.UUID,
        target_status: ReferralStatus,
        actor_id: uuid.UUID,
        role: Role,
        note: str | None = None,
    ) -> Referral:
        referral = await self.referrals.get_by_id(referral_id)
        if not referral:
            raise NotFoundError("Referral not found")

        assert_valid_transition(referral.status, target_status, role)

        previous_status = referral.status
        referral.status = target_status
        referral.updated_by = actor_id
        await self.db.flush()

        await self.referrals.add_timeline_event(
            ReferralTimelineEvent(
                referral_id=referral.id,
                from_status=previous_status,
                to_status=target_status,
                actor_id=actor_id,
                note=note,
            )
        )

        await self.audit.log(
            actor_id=actor_id,
            action="REFERRAL_STATUS_CHANGED",
            resource_type="Referral",
            resource_id=str(referral.id),
            metadata={"from": previous_status.value, "to": target_status.value},
        )

        # Notify the referring employee in-app; email is best-effort and should not
        # block the transition if SMTP is briefly unavailable in local/dev.
        await self.notifications.create(
            user_id=referral.referred_by_id,
            type_=NotificationType.REFERRAL_STATUS_CHANGED,
            title=f"Referral for {referral.candidate_full_name} updated",
            body=f"Status changed from {previous_status} to {target_status}",
            link_url=f"/referrals/{referral.id}",
        )
        try:
            employee = await self.users.get_by_id(referral.referred_by_id)
            if employee:
                await self.email.send_referral_status_email(
                    to_email=employee.email,
                    full_name=employee.full_name,
                    candidate_name=referral.candidate_full_name,
                    status=target_status.value,
                )
        except Exception:
            # Logged, not raised: email delivery failures must never break the
            # core workflow transition.
            pass

        return referral

    async def list_referrals(
        self, *, actor_id: uuid.UUID, role: Role, page: int, page_size: int, status: ReferralStatus | None
    ) -> tuple[list[Referral], int]:
        if can(role, Action.VIEW_ALL_REFERRALS):
            return await self.referrals.list_all(page, page_size, status)
        return await self.referrals.list_for_employee(actor_id, page, page_size)
