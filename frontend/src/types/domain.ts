export type Role = "EMPLOYEE" | "INTERN" | "ADMIN" | "MAIN_ADMIN";

export type ReferralStatus =
  | "REFERRED"
  | "INTERN_REGISTERED"
  | "EMPLOYEE_APPROVED"
  | "PROFILE_SUBMITTED"
  | "ADMIN_REVIEW"
  | "CHANGES_REQUESTED"
  | "OFFER_GENERATED"
  | "OFFER_UPLOADED"
  | "OFFER_SENT"
  | "OFFER_ACCEPTED"
  | "COMPLETED"
  | "REJECTED";

export interface CurrentUser {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  is_email_verified: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Referral {
  id: string;
  referred_by_id: string;
  candidate_full_name: string;
  candidate_email: string;
  candidate_phone: string | null;
  position_applied: string;
  relationship_to_candidate: string | null;
  referral_notes: string | null;
  status: ReferralStatus;
  intern_user_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface TimelineEvent {
  id: string;
  from_status: ReferralStatus | null;
  to_status: ReferralStatus;
  actor_id: string | null;
  note: string | null;
  created_at: string;
}

export interface ReferralDetail extends Referral {
  timeline_events: TimelineEvent[];
}

export interface PaginatedReferrals {
  items: Referral[];
  total: number;
  page: number;
  page_size: number;
}

export type NotificationType = "REFERRAL_STATUS_CHANGED" | "OFFER_SENT" | "OFFER_ACCEPTED" | "PROFILE_INCOMPLETE_REMINDER" | "GENERIC";

export interface Notification {
  id: string;
  user_id: string;
  type: NotificationType;
  title: string;
  body: string | null;
  is_read: boolean;
  link_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedNotifications {
  items: Notification[];
  total: number;
  page: number;
  page_size: number;
}
