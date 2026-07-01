import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { authApi } from "@/api/auth";
import { useAuth } from "@/features/auth/AuthContext";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";

const passwordSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});
type PasswordForm = z.infer<typeof passwordSchema>;

const otpRequestSchema = z.object({ email: z.string().email("Enter a valid email") });
const otpVerifySchema = z.object({ otp_code: z.string().length(6, "Enter the 6-digit code") });

export default function LoginPage() {
  const navigate = useNavigate();
  const { refetchUser } = useAuth();
  const [mode, setMode] = useState<"password" | "otp">("password");
  const [otpStage, setOtpStage] = useState<"request" | "verify">("request");
  const [otpEmail, setOtpEmail] = useState("");
  const [serverError, setServerError] = useState<string | null>(null);

  const passwordForm = useForm<PasswordForm>({ resolver: zodResolver(passwordSchema) });
  const otpRequestForm = useForm<{ email: string }>({ resolver: zodResolver(otpRequestSchema) });
  const otpVerifyForm = useForm<{ otp_code: string }>({ resolver: zodResolver(otpVerifySchema) });

  const onPasswordSubmit = async (values: PasswordForm) => {
    setServerError(null);
    try {
      await authApi.login(values.email, values.password);
      await refetchUser();
      navigate("/");
    } catch {
      setServerError("Invalid email or password");
    }
  };

  const onOtpRequest = async (values: { email: string }) => {
    setServerError(null);
    try {
      await authApi.requestOtp(values.email);
      setOtpEmail(values.email);
      setOtpStage("verify");
    } catch {
      setServerError("Could not send code. Please try again.");
    }
  };

  const onOtpVerify = async (values: { otp_code: string }) => {
    setServerError(null);
    try {
      await authApi.verifyOtp(otpEmail, values.otp_code);
      await refetchUser();
      navigate("/");
    } catch {
      setServerError("Invalid or expired code");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <Card className="w-full max-w-sm p-8">
        <div className="flex items-center gap-3">
          <img src="/favicon.ico" alt="AIRP logo" className="h-10 w-10 rounded-lg" />
          <div>
            <h1 className="text-xl font-semibold text-foreground">Sign in to AIRP</h1>
            <p className="mt-1 text-sm text-muted-foreground">Agilisium Intern Referral Portal</p>
          </div>
        </div>

        <div className="mt-6 flex rounded-lg border border-border p-1 text-sm">
          <button
            className={`flex-1 rounded-md py-1.5 ${mode === "password" ? "bg-primary text-primary-foreground" : "text-muted-foreground"}`}
            onClick={() => setMode("password")}
          >
            Password
          </button>
          <button
            className={`flex-1 rounded-md py-1.5 ${mode === "otp" ? "bg-primary text-primary-foreground" : "text-muted-foreground"}`}
            onClick={() => setMode("otp")}
          >
            Email code
          </button>
        </div>

        {serverError && <p className="mt-4 text-sm text-danger">{serverError}</p>}

        {mode === "password" && (
          <form className="mt-6 flex flex-col gap-4" onSubmit={passwordForm.handleSubmit(onPasswordSubmit)}>
            <Input
              label="Email"
              type="email"
              {...passwordForm.register("email")}
              error={passwordForm.formState.errors.email?.message}
            />
            <Input
              label="Password"
              type="password"
              {...passwordForm.register("password")}
              error={passwordForm.formState.errors.password?.message}
            />
            <Button type="submit" isLoading={passwordForm.formState.isSubmitting}>
              Sign in
            </Button>
          </form>
        )}

        {mode === "otp" && otpStage === "request" && (
          <form className="mt-6 flex flex-col gap-4" onSubmit={otpRequestForm.handleSubmit(onOtpRequest)}>
            <Input
              label="Email"
              type="email"
              {...otpRequestForm.register("email")}
              error={otpRequestForm.formState.errors.email?.message}
            />
            <Button type="submit" isLoading={otpRequestForm.formState.isSubmitting}>
              Send code
            </Button>
          </form>
        )}

        {mode === "otp" && otpStage === "verify" && (
          <form className="mt-6 flex flex-col gap-4" onSubmit={otpVerifyForm.handleSubmit(onOtpVerify)}>
            <p className="text-sm text-muted-foreground">Code sent to {otpEmail}</p>
            <Input
              label="6-digit code"
              maxLength={6}
              {...otpVerifyForm.register("otp_code")}
              error={otpVerifyForm.formState.errors.otp_code?.message}
            />
            <Button type="submit" isLoading={otpVerifyForm.formState.isSubmitting}>
              Verify &amp; sign in
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
}
