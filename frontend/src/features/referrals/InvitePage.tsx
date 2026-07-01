import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { referralsApi } from "@/api/referrals";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export default function InvitePage() {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const referralId = params.get("referral_id") || "";
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await referralsApi.registerCandidate(referralId, token, email, password, { full_name: name });
      setMessage("Registration submitted — awaiting employee approval.");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err: any) {
      setMessage(err?.response?.data?.detail || String(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-12">
      <h2 className="text-2xl font-bold mb-4">You're invited to join</h2>
      <form onSubmit={submit} className="space-y-4">
        <Input label="Full name" value={name} onChange={(e) => setName(e.target.value)} required />
        <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <div className="pt-2">
          <Button type="submit" isLoading={isSubmitting}>
            Register
          </Button>
        </div>
      </form>
      {message && <p className="mt-4 text-sm">{message}</p>}
    </div>
  );
}
