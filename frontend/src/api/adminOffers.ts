import { apiClient } from "@/api/client";

export const adminOffersApi = {
  list: async (page = 1, pageSize = 50) => {
    const { data } = await apiClient.get(`/admin/offers`, { params: { page, page_size: pageSize } });
    return data;
  },

  upload: async (formData: FormData) => {
    const { data } = await apiClient.post(`/admin/offers/upload`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },

  send: async (offerId: string) => {
    const { data } = await apiClient.post(`/admin/offers/${offerId}/send`);
    return data;
  },

  versions: async (offerId: string) => {
    const { data } = await apiClient.get(`/admin/offers/${offerId}/versions`);
    return data;
  },
};
