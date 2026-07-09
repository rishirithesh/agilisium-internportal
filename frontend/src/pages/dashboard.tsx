import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LogOut, Settings, Award, Calendar, FileDown,
  Upload, Layers, CheckCircle2, XCircle, Users, BarChart3,
  Plus, Trash2, Database, Clock, RefreshCw, FileText, Loader2
} from 'lucide-react';
import { api, clearToken, getRole, getEmail, User, Internship, Attendance, Project, CompanyProject, AuditLog, Analytics } from '../services/api';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const role = getRole();
  const email = getEmail();

  const [loading, setLoading] = useState(true);

  // Navigation active tab
  const [activeTab, setActiveTab] = useState('');

  useEffect(() => {
    if (!role) {
      navigate('/login');
      return;
    }

    // Set default tab based on role
    if (role === 'Super Admin') setActiveTab('analytics');
    else if (role === 'Admin') setActiveTab('applications');
    else if (role === 'Employee') setActiveTab('referrals');
    else if (role === 'Intern') setActiveTab('portal');

    setLoading(false);
  }, [role, navigate]);

  const handleLogout = () => {
    clearToken();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <RefreshCw className="w-8 h-8 text-brand-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex bg-neutral-50">
      {/* Sidebar */}
      <div className="w-64 border-r border-neutral-200 bg-white flex flex-col justify-between shrink-0">
        <div>
          {/* Logo / Branding */}
          <div className="p-6 border-b border-neutral-100 flex items-center gap-3">
            <img src="/favicon.ico" alt="AIRP Logo" className="w-8 h-8" />
            <div>
              <h1 className="font-bold text-sm text-neutral-900 tracking-tight">Agilisium AIRP</h1>
              <p className="text-[10px] text-neutral-400 font-semibold uppercase tracking-wider">Intern & Referral Portal</p>
            </div>
          </div>

          {/* User profile brief */}
          <div className="px-6 py-4 border-b border-neutral-50 bg-neutral-50/40">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm">
                {email ? email.substring(0, 2).toUpperCase() : 'US'}
              </div>
              <div className="truncate">
                <p className="text-xs font-semibold text-neutral-800 truncate">{email}</p>
                <span className="inline-flex mt-0.5 px-1.5 py-0.5 rounded text-[9px] font-bold tracking-wide uppercase bg-brand-50 text-brand-700 border border-brand-100">
                  {role}
                </span>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1">
            {role === 'Super Admin' && (
              <>
                <SidebarLink icon={<BarChart3 />} label="Analytics" active={activeTab === 'analytics'} onClick={() => setActiveTab('analytics')} />
                <SidebarLink icon={<Users />} label="Accounts Management" active={activeTab === 'accounts'} onClick={() => setActiveTab('accounts')} />
                <SidebarLink icon={<Settings />} label="SMTP Configuration" active={activeTab === 'smtp'} onClick={() => setActiveTab('smtp')} />
                <SidebarLink icon={<Database />} label="System Audit Logs" active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} />
              </>
            )}

            {role === 'Admin' && (
              <>
                <SidebarLink icon={<Layers />} label="Applications Review" active={activeTab === 'applications'} onClick={() => setActiveTab('applications')} />
                <SidebarLink icon={<Users />} label="Interns Tracker" active={activeTab === 'tracker'} onClick={() => setActiveTab('tracker')} />
                <SidebarLink icon={<Award />} label="Company Projects" active={activeTab === 'projects'} onClick={() => setActiveTab('projects')} />
                <SidebarLink icon={<Calendar />} label="Attendance Records" active={activeTab === 'attendance'} onClick={() => setActiveTab('attendance')} />
              </>
            )}

            {role === 'Employee' && (
              <>
                <SidebarLink icon={<Layers />} label="Pending Referrals" active={activeTab === 'referrals'} onClick={() => setActiveTab('referrals')} />
                <SidebarLink icon={<Users />} label="Referred Interns" active={activeTab === 'referred_list'} onClick={() => setActiveTab('referred_list')} />
              </>
            )}

            {role === 'Intern' && (
              <>
                <SidebarLink icon={<Award />} label="Internship Journey" active={activeTab === 'portal'} onClick={() => setActiveTab('portal')} />
              </>
            )}
          </nav>
        </div>

        {/* Footer actions */}
        <div className="p-4 border-t border-neutral-100 bg-neutral-50/50">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 py-2 px-3 hover:bg-red-50 hover:text-red-700 text-neutral-600 rounded-lg text-sm font-medium transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 border-b border-neutral-200 bg-white flex items-center justify-between px-8">
          <h2 className="font-semibold text-neutral-800 text-lg">
            {activeTab.charAt(0).toUpperCase() + activeTab.slice(1).replace('_', ' ')}
          </h2>
          <div className="text-xs text-neutral-400 font-medium">
            Logged in as: {email} ({role})
          </div>
        </header>

        {/* Scrollable Container */}
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            {role === 'Super Admin' && activeTab === 'analytics' && <SuperAdminAnalytics />}
            {role === 'Super Admin' && activeTab === 'accounts' && <SuperAdminAccounts />}
            {role === 'Super Admin' && activeTab === 'smtp' && <SuperAdminSMTP />}
            {role === 'Super Admin' && activeTab === 'logs' && <SuperAdminLogs />}

            {role === 'Admin' && activeTab === 'applications' && <AdminApplications />}
            {role === 'Admin' && activeTab === 'tracker' && <AdminTracker />}
            {role === 'Admin' && activeTab === 'projects' && <AdminProjects />}
            {role === 'Admin' && activeTab === 'attendance' && <AdminAttendance />}

            {role === 'Employee' && activeTab === 'referrals' && <EmployeeReferrals />}
            {role === 'Employee' && activeTab === 'referred_list' && <EmployeeReferredList />}

            {role === 'Intern' && activeTab === 'portal' && <InternPortal />}
          </div>
        </main>
      </div>
    </div>
  );
};

// --- Sidebar Link Helper Component ---
interface SidebarLinkProps {
  icon: React.ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}
