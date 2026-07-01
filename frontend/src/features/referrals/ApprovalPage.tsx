import { useSearchParams, useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { referralsApi } from "@/api/referrals";

export default function ApprovalPage() {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const { id } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      if (!id || !token) return;
      try {
        await referralsApi.approveByToken(id, token);
        setMessage("Referral approved successfully.");
        setTimeout(() => navigate("/referrals"), 2500);
      } catch (err: any) {
        setMessage(err?.response?.data?.detail || String(err));
      }
    })();
  }, [id, token]);

  return (
    <div className="max-w-xl mx-auto mt-12">
      <h2 className="text-xl font-semibold mb-4">Processing approval...</h2>
      {message && <p>{message}</p>}
    </div>
  );
}
