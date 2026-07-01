import { useEffect, useState } from "react";
import { offersApi } from "@/api/offers";
import { Button } from "@/components/ui/Button";
import { Link } from "react-router-dom";

export default function OffersListPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      const data = await offersApi.list();
      setItems(data || []);
    })();
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Offers</h2>
      <ul className="space-y-2">
        {items.map((o) => (
          <li key={o.id} className="p-4 border rounded">
            <div className="flex items-center justify-between">
              <div>
                <Link to={`/offers/${o.id}`} className="font-semibold text-primary">{o.position_title}</Link>
                <div className="text-sm text-muted">Referral: {o.referral_id}</div>
              </div>
              <div className="flex gap-2">
                <a href={offersApi.downloadUrl(o.id)} target="_blank" rel="noreferrer">
                  <Button variant="secondary">Download</Button>
                </a>
                <Link to={`/offers/${o.id}`}>
                  <Button variant="ghost">Details</Button>
                </Link>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
