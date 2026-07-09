import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Lock, Mail, Loader2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      await api.login(formData);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 px-4">
      <div className="w-full max-w-md bg-white rounded-xl border border-neutral-200 shadow-sm p-8 animate-fade-in">
        {/* Branding header */}
        <div className="flex flex-col items-center mb-8">
          <img src="/favicon.ico" alt="AIRP Logo" className="w-12 h-12 mb-3" />
          <h2 className="text-xl font-bold text-neutral-900 tracking-tight">Agilisium AIRP</h2>
          <p className="text-neutral-500 text-xs mt-1">Intern & Referral Portal</p>
        </div>

        {error && (
          <div className="mb-6 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg flex items-start gap-2">
            <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
              Official Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@agilisium.com"
                className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white py-2 px-4 rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-colors disabled:opacity-70 disabled:cursor-not-allowed shadow-sm shadow-brand-100"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Signing in...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-neutral-100 text-center">
          <p className="text-xs text-neutral-500">
            Are you an intern candidate?{' '}
            <Link to="/apply" className="text-brand-600 font-semibold hover:underline">
              Apply for Internship
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
