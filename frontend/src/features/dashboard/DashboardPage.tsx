import { useQuery } from "@tanstack/react-query";
import { referralsApi } from "@/api/referrals";
import { Card } from "@/components/ui/Card";
import { useAuth } from "@/features/auth/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();
  const { data } = useQuery({ queryKey: ["referrals", "dashboard"], queryFn: () => referralsApi.list(1, 100) });

  const total = data?.total ?? 0;
  const completed = data?.items.filter((r) => r.status === "COMPLETED").length ?? 0;
  const inProgress = total - completed - (data?.items.filter((r) => r.status === "REJECTED").length ?? 0);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-lg font-semibold text-foreground">Welcome back, {user?.full_name?.split(" ")[0]}</h1>
        <p className="text-sm text-muted-foreground">Here's what's happening across your referrals.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card className="p-5">
          <p className="text-xs text-muted-foreground">Total referrals</p>
          <p className="mt-2 text-2xl font-semibold text-foreground">{total}</p>
        </Card>
        <Card className="p-5">
          <p className="text-xs text-muted-foreground">In progress</p>
          <p className="mt-2 text-2xl font-semibold text-foreground">{inProgress}</p>
        </Card>
        <Card className="p-5">
          <p className="text-xs text-muted-foreground">Completed</p>
          <p className="mt-2 text-2xl font-semibold text-foreground">{completed}</p>
        </Card>
      </div>
    </div>
  );
}
