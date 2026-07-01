import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "@/features/auth/LoginPage";
import DashboardPage from "@/features/dashboard/DashboardPage";
import ReferralsListPage from "@/features/referrals/ReferralsListPage";
import CreateReferralPage from "@/features/referrals/CreateReferralPage";
import ReferralDetailPage from "@/features/referrals/ReferralDetailPage";
import InvitePage from "@/features/referrals/InvitePage";
import ApprovalPage from "@/features/referrals/ApprovalPage";
import OffersListPage from "@/features/offers/OffersListPage";
import OfferDetailPage from "@/features/offers/OfferDetailPage";
import AdminOfferUploadPage from "@/features/offers/AdminOfferUploadPage";
import OfferVersionsPage from "@/features/offers/OfferVersionsPage";
import ProtectedRoute from "@/components/layout/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/referrals"
          element={
            <ProtectedRoute>
              <ReferralsListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/referrals/new"
          element={
            <ProtectedRoute>
              <CreateReferralPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/referrals/:id"
          element={
            <ProtectedRoute>
              <ReferralDetailPage />
            </ProtectedRoute>
          }
        />
        <Route path="/invite" element={<InvitePage />} />
        <Route path="/admin/referrals/:id/approve" element={<ApprovalPage />} />
        <Route
          path="/offers"
          element={
            <ProtectedRoute>
              <OffersListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/offers/:id"
          element={
            <ProtectedRoute>
              <OfferDetailPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/offers/upload"
          element={
            <ProtectedRoute>
              <AdminOfferUploadPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/offers/:id/versions"
          element={
            <ProtectedRoute>
              <OfferVersionsPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
