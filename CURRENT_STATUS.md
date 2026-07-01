# Current Status — Agilisium IRP

Date: 2026-07-01

## Summary
- Backend: major referral and offer flows implemented (invite -> intern registration -> employee approval -> offer upload/send -> accept -> internship creation). Email sending uses direct SMTP with retries and DB logging. Alembic revisions generated but not applied.
- Frontend: Vite + React UI implemented for login, referrals pages, invite registration, one-tap approval processing, offers list and offer detail/accept. Frontend builds successfully.

## Backend (implemented)
- Referral flows: create referral, invite token generation, register candidate, employee approve/reject (token links).
- Offer flows: admin upload, offer versioning, send offer email, user download, accept -> creates Internship record.
- Email: `EmailService` using direct SMTP + exponential backoff; logs to `email_logs` when DB available.
- Storage: local filesystem storage service for uploaded offer PDFs.
- Validation: PDF header + size checks implemented.
- Migrations: Alembic revisions created under `backend/alembic/versions/` (0001..0004) but `alembic upgrade head` has not been applied due to DB credentials.

## Frontend (implemented)
- API client with refresh token handling: `frontend/src/api/client.ts`.
- Referral pages: list, create, detail (`frontend/src/features/referrals/*`), invite page (`/invite`) and approval page (token handler).
- Offers: list (`/offers`), detail + accept flow (`/offers/:id`).
- Shared UI components: `Input`, `Button`, `Card` used across pages.
- Build validated: `npm run build` succeeds; production assets in `frontend/dist/`.

## Pending / To do
- Apply Alembic migrations to the target PostgreSQL database (needs valid DB credentials). See `backend/.env.example` and `RUN_INSTRUCTIONS.md`.
- Frontend: admin offer upload UI, offer-version history page, richer client-side validation and accessibility polish (implemented in frontend; see pages under `frontend/src/features/offers`).
- Backend: finalize small worker/task code paths to pass DB sessions into `EmailService` in all call sites (some helper files still instantiate without DB); add tests and CI.
- Security: review JWT refresh, secure cookie usage, rate-limiting, and harden token single-use guarantees if required.
- Observability: add health checks, metrics, and logging aggregation (deferred per project note).

## Required to run everything locally
- PostgreSQL connection (DATABASE_URL) with a user that can run migrations.
- SMTP credentials (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD) for `EmailService` to send emails.
- Environment files: copy `backend/.env.example` -> `backend/.env` and fill credentials.

## Quick run commands

Backend (from repo root):
```
cd backend
pip install -r requirements.txt
# set backend/.env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```
cd frontend
npm install
npm run dev          # development
npm run build        # verify production build
```

## Helpful file locations
- Backend env/migrations: `backend/alembic/` and `backend/alembic/versions/`
- Backend run notes: `RUN_INSTRUCTIONS.md` and `backend/.env.example`
- Frontend API client: `frontend/src/api/client.ts`
- Frontend entry and routes: `frontend/src/App.tsx`
 
## Architecture / API handling (theory)

- API surface: the backend exposes a REST API under `/api/v1/*` (configurable via `VITE_API_BASE_URL` on the frontend). Key endpoints used by the frontend live under `/referrals`, `/offers`, and `/admin/offers`.
- Frontend responsibilities: the React app (in `frontend/src`) renders UI, performs client-side validation, and calls backend APIs via `frontend/src/api/*` (shared `apiClient` handles Authorization headers and token refresh). The frontend uses `@tanstack/react-query` for data fetching and caching.
- Backend responsibilities: the FastAPI app (in `backend/app`) validates requests, runs business logic in services (e.g. `ReferralService`, `OfferService`, `EmailService`), persists data via SQLAlchemy, and stores uploaded files via `StorageService`.
- Where they connect: the frontend's `apiClient` sends HTTP requests to the backend base URL. Authentication is JWT-based: the frontend stores access/refresh tokens in localStorage and `apiClient` adds `Authorization: Bearer <token>` to requests. The backend validates tokens and applies RBAC checks from `app/core/permissions.py`.
- File uploads: the frontend sends `multipart/form-data` to admin upload endpoints; the backend validates PDF content and saves files to local storage before creating `Offer`/`OfferVersion` records.

## SMTP details (to set in `backend/.env`)

You provided SMTP details — add these to `backend/.env` (do not commit this file):

```
SMTP_HOST="smtp.office365.com"
SMTP_PORT="587"
SMTP_USER="rishi2470003@ssn.edu.in"
SMTP_PASS="hava kcby kmpa qqom"
SMTP_FROM="Agilisium LMS <rishi2470003@ssn.edu.in>"
```

## Database (what I mean by "DB details") and how to create one

I need a PostgreSQL connection string that the backend can use to run Alembic migrations and to persist data. The backend reads `DATABASE_URL` from `backend/.env` (or individual `POSTGRES_*` variables depending on your config). Typical connection string format:

```
postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
```

Example local setup using `psql` (Postgres must be installed):

1. Create a database and user (run in a terminal where `psql` is available):

```bash
# become postgres user (on Linux/macOS)
sudo -iu postgres
# open psql
psql
# create user and db (replace password)
CREATE USER airp_user WITH PASSWORD 'StrongPassword123!';
CREATE DATABASE airp_dev OWNER airp_user;
# grant privileges
GRANT ALL PRIVILEGES ON DATABASE airp_dev TO airp_user;
\q
```

2. Construct the connection string and put it into `backend/.env` as `DATABASE_URL`:

```
DATABASE_URL="postgresql://airp_user:StrongPassword123!@localhost:5432/airp_dev"
```

3. Then run migrations and start the app:

```bash
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

If you prefer, provide the full `DATABASE_URL` here and I will run migrations locally in this environment.


## Recommended next steps
1. Provide DB and SMTP credentials so I can run `alembic upgrade head` and verify DB migrations end-to-end.
2. Implement admin offer upload UI and offer-version history in the frontend (I can add these next).
3. Add unit/integration tests and CI pipeline; optionally add simple health endpoints for deployment checks.

If you want, I can now: apply the migrations (if you supply DB creds), add the admin upload UI, or implement offer-version history UI. Tell me which to do next.
