import { apiClient } from "@/api/client";

export const offersApi = {
  list: async () => {
    const { data } = await apiClient.get("/offers");
    return data;
  },

  get: async (offerId: string) => {
    const { data } = await apiClient.get(`/offers/${offerId}`);
    return data;
  },

  downloadUrl: (offerId: string) => {
    return `${apiClient.defaults.baseURL}/offers/${offerId}/download`;
  },

  accept: async (offerId: string) => {
    const { data } = await apiClient.post(`/offers/${offerId}/accept`);
    return data;
  },
};
