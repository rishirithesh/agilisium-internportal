import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { referralsApi } from "@/api/referrals";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  candidate_full_name: z.string().min(2, "Required"),
  candidate_email: z.string().email("Enter a valid email"),
  candidate_phone: z.string().optional(),
  position_applied: z.string().min(2, "Required"),
  relationship_to_candidate: z.string().optional(),
  referral_notes: z.string().optional(),
});
type FormValues = z.infer<typeof schema>;

export default function CreateReferralPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const mutation = useMutation({
    mutationFn: referralsApi.create,
    onSuccess: (referral) => {
      queryClient.invalidateQueries({ queryKey: ["referrals"] });
      navigate(`/referrals/${referral.id}`);
    },
  });

  return (
    <div className="mx-auto max-w-xl">
      <h1 className="text-lg font-semibold text-foreground">New referral</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Refer a candidate into the intern pipeline.
      </p>

      <Card className="mt-6 p-6">
        <form
          className="flex flex-col gap-4"
          onSubmit={handleSubmit((values) => mutation.mutate(values))}
        >
          <Input
            label="Candidate full name"
            {...register("candidate_full_name")}
            error={errors.candidate_full_name?.message}
          />
          <Input
            label="Candidate email"
            type="email"
            {...register("candidate_email")}
            error={errors.candidate_email?.message}
          />
          <Input label="Candidate phone (optional)" {...register("candidate_phone")} />
          <Input
            label="Position applied for"
            {...register("position_applied")}
            error={errors.position_applied?.message}
          />
          <Input
            label="Your relationship to the candidate (optional)"
            {...register("relationship_to_candidate")}
          />
          <Input label="Notes (optional)" {...register("referral_notes")} />

          {mutation.isError && (
            <p className="text-sm text-danger">Couldn't submit the referral. Please try again.</p>
          )}

          <div className="mt-2 flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={() => navigate("/referrals")}>
              Cancel
            </Button>
            <Button type="submit" isLoading={isSubmitting || mutation.isPending}>
              Submit referral
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
