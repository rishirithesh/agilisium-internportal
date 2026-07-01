"""
Centralized authorization policy.

Every route, service, and component-level check must go through `can()`.
Never duplicate role checks inline elsewhere in the codebase.
"""
from enum import StrEnum


class Role(StrEnum):
    EMPLOYEE = "EMPLOYEE"
    INTERN = "INTERN"
    ADMIN = "ADMIN"
    MAIN_ADMIN = "MAIN_ADMIN"


class Action(StrEnum):
    CREATE_REFERRAL = "create_referral"
    VIEW_OWN_REFERRALS = "view_own_referrals"
    VIEW_ALL_REFERRALS = "view_all_referrals"
    APPROVE_REFERRAL_AS_EMPLOYEE = "approve_referral_as_employee"
    SUBMIT_INTERN_PROFILE = "submit_intern_profile"
    REVIEW_REFERRAL_AS_ADMIN = "review_referral_as_admin"
    GENERATE_OFFER = "generate_offer"
    UPLOAD_OFFER = "upload_offer"
    SEND_OFFER = "send_offer"
    ACCEPT_OFFER = "accept_offer"
    MANAGE_USERS = "manage_users"
    MANAGE_ADMINS = "manage_admins"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    VIEW_ANALYTICS = "view_analytics"
    UPLOAD_RESUME = "upload_resume"


# Role -> allowed actions. This is the single permission map for the entire app.
_POLICY: dict[Role, set[Action]] = {
    Role.EMPLOYEE: {
        Action.CREATE_REFERRAL,
        Action.VIEW_OWN_REFERRALS,
        Action.APPROVE_REFERRAL_AS_EMPLOYEE,
    },
    Role.INTERN: {
        Action.SUBMIT_INTERN_PROFILE,
        Action.UPLOAD_RESUME,
        Action.ACCEPT_OFFER,
    },
    Role.ADMIN: {
        Action.VIEW_ALL_REFERRALS,
        Action.REVIEW_REFERRAL_AS_ADMIN,
        Action.GENERATE_OFFER,
        Action.UPLOAD_OFFER,
        Action.SEND_OFFER,
        Action.VIEW_ANALYTICS,
        Action.VIEW_AUDIT_LOGS,
    },
    Role.MAIN_ADMIN: set(),  # populated below: MAIN_ADMIN inherits everything + user mgmt
}

# MAIN_ADMIN inherits every action plus platform-level management actions.
_POLICY[Role.MAIN_ADMIN] = (
    _POLICY[Role.EMPLOYEE]
    | _POLICY[Role.ADMIN]
    | {Action.MANAGE_USERS, Action.MANAGE_ADMINS}
)


def can(role: Role | str, action: Action | str) -> bool:
    role = Role(role)
    action = Action(action)
    return action in _POLICY.get(role, set())


class PermissionDenied(Exception):
    def __init__(self, action: str):
        self.action = action
        super().__init__(f"Permission denied for action: {action}")


def require(role: Role | str, action: Action | str) -> None:
    if not can(role, action):
        raise PermissionDenied(str(action))
