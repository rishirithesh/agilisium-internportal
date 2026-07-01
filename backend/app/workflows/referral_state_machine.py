"""
Centralized referral state machine.

Every status transition in the application MUST go through `transition()`.
No service or route is permitted to set `referral.status` directly.
"""
from app.core.exceptions import InvalidStateTransitionError
from app.core.permissions import Role
from app.models.referral import ReferralStatus

# Map of current_status -> set of statuses it may legally move to.
_ALLOWED_TRANSITIONS: dict[ReferralStatus, set[ReferralStatus]] = {
    ReferralStatus.REFERRED: {ReferralStatus.INTERN_REGISTERED, ReferralStatus.REJECTED},
    ReferralStatus.INTERN_REGISTERED: {ReferralStatus.EMPLOYEE_APPROVED, ReferralStatus.REJECTED},
    ReferralStatus.EMPLOYEE_APPROVED: {ReferralStatus.PROFILE_SUBMITTED, ReferralStatus.REJECTED},
    ReferralStatus.PROFILE_SUBMITTED: {ReferralStatus.ADMIN_REVIEW},
    ReferralStatus.ADMIN_REVIEW: {
        ReferralStatus.OFFER_GENERATED,
        ReferralStatus.CHANGES_REQUESTED,
        ReferralStatus.REJECTED,
    },
    ReferralStatus.CHANGES_REQUESTED: {ReferralStatus.PROFILE_SUBMITTED},
    ReferralStatus.OFFER_GENERATED: {ReferralStatus.OFFER_UPLOADED},
    ReferralStatus.OFFER_UPLOADED: {ReferralStatus.OFFER_SENT},
    ReferralStatus.OFFER_SENT: {ReferralStatus.OFFER_ACCEPTED, ReferralStatus.REJECTED},
    ReferralStatus.OFFER_ACCEPTED: {ReferralStatus.COMPLETED},
    ReferralStatus.COMPLETED: set(),
    ReferralStatus.REJECTED: set(),
}

# Which role is allowed to *trigger* each transition (defense in depth on top of `can()`).
_TRANSITION_ACTOR: dict[tuple[ReferralStatus, ReferralStatus], set[Role]] = {
    (ReferralStatus.REFERRED, ReferralStatus.INTERN_REGISTERED): {Role.INTERN, Role.ADMIN},
    (ReferralStatus.INTERN_REGISTERED, ReferralStatus.EMPLOYEE_APPROVED): {Role.EMPLOYEE},
    (ReferralStatus.EMPLOYEE_APPROVED, ReferralStatus.PROFILE_SUBMITTED): {Role.INTERN},
    (ReferralStatus.PROFILE_SUBMITTED, ReferralStatus.ADMIN_REVIEW): {Role.INTERN, Role.ADMIN},
    (ReferralStatus.ADMIN_REVIEW, ReferralStatus.OFFER_GENERATED): {Role.ADMIN, Role.MAIN_ADMIN},
    (ReferralStatus.ADMIN_REVIEW, ReferralStatus.CHANGES_REQUESTED): {Role.ADMIN, Role.MAIN_ADMIN},
    (ReferralStatus.CHANGES_REQUESTED, ReferralStatus.PROFILE_SUBMITTED): {Role.INTERN},
    (ReferralStatus.OFFER_GENERATED, ReferralStatus.OFFER_UPLOADED): {Role.ADMIN, Role.MAIN_ADMIN},
    (ReferralStatus.OFFER_UPLOADED, ReferralStatus.OFFER_SENT): {Role.ADMIN, Role.MAIN_ADMIN},
    (ReferralStatus.OFFER_SENT, ReferralStatus.OFFER_ACCEPTED): {Role.INTERN},
    (ReferralStatus.OFFER_ACCEPTED, ReferralStatus.COMPLETED): {Role.ADMIN, Role.MAIN_ADMIN},
}


def assert_valid_transition(
    current: ReferralStatus, target: ReferralStatus, actor_role: Role
) -> None:
    allowed_targets = _ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed_targets:
        raise InvalidStateTransitionError(
            f"Cannot transition referral from {current} to {target}"
        )

    # REJECTED is reachable from several states by Admin/Main Admin regardless of the
    # specific source state, so only enforce the actor map for non-rejection transitions.
    if target != ReferralStatus.REJECTED:
        allowed_actors = _TRANSITION_ACTOR.get((current, target))
        if allowed_actors and actor_role not in allowed_actors:
            raise InvalidStateTransitionError(
                f"Role {actor_role} is not permitted to move referral from {current} to {target}"
            )
    elif actor_role not in {Role.ADMIN, Role.MAIN_ADMIN, Role.EMPLOYEE}:
        raise InvalidStateTransitionError(f"Role {actor_role} cannot reject a referral")


def next_possible_statuses(current: ReferralStatus) -> set[ReferralStatus]:
    return _ALLOWED_TRANSITIONS.get(current, set())