const SidebarLink: React.FC<SidebarLinkProps> = ({ icon, label, active, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg transition-colors ${active
        ? 'bg-brand-50 text-brand-700'
        : 'text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900'
        }`}
    >
      {React.cloneElement(icon as React.ReactElement, { className: 'w-4 h-4 shrink-0' })}
      <span>{label}</span>
    </button>
  );
};

// ==========================================
// ROLE SUB-COMPONENTS
// ==========================================

// --- Super Admin: Analytics ---
const SuperAdminAnalytics: React.FC = () => {
  const [data, setData] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAnalytics().then(setData).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12"><RefreshCw className="w-6 h-6 animate-spin mx-auto text-neutral-400" /></div>;
  if (!data) return <div className="text-red-500">Failed to load analytics.</div>;

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <AnalyticsCard icon={<Layers className="text-blue-500" />} label="Total Applications" value={data.total_applications} />
        <AnalyticsCard icon={<Clock className="text-amber-500" />} label="Pending Referrals" value={data.pending_referrals} />
        <AnalyticsCard icon={<Award className="text-emerald-500" />} label="Active Interns" value={data.active_interns} />
        <AnalyticsCard icon={<CheckCircle2 className="text-indigo-500" />} label="Completed Internships" value={data.completed_internships} />
      </div>

      <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Status Breakdown</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.by_status).map(([status, count]) => (
            <div key={status} className="border border-neutral-100 bg-neutral-50/50 rounded-lg p-4">
              <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">{status.replace('_', ' ')}</p>
              <p className="text-xl font-bold text-neutral-800 mt-1">{count}</p>
            </div>
          ))}
          {Object.keys(data.by_status).length === 0 && (
            <div className="col-span-4 text-center py-6 text-xs text-neutral-400">No statuses recorded yet.</div>
          )}
        </div>
      </div>
    </div>
  );
};

const AnalyticsCard: React.FC<{ icon: React.ReactNode; label: string; value: number }> = ({ icon, label, value }) => (
  <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm flex items-center gap-4">
    <div className="p-3 bg-neutral-50 rounded-lg">{icon}</div>
    <div>
      <p className="text-xs font-semibold text-neutral-400 uppercase tracking-wider">{label}</p>
      <p className="text-2xl font-bold text-neutral-800 mt-0.5">{value}</p>
    </div>
  </div>
);

// --- Super Admin: Accounts Management ---
const SuperAdminAccounts: React.FC = () => {
  const [accounts, setAccounts] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('Employee');

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const loadAccounts = () => {
    setLoading(true);
    api.getAccounts().then(setAccounts).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');

    if (!email.toLowerCase().endsWith('@agilisium.com')) {
      setError('Emails must end with @agilisium.com');
      setSubmitting(false);
      return;
    }

    try {
      await api.createAccount(email, role, true);
      setSuccess(`Successfully created ${role} account! (Default password is ${role === 'Admin' ? 'Admin@123' : 'Employee@123'})`);
      setEmail('');
      loadAccounts();
    } catch (err: any) {
      setError(err.message || 'Failed to create account.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in">
      {/* Create Account Form */}
      <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm h-fit">
        <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Create Account</h3>
        {error && <div className="mb-4 p-3 bg-red-50 text-red-700 border border-red-100 text-xs rounded-lg">{error}</div>}
        {success && <div className="mb-4 p-3 bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs rounded-lg">{success}</div>}

        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@agilisium.com"
              className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">System Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none bg-white focus:border-brand-500"
            >
              <option value="Employee">Employee</option>
              <option value="Admin">Admin</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-semibold py-2 rounded-lg text-sm flex items-center justify-center gap-2 transition-colors disabled:opacity-75"
          >
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            Create User Account
          </button>
        </form>
      </div>

      {/* Accounts List */}
      <div className="lg:col-span-2 bg-white border border-neutral-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Created Accounts</h3>
        {loading ? (
          <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                  <th className="pb-3">Email</th>
                  <th className="pb-3">Role</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Created At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-50">
                {accounts.map((acc) => (
                  <tr key={acc.id} className="text-neutral-700">
                    <td className="py-3 font-medium">{acc.email}</td>
                    <td className="py-3">
                      <span className={`inline-flex px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase ${acc.role === 'Admin' ? 'bg-indigo-50 text-indigo-700' : 'bg-amber-50 text-amber-700'
                        }`}>
                        {acc.role}
                      </span>
                    </td>
                    <td className="py-3">
                      <span className="inline-flex items-center gap-1 text-emerald-600 text-xs font-semibold">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                        Active
                      </span>
                    </td>
                    <td className="py-3 text-neutral-400 text-xs">{new Date(acc.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
                {accounts.length === 0 && (
                  <tr>
                    <td colSpan={4} className="text-center py-6 text-neutral-400 text-xs">No admin or employee accounts created yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// --- Super Admin: SMTP Configuration ---
const SuperAdminSMTP: React.FC = () => {
  const [host, setHost] = useState('');
  const [port, setPort] = useState(587);
  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');
  const [fromEmail, setFromEmail] = useState('');

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    api.getSMTPConfig().then((cfg) => {
      setHost(cfg.host);
      setPort(cfg.port);
      setUser(cfg.user);
      setPassword(cfg.password || '');
      setFromEmail(cfg.from_email);
    }).finally(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await api.updateSMTPConfig({ host, port, user, password, from_email: fromEmail });
      setSuccess('SMTP settings saved successfully!');
    } catch (err: any) {
      setError(err.message || 'Failed to save SMTP configurations.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center py-12"><RefreshCw className="w-6 h-6 animate-spin mx-auto text-neutral-400" /></div>;

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm max-w-xl mx-auto animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Configure System SMTP Server</h3>

      {error && <div className="mb-4 p-3 bg-red-50 text-red-700 border border-red-100 text-xs rounded-lg">{error}</div>}
      {success && <div className="mb-4 p-3 bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs rounded-lg">{success}</div>}

      <form onSubmit={handleSave} className="space-y-4">
        <div>
          <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">SMTP Host</label>
          <input
            type="text"
            required
            value={host}
            onChange={(e) => setHost(e.target.value)}
            placeholder="smtp.gmail.com"
            className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">SMTP Port</label>
          <input
            type="number"
            required
            value={port}
            onChange={(e) => setPort(Number(e.target.value))}
            placeholder="587"
            className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">SMTP Username / Email</label>
          <input
            type="text"
            required
            value={user}
            onChange={(e) => setUser(e.target.value)}
            placeholder="hr@agilisium.com"
            className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">SMTP Password / App Password</label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••••••"
            className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Sender From Address</label>
          <input
            type="text"
            required
            value={fromEmail}
            onChange={(e) => setFromEmail(e.target.value)}
            placeholder="Agilisium AIRP <hr@agilisium.com>"
            className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
          />
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-semibold py-2 rounded-lg text-sm flex items-center justify-center gap-2 transition-colors disabled:opacity-75"
        >
          {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
          Save Configuration
        </button>
      </form>
    </div>
  );
};

// --- Super Admin: Audit Logs ---
const SuperAdminLogs: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAuditLogs().then(setLogs).finally(() => setLoading(false));
  }, []);

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">System Audit Trail</h3>
      {loading ? (
        <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                <th className="pb-3">Timestamp</th>
                <th className="pb-3">User Email</th>
                <th className="pb-3">Action</th>
                <th className="pb-3">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-50 text-xs">
              {logs.map((log) => (
                <tr key={log.id} className="text-neutral-700">
                  <td className="py-3 font-semibold text-neutral-400 shrink-0">{new Date(log.created_at).toLocaleString()}</td>
                  <td className="py-3 font-semibold">{log.user_email || 'System / Public'}</td>
                  <td className="py-3">
                    <span className="inline-flex px-1.5 py-0.5 rounded font-bold uppercase text-[9px] tracking-wide bg-neutral-100 text-neutral-700 border border-neutral-200">
                      {log.action}
                    </span>
                  </td>
                  <td className="py-3 text-neutral-600 max-w-sm truncate" title={log.details || ''}>{log.details}</td>
                </tr>
              ))}
              {logs.length === 0 && (
                <tr>
                  <td colSpan={4} className="text-center py-6 text-neutral-400">No logs found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// --- Admin: Applications Review ---
const AdminApplications: React.FC = () => {
  const [apps, setApps] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedApp, setSelectedApp] = useState<Internship | null>(null);

  const [offerFile, setOfferFile] = useState<File | null>(null);
  const [rejectReason, setRejectReason] = useState('');

  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState('');

  const loadApps = () => {
    setLoading(true);
    api.getApplications().then(setApps).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadApps();
  }, []);

  const handleApprove = async () => {
    if (!selectedApp || !offerFile) {
      setError('Please upload a PDF offer letter.');
      return;
    }
    setActionLoading(true);
    setError('');

    try {
      await api.approveApplication(selectedApp.id, offerFile);
      setSelectedApp(null);
      setOfferFile(null);
      loadApps();
    } catch (err: any) {
      setError(err.message || 'Failed to approve application.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async () => {
    if (!selectedApp || !rejectReason) {
      setError('Please provide a reason for rejection.');
      return;
    }
    setActionLoading(true);
    setError('');

    try {
      await api.rejectApplication(selectedApp.id, rejectReason);
      setSelectedApp(null);
      setRejectReason('');
      loadApps();
    } catch (err: any) {
      setError(err.message || 'Failed to reject application.');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Candidate Internship Applications</h3>
        {loading ? (
          <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                  <th className="pb-3">Candidate</th>
                  <th className="pb-3">College</th>
                  <th className="pb-3">Referring Employee</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Submitted At</th>
                  <th className="pb-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-50">
                {apps.map((app) => (
                  <tr key={app.id} className="text-neutral-700">
                    <td className="py-4">
                      <p className="font-semibold text-neutral-800">{app.name}</p>
                      <p className="text-xs text-neutral-400 mt-0.5">{app.preferred_role || 'No preferred role'}</p>
                    </td>
                    <td className="py-4 font-medium text-neutral-600">{app.college}</td>
                    <td className="py-4 text-xs font-semibold text-neutral-500">{app.referrer_email}</td>
                    <td className="py-4">
                      <span className={`inline-flex px-1.5 py-0.5 rounded text-[10px] font-bold uppercase border ${app.status === 'WAITING_ADMIN' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                        app.status === 'ACTIVATED' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                          app.status === 'COMPLETED' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' :
                            app.status === 'OFFER_SENT' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                              'bg-neutral-100 text-neutral-600 border-neutral-200'
                        }`}>
                        {app.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-4 text-xs text-neutral-400">{new Date(app.created_at).toLocaleDateString()}</td>
                    <td className="py-4 text-right">
                      {app.status === 'WAITING_ADMIN' ? (
                        <button
                          onClick={() => setSelectedApp(app)}
                          className="bg-brand-600 hover:bg-brand-700 text-white font-semibold py-1 px-3 rounded text-xs transition-colors shadow-sm shadow-brand-50"
                        >
                          Review App
                        </button>
                      ) : (
                        <span className="text-xs text-neutral-400 font-semibold">Processed</span>
                      )}
                    </td>
                  </tr>
                ))}
                {apps.length === 0 && (
                  <tr>
                    <td colSpan={6} className="text-center py-6 text-neutral-400 text-xs">No internship applications found.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Review Dialog/Modal */}
      {selectedApp && (
        <div className="fixed inset-0 bg-neutral-900/40 backdrop-blur-[2px] flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white border border-neutral-200 rounded-xl shadow-lg w-full max-w-lg p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-100 mb-6">
              <h3 className="font-bold text-neutral-800 text-base">Review Application: {selectedApp.name}</h3>
              <button onClick={() => setSelectedApp(null)} className="text-neutral-400 hover:text-neutral-600 text-sm font-bold">✕</button>
            </div>

            {error && <div className="mb-4 p-3 bg-red-50 text-red-700 border border-red-100 text-xs rounded-lg">{error}</div>}

            <div className="space-y-4 text-sm text-neutral-600 mb-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Candidate College</p>
                  <p className="font-medium text-neutral-800 mt-0.5">{selectedApp.college}</p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Preferred Role</p>
                  <p className="font-medium text-neutral-800 mt-0.5">{selectedApp.preferred_role}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Internship Duration</p>
                  <p className="font-medium text-neutral-800 mt-0.5">{selectedApp.duration_months} Months</p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Tentative Timeline</p>
                  <p className="font-medium text-neutral-800 mt-0.5">
                    {selectedApp.tentative_start_date} to {selectedApp.tentative_end_date}
                  </p>
                </div>
              </div>

              <div>
                <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider">Submitted Resume</p>
                {selectedApp.resume_path ? (
                  <a
                    href={selectedApp.resume_path}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-brand-600 font-semibold hover:underline mt-1 bg-brand-50/50 py-1 px-2.5 rounded border border-brand-100 text-xs"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    Open Candidate Resume (PDF)
                  </a>
                ) : (
                  <span className="text-xs text-neutral-400">No resume uploaded</span>
                )}
              </div>
            </div>

            <div className="border-t border-neutral-100 pt-6 space-y-6">
              {/* Approve actions */}
              <div>
                <h4 className="text-xs font-bold text-neutral-800 uppercase tracking-wider mb-2">Option A: Approve & Upload Offer Letter</h4>
                <div className="flex gap-2">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setOfferFile(e.target.files ? e.target.files[0] : null)}
                    className="block w-full text-xs text-neutral-500 file:mr-4 file:py-1 file:px-3 file:rounded file:border file:border-brand-200 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100"
                  />
                  <button
                    onClick={handleApprove}
                    disabled={actionLoading || !offerFile}
                    className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold py-1.5 px-4 rounded text-xs shrink-0 transition-colors"
                  >
                    {actionLoading ? 'Approving...' : 'Approve & Send Offer'}
                  </button>
                </div>
              </div>

              {/* Reject actions */}
              <div className="border-t border-neutral-50 pt-4">
                <h4 className="text-xs font-bold text-neutral-800 uppercase tracking-wider mb-2">Option B: Reject Application</h4>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Enter reason for rejection..."
                    value={rejectReason}
                    onChange={(e) => setRejectReason(e.target.value)}
                    className="flex-1 px-3 py-1.5 border border-neutral-200 text-xs rounded outline-none focus:border-red-500"
                  />
                  <button
                    onClick={handleReject}
                    disabled={actionLoading || !rejectReason}
                    className="bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-semibold py-1.5 px-4 rounded text-xs shrink-0 transition-colors"
                  >
                    Reject Candidate
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// --- Admin: Interns Tracker ---
const AdminTracker: React.FC = () => {
  const [interns, setInterns] = useState<Internship[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const allApps = await api.getApplications();
      // Filter only active/activated or completed
      const activeApps = allApps.filter((a) => a.status === 'ACTIVATED' || a.status === 'COMPLETED');
      setInterns(activeApps);

      const allProjs = await api.getAllInternProjects();
      setProjects(allProjs);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleComplete = async (internshipId: number) => {
    setActionLoading(true);
    try {
      await api.completeInternship(internshipId);
      loadData();
    } catch (e: any) {
      alert(e.message || 'Failed to mark completion');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Active & Completed Interns</h3>
      {loading ? (
        <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                <th className="pb-3">Intern Details</th>
                <th className="pb-3">Project Selection</th>
                <th className="pb-3">Progress</th>
                <th className="pb-3">Submissions</th>
                <th className="pb-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-50 text-sm">
              {interns.map((intern) => {
                const proj = projects.find((p) => p.intern_id === intern.intern_id);
                return (
                  <tr key={intern.id} className="text-neutral-700">
                    <td className="py-4">
                      <p className="font-semibold text-neutral-800">{intern.name}</p>
                      <p className="text-[10px] text-neutral-400 mt-0.5">{intern.college} • {intern.preferred_role}</p>
                    </td>
                    <td className="py-4">
                      {proj ? (
                        <div>
                          <p className="font-medium text-xs text-neutral-800">
                            {proj.project_type === 'Company' ? 'Company Project' : 'Own Problem Statement'}
                          </p>
                          <p className="text-[10px] text-neutral-400 max-w-xs truncate mt-0.5">
                            {proj.project_type === 'Company' ? proj.company_project?.title : proj.own_project_title}
                          </p>
                        </div>
                      ) : (
                        <span className="text-xs text-neutral-400">No project selected</span>
                      )}
                    </td>
                    <td className="py-4">
                      {proj ? (
                        <div className="flex items-center gap-2">
                          <div className="w-16 bg-neutral-100 rounded-full h-1.5 overflow-hidden">
                            <div className="bg-brand-500 h-1.5" style={{ width: `${proj.progress_pct}%` }} />
                          </div>
                          <span className="text-xs font-semibold text-neutral-700">{proj.progress_pct}%</span>
                        </div>
                      ) : (
                        <span className="text-xs text-neutral-400">-</span>
                      )}
                    </td>
                    <td className="py-4">
                      <div className="flex flex-col gap-1">
                        {intern.resume_path && (
                          <a href={intern.resume_path} target="_blank" rel="noreferrer" className="text-[10px] text-brand-600 font-semibold hover:underline">
                            Open Resume (PDF)
                          </a>
                        )}
                        {intern.final_ppt_path ? (
                          <a href={intern.final_ppt_path} target="_blank" rel="noreferrer" className="text-[10px] text-emerald-600 font-semibold hover:underline flex items-center gap-0.5">
                            <FileDown className="w-3 h-3 shrink-0" />
                            Download Final PPT
                          </a>
                        ) : (
                          <span className="text-[10px] text-neutral-400">PPT not uploaded</span>
                        )}
                      </div>
                    </td>
                    <td className="py-4 text-right">
                      {intern.status === 'ACTIVATED' ? (
                        <button
                          onClick={() => handleComplete(intern.id)}
                          disabled={actionLoading || !intern.final_ppt_path}
                          className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold py-1 px-3 rounded text-xs transition-colors shadow-sm"
                          title={!intern.final_ppt_path ? 'Candidate must upload final PPT first' : ''}
                        >
                          Complete Internship
                        </button>
                      ) : (
                        <span className="text-xs text-emerald-600 font-bold flex items-center justify-end gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Completed
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
              {interns.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center py-6 text-neutral-400 text-xs">No active or completed interns found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// --- Admin: Company Projects Ideas ---
const AdminProjects: React.FC = () => {
  const [projects, setProjects] = useState<CompanyProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const loadProjects = () => {
    setLoading(true);
    api.getCompanyProjects().then(setProjects).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await api.createCompanyProject(title, desc);
      setTitle('');
      setDesc('');
      loadProjects();
    } catch (err: any) {
      setError(err.message || 'Failed to create project idea.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this project idea?')) return;
    try {
      await api.deleteCompanyProject(id);
      loadProjects();
    } catch (e: any) {
      alert(e.message || 'Failed to delete project');
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in">
      {/* Create project form */}
      <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm h-fit">
        <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">New Project Idea</h3>
        {error && <div className="mb-4 p-3 bg-red-50 text-red-700 border border-red-100 text-xs rounded-lg">{error}</div>}

        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Project Title</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Cloud Automation Framework"
              className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Problem Description</label>
            <textarea
              required
              rows={4}
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="Write a clear statement of the problem, required technology stack, and expectations..."
              className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-semibold py-2 rounded-lg text-sm flex items-center justify-center gap-2 transition-colors disabled:opacity-75"
          >
            {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            Publish Project Idea
          </button>
        </form>
      </div>

      {/* Projects List */}
      <div className="lg:col-span-2 space-y-4">
        {loading ? (
          <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm text-center">
            <RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" />
          </div>
        ) : (
          projects.map((proj) => (
            <div key={proj.id} className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm flex justify-between gap-4">
              <div className="space-y-2">
                <h4 className="font-bold text-neutral-800 text-sm uppercase tracking-wider">{proj.title}</h4>
                <p className="text-xs text-neutral-600 leading-relaxed">{proj.description}</p>
                <p className="text-[10px] text-neutral-400 font-semibold uppercase tracking-wider">
                  Published: {new Date(proj.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => handleDelete(proj.id)}
                className="p-2 hover:bg-red-50 hover:text-red-600 text-neutral-400 rounded-lg h-fit transition-colors"
                title="Delete Project"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
        {!loading && projects.length === 0 && (
          <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm text-center text-neutral-400 text-xs">
            No published company project ideas.
          </div>
        )}
      </div>
    </div>
  );
};

// --- Admin: Attendance Records ---
const AdminAttendance: React.FC = () => {
  const [att, setAtt] = useState<Attendance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAllAttendance().then(setAtt).finally(() => setLoading(false));
  }, []);

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Intern Daily Attendance Calendar</h3>
      {loading ? (
        <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                <th className="pb-3">Date</th>
                <th className="pb-3">Intern ID / User</th>
                <th className="pb-3">Attendance Status</th>
                <th className="pb-3">Marked Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-50 text-xs">
              {att.map((a) => (
                <tr key={a.id} className="text-neutral-700">
                  <td className="py-3 font-semibold text-neutral-800">{a.date}</td>
                  <td className="py-3">Candidate #{a.intern_id}</td>
                  <td className="py-3">
                    <span className={`inline-flex items-center gap-1.5 font-semibold text-xs ${a.status === 'Present' ? 'text-emerald-600' : 'text-red-600'
                      }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${a.status === 'Present' ? 'bg-emerald-500' : 'bg-red-500'}`} />
                      {a.status}
                    </span>
                  </td>
                  <td className="py-3 text-neutral-400">{new Date(a.created_at).toLocaleString()}</td>
                </tr>
              ))}
              {att.length === 0 && (
                <tr>
                  <td colSpan={4} className="text-center py-6 text-neutral-400">No attendance records found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// --- Employee: Pending Referrals ---
const EmployeeReferrals: React.FC = () => {
  const [refs, setRefs] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const loadRefs = () => {
    setLoading(true);
    api.getReferredInterns().then((data) => {
      // Show only pending referrals
      setRefs(data.filter((r) => r.status === 'WAITING_EMPLOYEE'));
    }).finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRefs();
  }, []);

  const handleAction = async (id: number, response: 'ACCEPT' | 'REJECT') => {
    if (!confirm(`Are you sure you want to ${response.toLowerCase()} this referral?`)) return;
    setActionLoading(true);
    try {
      await api.respondToReferral(id, response);
      loadRefs();
    } catch (e: any) {
      alert(e.message || 'Failed to update referral response');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Referral Requests for Review</h3>
      {loading ? (
        <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                <th className="pb-3">Candidate</th>
                <th className="pb-3">College</th>
                <th className="pb-3">Resume Upload</th>
                <th className="pb-3">Requested At</th>
                <th className="pb-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-50 text-sm">
              {refs.map((r) => (
                <tr key={r.id} className="text-neutral-700">
                  <td className="py-4 font-semibold text-neutral-800">{r.name}</td>
                  <td className="py-4 font-medium text-neutral-600">{r.college}</td>
                  <td className="py-4">
                    {r.resume_path ? (
                      <a href={r.resume_path} target="_blank" rel="noreferrer" className="text-xs text-brand-600 font-semibold hover:underline">
                        Open Resume (PDF)
                      </a>
                    ) : (
                      <span className="text-xs text-neutral-400">None</span>
                    )}
                  </td>
                  <td className="py-4 text-xs text-neutral-400">{new Date(r.created_at).toLocaleDateString()}</td>
                  <td className="py-4 text-right space-x-2">
                    <button
                      onClick={() => handleAction(r.id, 'REJECT')}
                      disabled={actionLoading}
                      className="border border-red-200 hover:bg-red-50 text-red-600 font-semibold py-1 px-3 rounded text-xs transition-colors"
                    >
                      Reject
                    </button>
                    <button
                      onClick={() => handleAction(r.id, 'ACCEPT')}
                      disabled={actionLoading}
                      className="bg-brand-600 hover:bg-brand-700 text-white font-semibold py-1 px-3 rounded text-xs transition-colors shadow-sm"
                    >
                      Accept Referral
                    </button>
                  </td>
                </tr>
              ))}
              {refs.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center py-6 text-neutral-400 text-xs">No pending referral requests found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// --- Employee: Referred Interns ---
const EmployeeReferredList: React.FC = () => {
  const [refs, setRefs] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getReferredInterns().then(setRefs).finally(() => setLoading(false));
  }, []);

  return (
    <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm animate-fade-in">
      <h3 className="text-sm font-bold text-neutral-800 mb-6 uppercase tracking-wider">Referral Tracking Dashboard</h3>
      {loading ? (
        <div className="text-center py-6"><RefreshCw className="w-5 h-5 animate-spin mx-auto text-neutral-400" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-neutral-100 text-[10px] font-bold text-neutral-400 uppercase tracking-wider">
                <th className="pb-3">Candidate</th>
                <th className="pb-3">College</th>
                <th className="pb-3">Referral Status</th>
                <th className="pb-3">Internship Role</th>
                <th className="pb-3">Timeline</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-50 text-sm">
              {refs.map((r) => (
                <tr key={r.id} className="text-neutral-700">
                  <td className="py-3 font-semibold text-neutral-800">{r.name}</td>
                  <td className="py-3 font-medium text-neutral-600">{r.college}</td>
                  <td className="py-3">
                    <span className={`inline-flex px-1.5 py-0.5 rounded text-[10px] font-bold uppercase border ${r.status === 'REFERRAL_ACCEPTED' || r.status === 'ACTIVATED' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                      r.status === 'REFERRAL_REJECTED' || r.status === 'ADMIN_REJECTED' ? 'bg-red-50 text-red-700 border-red-100' :
                        r.status === 'WAITING_EMPLOYEE' ? 'bg-amber-50 text-amber-700 border-amber-100' :
                          'bg-indigo-50 text-indigo-700 border-indigo-100'
                      }`}>
                      {r.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-3 text-neutral-500 font-semibold">{r.preferred_role || '-'}</td>
                  <td className="py-3 text-xs text-neutral-400">
                    {r.tentative_start_date ? `${r.tentative_start_date} to ${r.tentative_end_date}` : 'Not scheduled'}
                  </td>
                </tr>
              ))}
              {refs.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center py-6 text-neutral-400 text-xs">You have not referred any candidates yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// --- Intern: Journey Portal ---
const InternPortal: React.FC = () => {
  const [internship, setInternship] = useState<Internship | null>(null);
  const [project, setProject] = useState<Project | null>(null);
  const [companyProjects, setCompanyProjects] = useState<CompanyProject[]>([]);
  const [attendance, setAttendance] = useState<Attendance[]>([]);

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState('');

  // Complete profile form state
  const [name, setName] = useState('');
  const [college, setCollege] = useState('');
  const [duration, setDuration] = useState(3);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [role, setRole] = useState('Data Engineer');
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  // Project Selection Form State
  const [projType, setProjType] = useState<'Company' | 'Own'>('Company');
  const [selectedCompProjId, setSelectedCompProjId] = useState<number>(0);
  const [ownTitle, setOwnTitle] = useState('');
  const [ownDesc, setOwnDesc] = useState('');

  // Project update state
  const [progressPct, setProgressPct] = useState(0);
  const [projectStatus, setProjectStatus] = useState('In Progress');
  const [notes, setNotes] = useState('');

  const loadInternData = async () => {
    setLoading(true);
    try {
      const details = await api.getInternshipDetails();
      setInternship(details);

      setName(details.name);
      setCollege(details.college);
      setDuration(details.duration_months || 3);
      setStartDate(details.tentative_start_date || '');
      setEndDate(details.tentative_end_date || '');
      setRole(details.preferred_role || 'Data Engineer');

      if (details.status === 'ACTIVATED' || details.status === 'COMPLETED') {
        const myProj = await api.getMyProject();
        setProject(myProj);
        if (myProj) {
          setProgressPct(myProj.progress_pct);
          setProjectStatus(myProj.status);
          setNotes(myProj.notes || '');
        }

        const compProjs = await api.getCompanyProjects();
        setCompanyProjects(compProjs);
        if (compProjs.length > 0) setSelectedCompProjId(compProjs[0].id);

        const myAtt = await api.getMyAttendance();
        setAttendance(myAtt);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInternData();
  }, []);

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);
    setError('');

    try {
      const form = new FormData();
      form.append('name', name);
      form.append('college', college);
      form.append('duration_months', String(duration));
      form.append('tentative_start_date', startDate);
      form.append('tentative_end_date', endDate);
      form.append('preferred_role', role);
      if (resumeFile) {
        form.append('resume', resumeFile);
      }

      await api.updateInternProfile(form);
      loadInternData();
    } catch (err: any) {
      setError(err.message || 'Failed to submit profile.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleOfferResponse = async (resp: 'ACCEPT' | 'DECLINE') => {
    if (!confirm(`Are you sure you want to ${resp.toLowerCase()} the internship offer?`)) return;
    setActionLoading(true);
    try {
      await api.respondToOffer(resp);
      loadInternData();
    } catch (err: any) {
      alert(err.message || 'Failed to respond to offer');
    } finally {
      setActionLoading(false);
    }
  };

  const handleMarkAttendance = async (status: 'Present' | 'Absent') => {
    setActionLoading(true);
    try {
      await api.markAttendance(status);
      loadInternData();
    } catch (err: any) {
      alert(err.message || 'Failed to mark attendance');
    } finally {
      setActionLoading(false);
    }
  };

  const handleProjectSelect = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);

    try {
      const form = new FormData();
      form.append('project_type', projType);
      if (projType === 'Company') {
        form.append('company_project_id', String(selectedCompProjId));
      } else {
        form.append('own_project_title', ownTitle);
        form.append('own_project_description', ownDesc);
      }

      await api.selectProject(form);
      loadInternData();
    } catch (err: any) {
      alert(err.message || 'Failed to select project');
    } finally {
      setActionLoading(false);
    }
  };

  const handleProjectUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);

    try {
      await api.updateProjectProgress(progressPct, projectStatus, notes);
      alert('Project progress updated successfully!');
      loadInternData();
    } catch (err: any) {
      alert(err.message || 'Failed to update progress');
    } finally {
      setActionLoading(false);
    }
  };

  const handlePPTUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.toLowerCase().endsWith('.pptx') && !file.name.toLowerCase().endsWith('.ppt')) {
        alert('Only PowerPoint presentations (.ppt, .pptx) are allowed.');
        return;
      }
      setActionLoading(true);
      try {
        await api.uploadFinalPPT(file);
        alert('Presentation uploaded successfully! Admin has been notified for review.');
        loadInternData();
      } catch (err: any) {
        alert(err.message || 'Failed to upload presentation');
      } finally {
        setActionLoading(false);
      }
    }
  };

  if (loading) return <div className="text-center py-12"><RefreshCw className="w-6 h-6 animate-spin mx-auto text-neutral-400" /></div>;
  if (!internship) return <div className="text-red-500">Failed to load intern details.</div>;

  // --- RENDERING ACCORDING TO APPLICATIONS STATES ---

  // 1. Waiting for employee referral approval
  if (internship.status === 'WAITING_EMPLOYEE') {
    return (
      <div className="bg-white border border-neutral-200 rounded-xl p-8 max-w-lg mx-auto text-center shadow-sm animate-fade-in">
        <Clock className="w-16 h-16 text-amber-500 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-neutral-900">Waiting for Employee Referral</h3>
        <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
          Your application has been received and is currently waiting for approval from the referring employee:{' '}
          <strong className="text-neutral-800">{internship.referrer_email}</strong>.
        </p>
        <p className="text-neutral-400 text-xs mt-3">Once accepted, you will be able to complete your profile.</p>
      </div>
    );
  }

  // 2. Referral Rejected
  if (internship.status === 'REFERRAL_REJECTED') {
    return (
      <div className="bg-white border border-neutral-200 rounded-xl p-8 max-w-lg mx-auto text-center shadow-sm animate-fade-in">
        <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-neutral-900">Referral Request Rejected</h3>
        <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
          We regret to inform you that your referral request was declined by the employee ({internship.referrer_email}).
          Your application has been closed.
        </p>
      </div>
    );
  }

  // 3. Referral Accepted: Complete Profile Form
  if (internship.status === 'REFERRAL_ACCEPTED' || internship.status === 'WAITING_ADMIN') {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in">
        <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm h-fit">
          <h3 className="text-sm font-bold text-neutral-800 mb-4 uppercase tracking-wider">Status Timeline</h3>
          <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-neutral-100">
            <TimelineStep done label="Referral Application Submitted" />
            <TimelineStep done label="Referral Approved by Employee" />
            <TimelineStep active={internship.status === 'REFERRAL_ACCEPTED'} label="Submit Internship Profile" desc="Fill details below" />
            <TimelineStep active={internship.status === 'WAITING_ADMIN'} label="HR Admin Review" desc="Profile is submitted for HR verification" />
            <TimelineStep label="Receive Internship Offer Letter" />
          </div>
        </div>

        <div className="lg:col-span-2 bg-white border border-neutral-200 rounded-xl p-6 shadow-sm">
          <div className="flex justify-between items-center pb-4 border-b border-neutral-100 mb-6">
            <h3 className="text-sm font-bold text-neutral-800 uppercase tracking-wider">Complete Internship Profile</h3>
            {internship.status === 'WAITING_ADMIN' && (
              <span className="bg-amber-50 text-amber-700 px-2 py-0.5 rounded text-[10px] font-bold border border-amber-200 uppercase">
                Waiting for Review
              </span>
            )}
          </div>

          {error && <div className="mb-4 p-3 bg-red-50 text-red-700 border border-red-100 text-xs rounded-lg">{error}</div>}

          <form onSubmit={handleProfileSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Candidate Name</label>
                <input
                  type="text"
                  required
                  disabled={internship.status === 'WAITING_ADMIN'}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 disabled:bg-neutral-50"
                />
              </div>

              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">College / Institution</label>
                <input
                  type="text"
                  required
                  disabled={internship.status === 'WAITING_ADMIN'}
                  value={college}
                  onChange={(e) => setCollege(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 disabled:bg-neutral-50"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Duration (Months)</label>
                <input
                  type="number"
                  required
                  disabled={internship.status === 'WAITING_ADMIN'}
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 disabled:bg-neutral-50"
                />
              </div>

              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Tentative Start Date</label>
                <input
                  type="date"
                  required
                  disabled={internship.status === 'WAITING_ADMIN'}
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 disabled:bg-neutral-50"
                />
              </div>

              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Tentative End Date</label>
                <input
                  type="date"
                  required
                  disabled={internship.status === 'WAITING_ADMIN'}
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 disabled:bg-neutral-50"
                />
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Preferred Technical Role</label>
              <select
                value={role}
                disabled={internship.status === 'WAITING_ADMIN'}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none bg-white focus:border-brand-500 disabled:bg-neutral-50"
              >
                <option value="Data Engineer">Data Engineer</option>
                <option value="Cloud Architect">Cloud Architect</option>
                <option value="Fullstack Web Developer">Fullstack Web Developer</option>
                <option value="AI / NLP Intern">AI / NLP Intern</option>
              </select>
            </div>

            {internship.status === 'REFERRAL_ACCEPTED' && (
              <div>
                <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Update Resume PDF (Optional)</label>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setResumeFile(e.target.files ? e.target.files[0] : null)}
                  className="block w-full text-xs text-neutral-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border file:border-neutral-200 file:text-xs file:font-semibold file:bg-neutral-50 file:text-neutral-700 hover:file:bg-neutral-100 cursor-pointer"
                />
              </div>
            )}

            {internship.status === 'REFERRAL_ACCEPTED' && (
              <button
                type="submit"
                disabled={actionLoading}
                className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2 rounded-lg text-sm transition-colors flex items-center justify-center gap-2"
              >
                {actionLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                Submit Profile for Review
              </button>
            )}
          </form>
        </div>
      </div>
    );
  }

  // 4. Admin Rejected
  if (internship.status === 'ADMIN_REJECTED') {
    return (
      <div className="bg-white border border-neutral-200 rounded-xl p-8 max-w-lg mx-auto text-center shadow-sm animate-fade-in">
        <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-neutral-900">Application Rejected</h3>
        <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
          We regret to inform you that your internship profile was not approved by the HR Admin team.
        </p>
      </div>
    );
  }

  // 5. Offer Sent: Review & Respond to Offer Letter
  if (internship.status === 'OFFER_SENT') {
    return (
      <div className="bg-white border border-neutral-200 rounded-xl p-8 max-w-lg mx-auto text-center shadow-sm animate-fade-in">
        <Award className="w-16 h-16 text-brand-500 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-neutral-900">Internship Offer Letter Received!</h3>
        <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
          Congratulations! Agilisium has issued an official internship offer letter for you. Please download and review the offer below.
        </p>

        {internship.offer_letter_path && (
          <div className="my-6">
            <a
              href={internship.offer_letter_path}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold border border-brand-200 rounded-lg py-2.5 px-6 text-sm transition-colors shadow-sm"
            >
              <FileDown className="w-4 h-4" />
              Download Official Offer Letter (PDF)
            </a>
          </div>
        )}

        <div className="flex gap-4 justify-center border-t border-neutral-100 pt-6">
          <button
            onClick={() => handleOfferResponse('DECLINE')}
            disabled={actionLoading}
            className="border border-red-200 hover:bg-red-50 text-red-600 font-semibold py-2 px-6 rounded-lg text-sm transition-colors disabled:opacity-50"
          >
            Decline Offer
          </button>
          <button
            onClick={() => handleOfferResponse('ACCEPT')}
            disabled={actionLoading}
            className="bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-semibold py-2 px-6 rounded-lg text-sm transition-colors disabled:opacity-50 shadow-sm"
          >
            Accept Offer & Activate
          </button>
        </div>
      </div>
    );
  }

  // 6. Offer Declined
  if (internship.status === 'OFFER_DECLINED') {
    return (
      <div className="bg-white border border-neutral-200 rounded-xl p-8 max-w-lg mx-auto text-center shadow-sm animate-fade-in">
        <XCircle className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-neutral-900">Offer Declined</h3>
        <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
          You declined the internship offer. If this was a mistake, please reach out to HR admins.
        </p>
      </div>
    );
  }

  // 7. Active Internship Portal: Attendance + Project Selection + Deliverables
  if (internship.status === 'ACTIVATED' || internship.status === 'COMPLETED') {
    return (
      <div className="space-y-8 animate-fade-in">

        {/* Banner */}
        <div className="bg-brand-700 text-white rounded-xl p-6 shadow-md flex justify-between items-center gap-4">
          <div>
            <h3 className="text-lg font-bold">Welcome to Agilisium, {internship.name}!</h3>
            <p className="text-xs text-brand-100 mt-1">Your internship is fully activated. Role: {internship.preferred_role}</p>
          </div>
          <span className="bg-emerald-500/20 text-emerald-100 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-bold shrink-0">
            {internship.status === 'COMPLETED' ? 'Completed' : 'Active'}
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          {/* Daily Attendance panel */}
          <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <h4 className="text-xs font-bold text-neutral-800 uppercase tracking-wider mb-4">Mark Attendance</h4>
              <p className="text-xs text-neutral-500 mb-6">Mark your daily presence or absence on the system calendar.</p>

              <div className="flex gap-4">
                <button
                  onClick={() => handleMarkAttendance('Absent')}
                  disabled={actionLoading || internship.status === 'COMPLETED'}
                  className="flex-1 border border-neutral-200 hover:bg-red-50 hover:border-red-200 hover:text-red-600 font-semibold py-2 rounded-lg text-sm transition-colors text-neutral-600 disabled:opacity-50"
                >
                  Absent
                </button>
                <button
                  onClick={() => handleMarkAttendance('Present')}
                  disabled={actionLoading || internship.status === 'COMPLETED'}
                  className="flex-1 bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-semibold py-2 rounded-lg text-sm transition-colors disabled:opacity-50 shadow-sm"
                >
                  Present
                </button>
              </div>
            </div>

            <div className="border-t border-neutral-100 pt-6 mt-6">
              <h5 className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider mb-3">Recent Logs</h5>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {attendance.slice(0, 5).map((att) => (
                  <div key={att.id} className="flex justify-between items-center text-xs border border-neutral-50 bg-neutral-50/50 p-2 rounded">
                    <span className="font-medium text-neutral-600">{att.date}</span>
                    <span className={`font-bold uppercase text-[9px] px-1.5 py-0.5 rounded ${att.status === 'Present' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' : 'bg-red-50 text-red-700 border border-red-100'
                      }`}>
                      {att.status}
                    </span>
                  </div>
                ))}
                {attendance.length === 0 && (
                  <p className="text-[10px] text-neutral-400">No attendance marked yet.</p>
                )}
              </div>
            </div>
          </div>

          {/* Project Selection / Tracking panel */}
          <div className="lg:col-span-2 bg-white border border-neutral-200 rounded-xl p-6 shadow-sm">
            <h4 className="text-xs font-bold text-neutral-800 uppercase tracking-wider mb-4">Internship Project Tracking</h4> 

            {/* If no project selected yet */}
            {!project ? (
              <form onSubmit={handleProjectSelect} className="space-y-4">
                <div className="flex gap-4 border-b border-neutral-100 pb-3">
                  <label className="flex items-center gap-2 text-xs font-semibold cursor-pointer">
                    <input
                      type="radio"
                      checked={projType === 'Company'}
                      onChange={() => setProjType('Company')}
                      className="text-brand-600 focus:ring-brand-500"
                    />
                    Select Company Project
                  </label>
                  <label className="flex items-center gap-2 text-xs font-semibold cursor-pointer">
                    <input
                      type="radio"
                      checked={projType === 'Own'}
                      onChange={() => setProjType('Own')}
                      className="text-brand-600 focus:ring-brand-500"
                    />
                    Submit Own Problem Statement
                  </label>
                </div>

                {projType === 'Company' ? (
                  <div>
                    <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Available Company Projects</label>
                    <select
                      value={selectedCompProjId}
                      onChange={(e) => setSelectedCompProjId(Number(e.target.value))}
                      className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none bg-white focus:border-brand-500"
                    >
                      {companyProjects.map((p) => (
                        <option key={p.id} value={p.id}>{p.title}</option>
                      ))}
                      {companyProjects.length === 0 && <option value={0}>No projects published</option>}
                    </select>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Project Title</label>
                      <input
                        type="text"
                        required
                        value={ownTitle}
                        onChange={(e) => setOwnTitle(e.target.value)}
                        placeholder="e.g. Automated Log Ingestor"
                        className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500"
                      />
                    </div>
                    <div>
                      <label className="block text-[10px] font-semibold text-neutral-500 mb-1 uppercase tracking-wider">Problem Statement / Details</label>
                      <textarea
                        required
                        rows={3}
                        value={ownDesc}
                        onChange={(e) => setOwnDesc(e.target.value)}
                        placeholder="Explain the workflow, tech stack, and goals of this project..."
                        className="w-full px-3 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 resize-none"
                      />
                    </div>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={actionLoading}
                  className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2 rounded-lg text-sm transition-colors shadow-sm"
                >
                  Activate Selected Project
                </button>
              </form>
            ) : (
              /* If project is selected, show Tracking & Status */
              <form onSubmit={handleProjectUpdate} className="space-y-6">
                <div className="bg-neutral-50/50 border border-neutral-100 rounded-lg p-4">
                  <span className="text-[9px] font-bold tracking-wide uppercase px-1.5 py-0.5 rounded bg-brand-100 text-brand-700 border border-brand-200">
                    {project.project_type === 'Company' ? 'Company Selected' : 'Custom Project'}
                  </span>
                  <h5 className="font-bold text-neutral-800 text-sm uppercase tracking-wider mt-2.5">
                    {project.project_type === 'Company' ? project.company_project?.title : project.own_project_title}
                  </h5>
                  <p className="text-xs text-neutral-500 mt-1 leading-relaxed">
                    {project.project_type === 'Company' ? project.company_project?.description : project.own_project_description}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-semibold text-neutral-500 mb-1.5 uppercase tracking-wider">Project Progress: {progressPct}%</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      disabled={internship.status === 'COMPLETED'}
                      value={progressPct}
                      onChange={(e) => setProgressPct(Number(e.target.value))}
                      className="w-full h-1.5 bg-neutral-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
                    />
                  </div>

                  <div>
                    <label className="block text-[10px] font-semibold text-neutral-500 mb-1.5 uppercase tracking-wider">Task Status</label>
                    <select
                      value={projectStatus}
                      disabled={internship.status === 'COMPLETED'}
                      onChange={(e) => setProjectStatus(e.target.value)}
                      className="w-full px-3 py-1.5 text-xs border border-neutral-200 rounded-lg outline-none bg-white focus:border-brand-500"
                    >
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-semibold text-neutral-500 mb-1.5 uppercase tracking-wider">Progress Update Notes</label>
                  <textarea
                    rows={3}
                    disabled={internship.status === 'COMPLETED'}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Describe tasks finished, roadblocks, or help required..."
                    className="w-full px-3 py-2 text-xs border border-neutral-200 rounded-lg outline-none focus:border-brand-500 resize-none disabled:bg-neutral-50"
                  />
                </div>

                {internship.status === 'ACTIVATED' && (
                  <button
                    type="submit"
                    disabled={actionLoading}
                    className="bg-brand-600 hover:bg-brand-700 text-white font-semibold py-1.5 px-6 rounded-lg text-xs transition-colors shadow-sm"
                  >
                    Save Progress Updates
                  </button>
                )}
              </form>
            )}
          </div>
        </div>

        {/* Deliverables Panel */}
        {project && (
          <div className="bg-white border border-neutral-200 rounded-xl p-6 shadow-sm grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div>
              <h4 className="text-xs font-bold text-neutral-800 uppercase tracking-wider mb-2">Final Deliverable: Presentation Slide</h4>
              <p className="text-xs text-neutral-500 leading-relaxed mb-4">
                To complete your internship, download the official presentation template slide, populate it with your project results, and upload it back here for HR and manager review.
              </p>

              <a
                href="/api/v1/download/template"
                download
                className="inline-flex items-center gap-1.5 border border-brand-200 hover:bg-brand-50 text-brand-700 text-xs font-bold py-2 px-4 rounded-lg transition-colors"
              >
                <FileDown className="w-3.5 h-3.5" />
                Download Template (PPTX)
              </a>
            </div>

            <div className="border-t md:border-t-0 md:border-l border-neutral-100 pt-6 md:pt-0 md:pl-6">
              <h5 className="text-[10px] font-bold text-neutral-400 uppercase tracking-wider mb-3">Upload Completed Presentation</h5>

              {internship.final_ppt_path ? (
                <div className="bg-emerald-50/50 border border-emerald-100 rounded-lg p-4 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-2 text-emerald-700">
                    <CheckCircle2 className="w-5 h-5 shrink-0" />
                    <div>
                      <p className="text-xs font-bold">Presentation Uploaded!</p>
                      <a href={internship.final_ppt_path} target="_blank" rel="noreferrer" className="text-[10px] underline text-emerald-600 font-semibold block mt-0.5">
                        Download Uploaded File
                      </a>
                    </div>
                  </div>
                  {internship.status === 'ACTIVATED' && (
                    <label className="bg-white hover:bg-neutral-50 border border-neutral-200 text-neutral-700 font-semibold py-1.5 px-3 rounded text-[10px] transition-colors cursor-pointer shrink-0">
                      Change File
                      <input type="file" accept=".ppt,.pptx" onChange={handlePPTUpload} className="hidden" />
                    </label>
                  )}
                </div>
              ) : (
                <label className="flex flex-col items-center justify-center border border-dashed border-neutral-200 rounded-lg py-6 bg-neutral-50/50 hover:bg-neutral-50 transition-colors cursor-pointer">
                  <Upload className="w-6 h-6 text-neutral-400 mb-1.5" />
                  <span className="text-[10px] text-neutral-600 font-semibold">Select and upload completed PPT/PPTX slide</span>
                  <input type="file" accept=".ppt,.pptx" onChange={handlePPTUpload} className="hidden" />
                </label>
              )}
              {internship.status === 'COMPLETED' && (
                <p className="text-[10px] text-emerald-600 font-semibold mt-2">Internship completed. Upload locked.</p>
              )}
            </div>
          </div>
        )}
      </div>
    );
  }

  return null;
};

// --- Timeline Step helper for Intern Portal ---
const TimelineStep: React.FC<{ done?: boolean; active?: boolean; label: string; desc?: string }> = ({ done, active, label, desc }) => {
  return (
    <div className="relative pl-6">
      <span className={`absolute left-0 top-1 w-4.5 h-4.5 -translate-x-1/2 rounded-full border-2 flex items-center justify-center ${done ? 'bg-brand-600 border-brand-600 text-white' :
        active ? 'bg-white border-brand-500 text-brand-600' :
          'bg-white border-neutral-200'
        }`}>
        {done && <span className="text-[8px] font-bold">✓</span>}
        {active && <span className="w-1.5 h-1.5 rounded-full bg-brand-500" />}
      </span>
      <div>
        <p className={`text-xs font-semibold ${active ? 'text-brand-700' : done ? 'text-neutral-800' : 'text-neutral-400'}`}>
          {label}
        </p>
        {desc && <p className="text-[10px] text-neutral-400 mt-0.5">{desc}</p>}
      </div>
    </div>
  );
};
