import { apiClient, tokenStorage } from "@/api/client";
import type { CurrentUser, TokenResponse } from "@/types/domain";

export const authApi = {
  login: async (email: string, password: string): Promise<TokenResponse> => {
    const { data } = await apiClient.post<TokenResponse>("/auth/login", { email, password });
    tokenStorage.set(data.access_token, data.refresh_token);
    return data;
  },

  requestOtp: async (email: string): Promise<void> => {
    await apiClient.post("/auth/otp/request", { email });
  },

  verifyOtp: async (email: string, otp_code: string): Promise<TokenResponse> => {
    const { data } = await apiClient.post<TokenResponse>("/auth/otp/verify", { email, otp_code });
    tokenStorage.set(data.access_token, data.refresh_token);
    return data;
  },

  me: async (): Promise<CurrentUser> => {
    const { data } = await apiClient.get<CurrentUser>("/auth/me");
    return data;
  },

  logout: (): void => {
    tokenStorage.clear();
  },
};
