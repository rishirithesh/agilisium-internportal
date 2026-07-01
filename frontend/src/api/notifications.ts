import { apiClient } from "@/api/client";
import type { Notification, PaginatedNotifications } from "@/types/domain";

export const notificationsApi = {
  list: async (page = 1, pageSize = 20): Promise<PaginatedNotifications> => {
    const { data } = await apiClient.get<PaginatedNotifications>("/notifications", {
      params: { page, page_size: pageSize },
    });
    return data;
  },
  markRead: async (id: string): Promise<Notification> => {
    const { data } = await apiClient.post<Notification>(`/notifications/${id}/read`);
    return data;
  },
  markAllRead: async (): Promise<{ updated: number }> => {
    const { data } = await apiClient.post<{ updated: number }>("/notifications/mark-all-read");
    return data;
  },
};
