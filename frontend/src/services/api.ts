const API_BASE = '/api/v1';

export interface User {
  id: number;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Internship {
  id: number;
  intern_id: number;
  name: string;
  college: string;
  duration_months: number | null;
  tentative_start_date: string | null;
  tentative_end_date: string | null;
  preferred_role: string | null;
  resume_path: string | null;
  referrer_email: string;
  referrer_id: number | null;
  status: string;
  offer_letter_path: string | null;
  final_ppt_path: string | null;
  created_at: string;
  updated_at: string;
}

export interface Attendance {
  id: number;
  intern_id: number;
  date: string;
  status: string;
  created_at: string;
}

export interface CompanyProject {
  id: number;
  title: string;
  description: string;
  created_at: string;
}

export interface Project {
  id: number;
  intern_id: number;
  project_type: string;
  company_project_id: number | null;
  own_project_title: string | null;
  own_project_description: string | null;
  status: string;
  progress_pct: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
  company_project?: CompanyProject;
}

export interface SMTPConfig {
  host: string;
  port: number;
  user: string;
  password?: string;
  from_email: string;
}

export interface AuditLog {
  id: number;
  user_id: number | null;
  action: string;
  details: string | null;
  created_at: string;
  user_email: string | null;
}

export interface Analytics {
  total_applications: number;
  pending_referrals: number;
  active_interns: number;
  completed_internships: number;
  by_status: Record<string, number>;
}

// Token helpers
export const getToken = () => localStorage.getItem('airp_token');
export const setToken = (token: string) => localStorage.setItem('airp_token', token);
export const clearToken = () => {
  localStorage.removeItem('airp_token');
  localStorage.removeItem('airp_role');
  localStorage.removeItem('airp_email');
};
export const getRole = () => localStorage.getItem('airp_role');
export const setRole = (role: string) => localStorage.setItem('airp_role', role);
export const getEmail = () => localStorage.getItem('airp_email');
export const setEmail = (email: string) => localStorage.setItem('airp_email', email);

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers || {});
  
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearToken();
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(errorData.detail || 'An error occurred');
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const api = {
  // Auth
  login: async (form: FormData): Promise<{ access_token: string; token_type: string; role: string; email: string }> => {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      body: form, // oauth2 login uses URLencoded form-data or standard form-data
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Failed to login' }));
      throw new Error(err.detail || 'Incorrect email or password');
    }
    const data = await response.json();
    setToken(data.access_token);
    setRole(data.role);
    setEmail(data.email);
    return data;
  },

  getCurrentUser: (): Promise<User> => request<User>('/auth/me'),

  // Public Apply
  apply: async (formData: FormData): Promise<Internship> => {
    const response = await fetch(`${API_BASE}/intern/apply`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Failed to submit application' }));
      throw new Error(err.detail || 'Submission failed');
    }
    return response.json();
  },

  // Intern endpoints
  getInternshipDetails: (): Promise<Internship> => request<Internship>('/intern/details'),
  
  updateInternProfile: async (formData: FormData): Promise<Internship> => {
    const response = await fetch(`${API_BASE}/intern/profile`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${getToken()}`
      },
      body: formData
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Failed to update profile' }));
      throw new Error(err.detail || 'Update failed');
    }
    return response.json();
  },

  respondToOffer: async (response: 'ACCEPT' | 'DECLINE'): Promise<Internship> => {
    const body = new FormData();
    body.append('response', response);
    return request<Internship>('/intern/offer/respond', {
      method: 'POST',
      body,
    });
  },

  markAttendance: async (status: 'Present' | 'Absent', dateStr?: string): Promise<Attendance> => {
    const body = new FormData();
    body.append('status', status);
    if (dateStr) body.append('date_str', dateStr);
    return request<Attendance>('/intern/attendance', {
      method: 'POST',
      body,
    });
  },

  getMyAttendance: (): Promise<Attendance[]> => request<Attendance[]>('/intern/attendance'),

  selectProject: async (formData: FormData): Promise<Project> => {
    return request<Project>('/intern/project', {
      method: 'POST',
      body: formData,
    });
  },

  getMyProject: (): Promise<Project | null> => request<Project | null>('/intern/project'),

  updateProjectProgress: async (progressPct: number, status: string, notes: string): Promise<Project> => {
    const body = new FormData();
    body.append('progress_pct', String(progressPct));
    body.append('status', status);
    body.append('notes', notes);
    return request<Project>('/intern/project', {
      method: 'PUT',
      body,
    });
  },

  uploadFinalPPT: async (file: File): Promise<Internship> => {
    const formData = new FormData();
    formData.append('ppt', file);
    const response = await fetch(`${API_BASE}/intern/complete`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`
      },
      body: formData
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Failed to upload presentation' }));
      throw new Error(err.detail || 'Upload failed');
    }
    return response.json();
  },

  // Employee endpoints
  getReferredInterns: (): Promise<Internship[]> => request<Internship[]>('/employee/referrals'),
  
  respondToReferral: async (internshipId: number, response: 'ACCEPT' | 'REJECT'): Promise<Internship> => {
    const body = new FormData();
    body.append('response', response);
    return request<Internship>(`/employee/referrals/${internshipId}/respond`, {
      method: 'POST',
      body,
    });
  },

  // Admin endpoints
  getApplications: (): Promise<Internship[]> => request<Internship[]>('/admin/applications'),
  
  approveApplication: async (id: number, offerLetter: File): Promise<Internship> => {
    const formData = new FormData();
    formData.append('offer_letter', offerLetter);
    const response = await fetch(`${API_BASE}/admin/applications/${id}/approve`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`
      },
      body: formData
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Failed to approve' }));
      throw new Error(err.detail || 'Approval failed');
    }
    return response.json();
  },

  rejectApplication: async (id: number, reason: string): Promise<Internship> => {
    const body = new FormData();
    body.append('reason', reason);
    return request<Internship>(`/admin/applications/${id}/reject`, {
      method: 'POST',
      body,
    });
  },

  getCompanyProjects: (): Promise<CompanyProject[]> => request<CompanyProject[]>('/admin/company-projects'),
  
  createCompanyProject: (title: string, description: string): Promise<CompanyProject> => {
    return request<CompanyProject>('/admin/company-projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
  },

  deleteCompanyProject: (id: number): Promise<void> => {
    return request<void>(`/admin/company-projects/${id}`, {
      method: 'DELETE',
    });
  },

  getAllInternProjects: (): Promise<Project[]> => request<Project[]>('/admin/intern-projects'),
  
  getAllAttendance: (): Promise<Attendance[]> => request<Attendance[]>('/admin/attendance'),
  
  completeInternship: (id: number): Promise<Internship> => {
    return request<Internship>(`/admin/internships/${id}/complete`, {
      method: 'POST',
    });
  },

  // Super Admin endpoints
  createAccount: (email: string, role: string, is_active: boolean): Promise<User> => {
    // Generate a default password for created accounts
    const password = role === 'Admin' ? 'Admin@123' : 'Employee@123';
    return request<User>('/super-admin/accounts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, role, is_active, password }),
    });
  },

  getAccounts: (): Promise<User[]> => request<User[]>('/super-admin/accounts'),
  
  getAnalytics: (): Promise<Analytics> => request<Analytics>('/super-admin/analytics'),
  
  getAuditLogs: (): Promise<AuditLog[]> => request<AuditLog[]>('/super-admin/audit-logs'),
  
  getSMTPConfig: (): Promise<SMTPConfig> => request<SMTPConfig>('/super-admin/smtp'),
  
  updateSMTPConfig: (config: SMTPConfig): Promise<void> => {
    return request<void>('/super-admin/smtp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
  }
};
