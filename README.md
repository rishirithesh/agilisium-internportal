# Agilisium Intern & Referral Portal (AIRP)

A full-stack internship management portal built with FastAPI + React.

## Architecture (Production)

| Layer | Service | URL |
|-------|---------|-----|
| Frontend | Vercel | `https://agilisium-internportal.vercel.app` |
| Backend API | Render | `https://airp-backend.onrender.com` |
| Database | Supabase PostgreSQL | `db.docrqhnmfmjvxegnxgpd.supabase.co` |
| File Storage | Supabase Storage | `docrqhnmfmjvxegnxgpd.supabase.co/storage` |

---

## 🚀 Deployment Guide

### Step 1 — Supabase Setup

1. Go to [supabase.com](https://supabase.com) and open your project
2. **Create Storage Buckets** (Dashboard → Storage → New Bucket):
   - `resumes` → Public ✅
   - `offers` → Public ✅
   - `presentations` → Public ✅
3. **Run SQL Schema** (Dashboard → SQL Editor → New Query):
   - Paste the contents of [`supabase_schema.sql`](./supabase_schema.sql) and click Run
4. **Get your credentials** (Dashboard → Project Settings → API):
   - **Project URL**: `https://docrqhnmfmjvxegnxgpd.supabase.co`
   - **service_role** secret key (needed for backend)
5. **Get DB password** (Dashboard → Project Settings → Database → Connection string)

---

### Step 2 — Deploy Backend on Render

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo: `rishirithesh/agilisium-internportal`
3. Configure:
   - **Name**: `airp-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
4. Set **Environment Variables** in Render dashboard:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@db.docrqhnmfmjvxegnxgpd.supabase.co:5432/postgres` |
   | `JWT_SECRET` | `9825b741029c017d23a49f87ef9280cdb90a12e2c56aef7b62c451db93ff0e81` |
   | `JWT_ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
   | `SUPABASE_URL` | `https://docrqhnmfmjvxegnxgpd.supabase.co` |
   | `SUPABASE_SERVICE_KEY` | `your-service_role-key` |
   | `SMTP_HOST` | `smtp.gmail.com` |
   | `SMTP_PORT` | `587` |
   | `SMTP_USER` | `rishi2470003@ssn.edu.in` |
   | `SMTP_PASS` | `hava kcby kmpa qqom` |
   | `SMTP_FROM` | `Agilisium Intern Portal <rishi2470003@ssn.edu.in>` |
   | `UPLOAD_DIR` | `uploads` |

5. Click **Deploy**. Copy the deployed URL (e.g. `https://airp-backend.onrender.com`)

> ⚠️ Free Render services sleep after 15 min of inactivity and take ~30s to wake up.

---

### Step 3 — Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import GitHub repo: `rishirithesh/agilisium-internportal`
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Set **Environment Variables** in Vercel:

   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://airp-backend.onrender.com/api/v1` |

5. Click **Deploy**

---

## 💻 Local Development

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# Copy .env.example to .env and fill in values
cp .env.example .env
uvicorn app.main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
# Vite proxy handles /api → localhost:8001 automatically
npm run dev
```

---

## Default Credentials (after running schema)

| Role | Email | Password |
|------|-------|----------|
| Super Admin | `superadmin@agilisium.com` | `secret` |

> ⚠️ Change the Super Admin password immediately after first login via the Supabase SQL editor:
> ```sql
> -- Generate a new hash at: https://bcrypt-generator.com
> UPDATE users SET hashed_password = '$2b$12$NEW_HASH_HERE' WHERE email = 'superadmin@agilisium.com';
> ```
