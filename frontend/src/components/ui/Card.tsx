import type { ReactNode } from "react";
import clsx from "clsx";
import type { ReferralStatus } from "@/types/domain";

export function Card({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div className={clsx("rounded-xl border border-border bg-surface shadow-sm", className)}>
      {children}
    </div>
  );
}

const STATUS_STYLE: Record<ReferralStatus, string> = {
  REFERRED: "bg-muted text-muted-foreground",
  INTERN_REGISTERED: "bg-blue-500/10 text-blue-500",
  EMPLOYEE_APPROVED: "bg-blue-500/10 text-blue-500",
  PROFILE_SUBMITTED: "bg-amber-500/10 text-amber-500",
  ADMIN_REVIEW: "bg-amber-500/10 text-amber-500",
  CHANGES_REQUESTED: "bg-orange-500/10 text-orange-500",
  OFFER_GENERATED: "bg-violet-500/10 text-violet-500",
  OFFER_UPLOADED: "bg-violet-500/10 text-violet-500",
  OFFER_SENT: "bg-violet-500/10 text-violet-500",
  OFFER_ACCEPTED: "bg-success/10 text-success",
  COMPLETED: "bg-success/10 text-success",
  REJECTED: "bg-danger/10 text-danger",
};

export function StatusChip({ status }: { status: ReferralStatus }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium",
        STATUS_STYLE[status]
      )}
    >
      {(status as string).split("_").join(" ")}
    </span>
  );
}
