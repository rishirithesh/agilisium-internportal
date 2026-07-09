<<<<<<< HEAD
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
=======
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/login';
import { Apply } from './pages/apply';
import { Dashboard } from './pages/dashboard';
import { getToken } from './services/api';

// Route guards
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = getToken();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = getToken();
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public auth-less pages */}
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        <Route path="/apply" element={<Apply />} />

        {/* Protected Dashboard pages */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />

        {/* Fallbacks */}
        <Route 
          path="*" 
          element={<Navigate to="/dashboard" replace />} 
>>>>>>> master
        />
      </Routes>
    </BrowserRouter>
  );
<<<<<<< HEAD
}
=======
};
export default App;
>>>>>>> master
