import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { adminOffersApi } from "@/api/adminOffers";
import { Button } from "@/components/ui/Button";
import { offersApi } from "@/api/offers";

export default function OfferVersionsPage() {
  const { id } = useParams<{ id: string }>();
  const { data: versions } = useQuery({ queryKey: ["offer-versions", id], queryFn: () => adminOffersApi.versions(id!), enabled: !!id });

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <h1 className="text-xl font-semibold mb-4">Offer Versions</h1>
      <ul className="space-y-3">
        {(versions || []).map((v: any) => (
          <li key={v.id} className="p-4 border rounded flex items-center justify-between">
            <div>
              <div className="font-medium">Version {v.version_number} · {new Date(v.created_at).toLocaleString()}</div>
              <div className="text-sm text-muted">Uploaded by: {v.uploaded_by ?? "system"}</div>
            </div>
            <div className="flex gap-2">
              <a href={offersApi.downloadUrl(v.offer_id)} target="_blank" rel="noreferrer">
                <Button variant="secondary">Download Latest</Button>
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
