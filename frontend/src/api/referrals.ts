import { apiClient } from "@/api/client";
import type { PaginatedReferrals, Referral, ReferralDetail, ReferralStatus } from "@/types/domain";

export interface CreateReferralPayload {
  candidate_full_name: string;
  candidate_email: string;
  candidate_phone?: string;
  position_applied: string;
  relationship_to_candidate?: string;
  referral_notes?: string;
}

export const referralsApi = {
  list: async (page = 1, pageSize = 20, status?: ReferralStatus): Promise<PaginatedReferrals> => {
    const { data } = await apiClient.get<PaginatedReferrals>("/referrals", {
      params: { page, page_size: pageSize, status },
    });
    return data;
  },

  get: async (id: string): Promise<ReferralDetail> => {
    const { data } = await apiClient.get<ReferralDetail>(`/referrals/${id}`);
    return data;
  },

  create: async (payload: CreateReferralPayload): Promise<Referral> => {
    const { data } = await apiClient.post<Referral>("/referrals", payload);
    return data;
  },

  transition: async (id: string, target_status: ReferralStatus, note?: string): Promise<Referral> => {
    const { data } = await apiClient.post<Referral>(`/referrals/${id}/transition`, {
      target_status,
      note,
    });
    return data;
  },
  registerCandidate: async (referralId: string, token: string, email: string, password: string, entered_details: any) => {
    const { data } = await apiClient.post(`/referrals/${referralId}/register`, {
      token,
      email,
      password,
      entered_details,
    });
    return data;
  },
  approveByToken: async (referralId: string, token: string) => {
    const { data } = await apiClient.get(`/referrals/${referralId}/approve_by_token`, { params: { token } });
    return data;
  },
  rejectByToken: async (referralId: string, token: string, reason?: string) => {
    const { data } = await apiClient.get(`/referrals/${referralId}/reject_by_token`, { params: { token, reason } });
    return data;
  },
};
