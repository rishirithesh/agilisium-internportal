import { type ReactNode, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Bell, Moon, Sun, LogOut, LayoutDashboard, Users } from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/features/auth/AuthContext";
import { useTheme } from "@/features/theme/ThemeContext";
import { notificationsApi } from "@/api/notifications";
import clsx from "clsx";

export default function AppShell({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();
  const queryClient = useQueryClient();
  const [showNotifications, setShowNotifications] = useState(false);

  const navItems = [
    { label: "Dashboard", to: "/", icon: LayoutDashboard },
    { label: "Referrals", to: "/referrals", icon: Users },
  ];

  const { data: notificationsData } = useQuery({
    queryKey: ["notifications"],
    queryFn: () => notificationsApi.list(1, 10),
  });

  const unreadCount = useMemo(
    () => notificationsData?.items.filter((item) => !item.is_read).length ?? 0,
    [notificationsData]
  );

  const handleMarkAllRead = async () => {
    await notificationsApi.markAllRead();
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };

  const handleReadNotification = async (id: string) => {
    await notificationsApi.markRead(id);
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };

  return (
    <div className="flex min-h-screen bg-background">
      <aside className="hidden w-64 flex-col border-r border-border bg-surface p-4 md:flex">
        <div className="mb-8 flex items-center gap-3 px-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-base font-semibold text-primary">
            AIRP
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground">AIRP</p>
            <p className="text-xs text-muted-foreground">Intern Referral Portal</p>
          </div>
        </div>
        <nav className="flex flex-col gap-1">
          {navItems.map(({ label, to, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={clsx(
                "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium",
                location.pathname === to
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted"
              )}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-3">
          <div>
            <p className="text-sm font-medium text-foreground">{user?.full_name}</p>
            <p className="text-xs text-muted-foreground">{user?.role.replace("_", " ")}</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="relative">
              <button
                onClick={() => setShowNotifications((value) => !value)}
                className="rounded-lg p-2 text-muted-foreground hover:bg-muted"
                aria-label="Notifications"
              >
                <Bell size={16} />
                {unreadCount > 0 && (
                  <span className="absolute -right-1 -top-1 rounded-full bg-danger px-1.5 py-0.5 text-[10px] font-semibold text-white">
                    {unreadCount}
                  </span>
                )}
              </button>
              {showNotifications && (
                <div className="absolute right-0 z-10 mt-2 w-80 rounded-xl border border-border bg-surface p-3 shadow-lg">
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-semibold text-foreground">Notifications</p>
                    <button className="text-xs text-primary" onClick={handleMarkAllRead}>
                      Mark all read
                    </button>
                  </div>
                  <div className="flex max-h-72 flex-col gap-2 overflow-y-auto">
                    {notificationsData?.items.length ? (
                      notificationsData.items.map((notification) => (
                        <button
                          key={notification.id}
                          className={clsx(
                            "rounded-lg border border-border p-2 text-left text-sm",
                            notification.is_read ? "bg-background" : "bg-primary/5"
                          )}
                          onClick={() => handleReadNotification(notification.id)}
                        >
                          <p className="font-medium text-foreground">{notification.title}</p>
                          {notification.body && <p className="text-xs text-muted-foreground">{notification.body}</p>}
                        </button>
                      ))
                    ) : (
                      <p className="py-4 text-center text-sm text-muted-foreground">No notifications yet.</p>
                    )}
                  </div>
                </div>
              )}
            </div>
            <button
              onClick={toggleTheme}
              className="rounded-lg p-2 text-muted-foreground hover:bg-muted"
              aria-label="Toggle theme"
            >
              {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
            </button>
            <button
              onClick={logout}
              className="rounded-lg p-2 text-muted-foreground hover:bg-muted"
              aria-label="Log out"
            >
              <LogOut size={16} />
            </button>
          </div>
        </header>
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
