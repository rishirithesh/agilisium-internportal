# AIRP Deployment Instructions

## 1. Backend deployment (Render)
1. Create a new Render web service pointing to the repository root.
2. Set the root directory to `backend`.
3. Use the build command:
   - `pip install -r requirements.txt`
4. Use the start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add these environment variables in Render:
   - `DATABASE_URL`
   - `JWT_SECRET`
   - `JWT_ALGORITHM=HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=1440`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `SMTP_HOST`
   - `SMTP_PORT`
   - `SMTP_USER`
   - `SMTP_PASS`
   - `SMTP_FROM`
   - `UPLOAD_DIR=uploads`

## 2. Supabase configuration
1. Create or open your Supabase project.
2. In Project Settings > API, copy:
   - `Project URL` to `SUPABASE_URL`
   - `service_role` secret to `SUPABASE_SERVICE_KEY`
3. In Project Settings > Database, copy the connection string to `DATABASE_URL`.
4. Create the storage buckets named:
   - `resumes`
   - `offers`
   - `presentations`
5. Make the buckets public if your app needs public file access.

## 3. Frontend deployment (Vercel)
1. Create a Vercel project for the `frontend` folder.
2. Set the build command to `npm run build`.
3. Set the output directory to `dist`.
4. Add this environment variable:
   - `VITE_API_BASE_URL=https://<your-render-backend-url>/api/v1`

## 4. Database initialization
After deployment, initialize the database schema and seed the default accounts:
- `python app/scripts/seed.py`

## 5. Verification checklist
- Backend health endpoint responds at `/`.
- API docs are available at `/docs`.
- File uploads work through Supabase Storage or local fallback storage.
- Login and dashboard flows work with seeded accounts.
