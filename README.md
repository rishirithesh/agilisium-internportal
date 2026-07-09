<<<<<<< HEAD
# AIRP — Agilisium Intern Referral Portal

Phase 1 scaffold: FastAPI + SQLAlchemy/Alembic + Neon Postgres backend, React/Vite/TS frontend,
and direct SMTP-based email automation for OTPs, referrals, and offer updates. This pass implements
full auth (password + OTP, all 4 roles), centralized RBAC, the complete referral state machine,
and one end-to-end vertical slice (create referral → transition through every workflow stage) wired
from database to UI.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL (Neon), aiosmtplib
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Radix UI primitives, TanStack Query, React Hook Form, Zod
- **Auth:** JWT (access + rotating refresh tokens, persisted/revocable), bcrypt password hashing, OTP-over-email

## Project layout

```
airp/
  backend/
    app/
      core/         # config, db session, security, RBAC policy, exceptions
      models/        # SQLAlchemy ORM entities
      schemas/       # Pydantic request/response DTOs
      repositories/  # data-access layer (no business logic)
      services/      # business logic, orchestrates repos + state machine + email + audit
      workflows/      # centralized referral state machine
      api/v1/        # FastAPI routers
      workers/       # arq background job definitions (email queue)
      templates/email/ # Jinja2 HTML email templates
      scripts/seed.py  # demo data for local dev
    alembic/         # migrations
  frontend/
    src/
      api/           # axios client + typed API functions
      features/       # auth, dashboard, referrals (feature-based modules)
      components/    # shared UI primitives + layout shell
      types/         # shared domain types mirroring backend schemas
```

## Local setup

### 1. Database (Neon)
Create a free Neon Postgres project, grab the pooled connection string (for the app) and the
direct connection string (for Alembic), and put both in `backend/.env` (copy from `.env.example`).

### 2. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, ALEMBIC_DATABASE_URL, SMTP_*, JWT_SECRET
alembic revision --autogenerate -m "init schema"
alembic upgrade head
python -m app.scripts.seed   # creates one demo user per role, password: ChangeMe123!
uvicorn app.main:app --reload
```
API now running at `http://localhost:8000` (docs at `/docs`).

### 3. SMTP email setup
SMTP uses an app password (for example Gmail: Account → Security → App Passwords) — set
`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_APP_PASSWORD`, `SMTP_FROM_NAME`, and `SMTP_FROM_EMAIL` in `.env`.

### 4. Frontend
```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
```
App now running at `http://localhost:5173`. Log in with one of the seeded accounts
(`employee@agilisium.com`, `intern@airp.local`, `admin@agilisium.com`, `mainadmin@agilisium.com`,
password `ChangeMe123!`).

## What's implemented in this pass

- Four-role auth (Employee, Intern, Admin, Main Admin): password login, OTP login, JWT
  access/refresh with server-side revocation, centralized `can()` RBAC policy reused across
  every route.
- Full referral state machine (`REFERRED → … → COMPLETED`, with `REJECTED` and
  `CHANGES_REQUESTED` branches) as a single source of truth — no status is ever set outside
  `workflows/referral_state_machine.py`.
- Referral create/list/detail/transition API + matching React pages (list, create form,
  detail + timeline + next-step actions), with loading skeletons and empty states.
- Audit logging on every sensitive action; in-app notifications + best-effort email on every
  status transition through SMTP.
- Dark/light theme, responsive app shell, reusable UI primitives (Button, Input, Card, StatusChip).

## Not yet built (next passes, per the original roadmap)

Resume/offer file upload + S3 storage abstraction, full admin/main-admin portals (bulk actions,
analytics, user management), notification center UI, in-app real-time updates, Playwright/Jest
test suites, and deployment configs (Dockerfile, CI). Flag which of these you want next and
I'll build it as the next slice on top of this foundation.

## Assumptions made (per AIRP.md's instruction to document and proceed)

- SQLAlchemy + Alembic used in place of Prisma, per your explicit choice.
- Frontend is a Vite SPA rather than Next.js App Router, since the backend is no longer
  Next.js Route Handlers — no SSR/server components in this stack.
- Local file storage as the default `STORAGE_BACKEND`, with an S3-compatible path already
  modeled in config for when you're ready to deploy.
=======
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
>>>>>>> master
