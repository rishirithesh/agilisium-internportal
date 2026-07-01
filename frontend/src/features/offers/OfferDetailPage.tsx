import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { offersApi } from "@/api/offers";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function OfferDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: offer, isLoading } = useQuery({ queryKey: ["offer", id], queryFn: () => offersApi.get(id!), enabled: !!id });

  const accept = useMutation({
    mutationFn: () => offersApi.accept(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["offers"] });
      queryClient.invalidateQueries({ queryKey: ["offer", id] });
      navigate("/offers");
    },
  });

  if (isLoading || !offer) return <div className="h-40 animate-pulse rounded-xl bg-muted" />;

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">{offer.position_title}</h1>
          <p className="text-sm text-muted-foreground">Referral: {offer.referral_id}</p>
        </div>
        <div className="flex gap-2">
          <a href={offersApi.downloadUrl(offer.id)} target="_blank" rel="noreferrer">
            <Button variant="secondary">Download Offer</Button>
          </a>
          <Button variant="primary" isLoading={accept.isPending} onClick={() => accept.mutate()}>
            Accept Offer
          </Button>
        </div>
      </div>

      <Card className="mt-6 p-6">
        <h2 className="text-sm font-semibold text-foreground">Details</h2>
        <dl className="mt-4 grid grid-cols-2 gap-4 text-sm">
          <div>
            <dt className="text-muted-foreground">Start date</dt>
            <dd className="text-foreground">{offer.start_date ?? "—"}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">Location</dt>
            <dd className="text-foreground">{offer.location ?? "—"}</dd>
          </div>
          <div className="col-span-2">
            <dt className="text-muted-foreground">Notes</dt>
            <dd className="text-foreground">{offer.notes ?? "—"}</dd>
          </div>
        </dl>
      </Card>
    </div>
  );
}
