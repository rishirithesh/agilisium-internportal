import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { User, Mail, GraduationCap, FileText, ArrowRight, Loader2, CheckCircle2, Lock, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export const Apply: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [college, setCollege] = useState('');
  const [referrerEmail, setReferrerEmail] = useState('');
  const [resume, setResume] = useState<File | null>(null);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.type !== 'application/pdf') {
        setError('Only PDF resumes are allowed.');
        setResume(null);
      } else if (file.size > 5 * 1024 * 1024) {
        setError('File size must be under 5MB.');
        setResume(null);
      } else {
        setError('');
        setResume(file);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resume) {
      setError('Please upload your PDF resume.');
      return;
    }

    // Verify referrer email is @agilisium.com
    if (!referrerEmail.toLowerCase().endsWith('@agilisium.com')) {
      setError('Referring employee email must end with @agilisium.com');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('name', name);
      formData.append('email', email);
      formData.append('password', password);
      formData.append('college', college);
      formData.append('referrer_email', referrerEmail);
      formData.append('resume', resume);

      await api.apply(formData);
      setSuccess(true);
    } catch (err: any) {
      setError(err.message || 'Submission failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50 px-4">
        <div className="w-full max-w-md bg-white rounded-xl border border-neutral-200 shadow-sm p-8 text-center animate-fade-in">
          <div className="flex justify-center mb-4 text-emerald-500">
            <CheckCircle2 className="w-16 h-16" />
          </div>
          <h2 className="text-2xl font-bold text-neutral-900 tracking-tight">Application Submitted!</h2>
          <p className="text-neutral-600 text-sm mt-3 leading-relaxed">
            Your application was successfully created. A referral request has been sent to{' '}
            <strong className="text-neutral-900">{referrerEmail}</strong>.
          </p>
          <p className="text-neutral-500 text-xs mt-3 leading-relaxed">
            Once your referral is accepted, you can log in to complete your profile.
          </p>
          <div className="mt-8 pt-6 border-t border-neutral-100">
            <Link
              to="/login"
              className="inline-flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white py-2 px-6 rounded-lg text-sm font-semibold transition-colors shadow-sm"
            >
              Go to Login
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 py-12 px-4">
      <div className="w-full max-w-lg bg-white rounded-xl border border-neutral-200 shadow-sm p-8 animate-fade-in">
        <div className="flex flex-col items-center mb-8">
          <img src="/favicon.ico" alt="AIRP Logo" className="w-12 h-12 mb-3" />
          <h2 className="text-xl font-bold text-neutral-900 tracking-tight">Apply for Internship</h2>
          <p className="text-neutral-500 text-xs mt-1">Submit your details for employee referral</p>
        </div>

        {error && (
          <div className="mb-6 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg flex items-start gap-2">
            <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="John Doe"
                  className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
                Personal Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="john.doe@gmail.com"
                  className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
                Account Password
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

            <div>
              <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
                College / University
              </label>
              <div className="relative">
                <GraduationCap className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
                <input
                  type="text"
                  required
                  value={college}
                  onChange={(e) => setCollege(e.target.value)}
                  placeholder="SSN College"
                  className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
              Referring Employee Email (@agilisium.com)
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 w-4 h-4 text-neutral-400" />
              <input
                type="email"
                required
                value={referrerEmail}
                onChange={(e) => setReferrerEmail(e.target.value)}
                placeholder="employee@agilisium.com"
                className="w-full pl-10 pr-4 py-2 text-sm border border-neutral-200 rounded-lg outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all bg-neutral-50/50"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-neutral-600 mb-1.5 uppercase tracking-wider">
              Resume (PDF only)
            </label>
            <div className="relative mt-1">
              <label className="flex flex-col items-center justify-center border border-dashed border-neutral-200 rounded-lg py-6 bg-neutral-50/50 hover:bg-neutral-50 transition-colors cursor-pointer">
                <FileText className="w-8 h-8 text-neutral-400 mb-2" />
                <span className="text-xs text-neutral-600 font-medium">
                  {resume ? resume.name : 'Click to upload your resume (Max 5MB)'}
                </span>
                <input
                  type="file"
                  required
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white py-2.5 px-4 rounded-lg text-sm font-semibold flex items-center justify-center gap-2 transition-colors disabled:opacity-70 disabled:cursor-not-allowed shadow-sm shadow-brand-100"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Submitting application...
              </>
            ) : (
              'Submit Application'
            )}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-neutral-100 text-center">
          <p className="text-xs text-neutral-500">
            Already have an account?{' '}
            <Link to="/login" className="text-brand-600 font-semibold hover:underline">
              Log In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
