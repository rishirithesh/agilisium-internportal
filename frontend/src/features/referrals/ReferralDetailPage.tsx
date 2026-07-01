import { useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { referralsApi } from "@/api/referrals";
import { Card, StatusChip } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/features/auth/AuthContext";
import type { ReferralStatus } from "@/types/domain";

// Mirrors the backend state machine's allowed targets per status, scoped to what
// each role is realistically expected to trigger from this single-page view.
const NEXT_STEPS: Partial<Record<ReferralStatus, { target: ReferralStatus; label: string }[]>> = {
  REFERRED: [{ target: "INTERN_REGISTERED", label: "Mark intern registered" }],
  INTERN_REGISTERED: [{ target: "EMPLOYEE_APPROVED", label: "Approve as employee" }],
  EMPLOYEE_APPROVED: [{ target: "PROFILE_SUBMITTED", label: "Submit intern profile" }],
  PROFILE_SUBMITTED: [{ target: "ADMIN_REVIEW", label: "Send for admin review" }],
  ADMIN_REVIEW: [
    { target: "OFFER_GENERATED", label: "Generate offer" },
    { target: "CHANGES_REQUESTED", label: "Request changes" },
    { target: "REJECTED", label: "Reject" },
  ],
  CHANGES_REQUESTED: [{ target: "PROFILE_SUBMITTED", label: "Resubmit profile" }],
  OFFER_GENERATED: [{ target: "OFFER_UPLOADED", label: "Mark offer uploaded" }],
  OFFER_UPLOADED: [{ target: "OFFER_SENT", label: "Send offer" }],
  OFFER_SENT: [{ target: "OFFER_ACCEPTED", label: "Mark offer accepted" }],
  OFFER_ACCEPTED: [{ target: "COMPLETED", label: "Mark completed" }],
};

export default function ReferralDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const { data: referral, isLoading } = useQuery({
    queryKey: ["referral", id],
    queryFn: () => referralsApi.get(id!),
    enabled: !!id,
  });

  const transition = useMutation({
    mutationFn: (target: ReferralStatus) => referralsApi.transition(id!, target),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["referral", id] });
      queryClient.invalidateQueries({ queryKey: ["referrals"] });
    },
  });

  if (isLoading || !referral) {
    return <div className="h-40 animate-pulse rounded-xl bg-muted" />;
  }

  const nextSteps = NEXT_STEPS[referral.status] ?? [];

  return (
    <div className="mx-auto max-w-2xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-foreground">{referral.candidate_full_name}</h1>
          <p className="text-sm text-muted-foreground">{referral.position_applied}</p>
        </div>
        <StatusChip status={referral.status} />
      </div>

      <Card className="mt-6 p-6">
        <dl className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <dt className="text-muted-foreground">Candidate email</dt>
            <dd className="text-foreground">{referral.candidate_email}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">Phone</dt>
            <dd className="text-foreground">{referral.candidate_phone ?? "—"}</dd>
          </div>
          <div className="col-span-2">
            <dt className="text-muted-foreground">Notes</dt>
            <dd className="text-foreground">{referral.referral_notes ?? "—"}</dd>
          </div>
        </dl>

        {nextSteps.length > 0 && (
          <div className="mt-6 flex flex-wrap gap-2 border-t border-border pt-4">
            {nextSteps.map((step) => (
              <Button
                key={step.target}
                variant={step.target === "REJECTED" ? "danger" : "primary"}
                isLoading={transition.isPending}
                onClick={() => transition.mutate(step.target)}
              >
                {step.label}
              </Button>
            ))}
          </div>
        )}
      </Card>

      <Card className="mt-6 p-6">
        <h2 className="text-sm font-semibold text-foreground">Timeline</h2>
        <ol className="mt-4 flex flex-col gap-4">
          {referral.timeline_events.map((event) => (
            <li key={event.id} className="flex items-start gap-3 text-sm">
              <div className="mt-1 h-2 w-2 shrink-0 rounded-full bg-primary" />
              <div>
                <p className="text-foreground">
                  {event.from_status ? `${event.from_status} → ${event.to_status}` : `Created (${event.to_status})`}
                </p>
                <p className="text-xs text-muted-foreground">
                  {new Date(event.created_at).toLocaleString()}
                  {event.note ? ` · ${event.note}` : ""}
                </p>
              </div>
            </li>
          ))}
        </ol>
      </Card>

      <p className="mt-4 text-xs text-muted-foreground">Viewing as {user?.role.replace("_", " ")}</p>
    </div>
  );
}
