from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.offer import Offer, OfferStatus
from app.models.offer_version import OfferVersion
from datetime import datetime
from app.repositories.offer_repository import OfferRepository
from app.repositories.referral_repository import ReferralRepository
from app.models.referral import Referral, ReferralStatus
from app.repositories.referral_repository import ReferralRepository
from app.services.storage_service import StorageService
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService
from app.services.email_service import EmailService


class OfferService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.referrals = ReferralRepository(db)
        self.storage = StorageService()
        self.audit = AuditService(db)
        self.notifications = NotificationService(db)
        self.email = EmailService(db=self.db)

    async def upload_offer_letter(self, *, referral_id, file_bytes: bytes, original_name: str, position_title: str | None = None, stipend_amount: float | None = None, start_date = None, end_date = None, uploaded_by=None) -> Offer:
        referral = await self.referrals.get_by_id(referral_id)
        if not referral:
            from app.core.exceptions import NotFoundError

            raise NotFoundError("Referral not found")

        key = self.storage.save_pdf(file_bytes, dest_folder=str(referral_id), original_name=original_name)

        offer = Offer(
            referral_id=referral.id,
            position_title=position_title or referral.position_applied,
            stipend_amount=stipend_amount,
            internship_start_date=start_date,
            internship_end_date=end_date,
            offer_letter_storage_key=key,
            status=OfferStatus.UPLOADED,
            created_by=uploaded_by,
            updated_by=uploaded_by,
        )
        self.db.add(offer)
        await self.db.flush()

        # create version record
        version = OfferVersion(offer_id=offer.id, storage_key=key, uploaded_at=datetime.utcnow())
        self.db.add(version)
        await self.db.flush()

        await self.audit.log(actor_id=uploaded_by, action="OFFER_UPLOADED", resource_type="Offer", resource_id=str(offer.id))

        # Notify admin/referrer
        from app.models.audit_log import NotificationType
        try:
            await self.notifications.create(
                user_id=referral.referred_by_id,
                type_=NotificationType.GENERIC,
                title=f"Offer uploaded for {referral.candidate_full_name}",
                body="An offer letter has been uploaded.",
                link_url=f"/offers/{offer.id}",
            )
        except Exception:
            pass

        return offer

    async def send_offer(self, *, offer_id, sent_by=None, send_email: bool = True) -> Offer:
        repo = OfferRepository(self.db)
        offer = await repo.get_by_id(offer_id)
        if not offer:
            from app.core.exceptions import NotFoundError

            raise NotFoundError("Offer not found")

        offer.status = OfferStatus.SENT
        offer.sent_at = datetime.utcnow()
        await self.db.flush()

        # update referral status
        referral_repo = ReferralRepository(self.db)
        referral = await referral_repo.get_by_id(offer.referral_id)
        if referral:
            referral.status = ReferralStatus.OFFER_SENT
            referral.offer_sent_at = datetime.utcnow()

        await self.audit.log(actor_id=sent_by, action="OFFER_SENT", resource_type="Offer", resource_id=str(offer.id))

        if send_email:
            try:
                await self.email.send_offer_email(
                    to_email=referral.candidate_email,
                    full_name=referral.candidate_full_name,
                    position_title=offer.position_title,
                )
            except Exception:
                pass

        return offer

    async def accept_offer(self, *, offer_id, user_id) -> Offer:
        repo = OfferRepository(self.db)
        offer = await repo.get_by_id(offer_id)
        if not offer:
            from app.core.exceptions import NotFoundError

            raise NotFoundError("Offer not found")

        # ensure the user matches the referral intern or email
        referral_repo = ReferralRepository(self.db)
        referral = await referral_repo.get_by_id(offer.referral_id)
        if not referral:
            from app.core.exceptions import NotFoundError

            raise NotFoundError("Referral not found")

        # check user is the intern for this referral
        if referral.intern_user_id and str(referral.intern_user_id) != str(user_id):
            from app.core.exceptions import ForbiddenError

            raise ForbiddenError("User not allowed to accept this offer")

        offer.status = OfferStatus.ACCEPTED
        offer.accepted_at = datetime.utcnow()
        await self.db.flush()

        # create Internship record
        from app.models.internship import Internship
        internship = Internship(
            user_id=user_id,
            referral_id=referral.id,
            offer_id=offer.id,
            start_date=offer.internship_start_date,
            end_date=offer.internship_end_date,
            stipend_amount=str(offer.stipend_amount) if offer.stipend_amount is not None else None,
        )
        from app.repositories.internship_repository import InternshipRepository

        internship = await InternshipRepository(self.db).create(internship)

        # update referral status
        referral.status = ReferralStatus.OFFER_ACCEPTED
        await self.audit.log(actor_id=user_id, action="OFFER_ACCEPTED", resource_type="Offer", resource_id=str(offer.id))

        return offer
