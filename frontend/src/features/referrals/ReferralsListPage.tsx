import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { Plus } from "lucide-react";
import { referralsApi } from "@/api/referrals";
import { Card, StatusChip } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function ReferralsListPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["referrals"],
    queryFn: () => referralsApi.list(),
  });

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-foreground">Referrals</h1>
          <p className="text-sm text-muted-foreground">Track every candidate from referral to offer.</p>
        </div>
        <Link to="/referrals/new">
          <Button>
            <Plus size={16} /> New referral
          </Button>
        </Link>
      </div>

      <Card>
        {isLoading && (
          <div className="divide-y divide-border">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="flex items-center gap-4 p-4">
                <div className="h-4 w-1/4 animate-pulse rounded bg-muted" />
                <div className="h-4 w-1/3 animate-pulse rounded bg-muted" />
                <div className="h-4 w-20 animate-pulse rounded bg-muted" />
              </div>
            ))}
          </div>
        )}

        {isError && (
          <div className="p-8 text-center text-sm text-danger">
            Couldn't load referrals. Please try again.
          </div>
        )}

        {!isLoading && !isError && data?.items.length === 0 && (
          <div className="flex flex-col items-center gap-2 p-12 text-center">
            <p className="text-sm font-medium text-foreground">No referrals yet</p>
            <p className="text-sm text-muted-foreground">
              Create your first referral to get the workflow started.
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.items.length > 0 && (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-muted-foreground">
                <th className="px-4 py-3 font-medium">Candidate</th>
                <th className="px-4 py-3 font-medium">Position</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {data.items.map((r) => (
                <tr key={r.id} className="hover:bg-muted/50">
                  <td className="px-4 py-3">
                    <Link to={`/referrals/${r.id}`} className="font-medium text-foreground hover:underline">
                      {r.candidate_full_name}
                    </Link>
                    <p className="text-xs text-muted-foreground">{r.candidate_email}</p>
                  </td>
                  <td className="px-4 py-3 text-foreground">{r.position_applied}</td>
                  <td className="px-4 py-3">
                    <StatusChip status={r.status} />
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {new Date(r.updated_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}
