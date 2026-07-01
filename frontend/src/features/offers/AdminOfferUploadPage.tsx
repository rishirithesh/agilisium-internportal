import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { adminOffersApi } from "@/api/adminOffers";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function AdminOfferUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [position, setPosition] = useState("");
  const [referralId, setReferralId] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return setMessage("Please select a PDF file");
    const fd = new FormData();
    fd.append("file", file);
    fd.append("position_title", position);
    if (referralId) fd.append("referral_id", referralId);

    setIsSubmitting(true);
    try {
      const data = await adminOffersApi.upload(fd);
      setMessage("Uploaded successfully");
      setTimeout(() => navigate(`/admin/offers/${data.id}/versions`), 1000);
    } catch (err: any) {
      setMessage(err?.response?.data?.detail || String(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-8">
      <h1 className="text-xl font-semibold mb-4">Upload Offer</h1>
      <form onSubmit={submit} className="space-y-4">
        <Input label="Position title" value={position} onChange={(e) => setPosition(e.target.value)} required />
        <Input label="Referral ID (optional)" value={referralId} onChange={(e) => setReferralId(e.target.value)} />
        <div>
          <label className="text-sm font-medium block mb-1">Offer PDF</label>
          <input aria-label="Offer PDF" type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </div>
        <div className="pt-2">
          <Button type="submit" isLoading={isSubmitting}>Upload</Button>
        </div>
      </form>
      {message && <p className="mt-3 text-sm">{message}</p>}
    </div>
  );
}
