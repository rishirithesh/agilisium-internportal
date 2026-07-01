## Run instructions (local development)

1) Create a Python virtualenv and install requirements

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

2) Configure environment

- Copy `backend/.env.example` to `backend/.env` and fill in real credentials (DB, SMTP, SECRET_KEY).

3) Apply database migrations (if you have a running Postgres instance)

```bash
cd backend
alembic upgrade head
```

If you don't have Postgres available, you can use a local SQLite for development by adjusting `backend/app/core/config.py` and `backend/alembic/env.py` (not recommended for production).

4) Start the backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5) Start the frontend

```bash
cd frontend
npm install
npm run dev
```

6) Credentials to provide back to me (paste into chat) for me to run migrations and smoke checks if you want me to run them:

- `DATABASE_URL` (e.g. postgresql+psycopg2://user:password@localhost:5432/airp_db)
- `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_APP_PASSWORD`
- `SECRET_KEY`

Keep secrets out of source control. Use a secure channel to share credentials.

7) One-tap approval (email links)

- When a candidate completes registration, the referring employee receives an approval-request email containing approve/reject links.
- These links call public endpoints:
	- `GET /api/v1/referrals/{referral_id}/approve_by_token?token=...`
	- `GET /api/v1/referrals/{referral_id}/reject_by_token?token=...&reason=...`
- To enable this flow, ensure SMTP credentials are set in `backend/.env` so the app can send emails.

8) Admin & user offer endpoints

- Admins can list offers via `GET /api/v1/admin/offers`.
- Interns can list their offers via `GET /api/v1/offers` and download via `GET /api/v1/offers/{offer_id}/download`.

9) Email behaviour and logging

- Emails are sent directly via SMTP (no external queue). The app will retry sends up to 3 times with exponential backoff.
- If the backend DB is configured, email delivery attempts and failures are recorded in the `email_logs` table for auditing.
- Ensure SMTP credentials in `backend/.env` are correct for reliable delivery.


