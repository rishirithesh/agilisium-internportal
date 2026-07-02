# Agilisium Intern & Referral Portal (AIRP) - Running Instructions

Follow these instructions to configure the database, start the FastAPI backend, and start the React frontend.

---

## 1. Database Configuration
The application connects to a local PostgreSQL instance.

* **Port**: `5432`
* **Username**: `postgres`
* **Password**: `rishi`
* **Database**: `airp`

### Seeding / Resetting the Database:
To create database tables and seed initial Super Admin, HR Admin, Employee, and Company Project details, run:
```bash
# From the project root directory
python backend/app/scripts/seed.py
```

---

## 2. Start the Backend Server
The backend is built with FastAPI. It runs on port `8001` to prevent local conflicts.

```bash
# Navigate to the backend directory
cd backend

# Run the backend using Uvicorn
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```
The backend API documentation will be available at `http://127.0.0.1:8001/docs`.

---

## 3. Start the Frontend Server
The frontend is built with React, TypeScript, and Vite.

```bash
# Navigate to the frontend directory
cd frontend

# Install package dependencies
npm install

# Start the Vite development server
npm run dev
```
Open your browser at the URL output by Vite (typically `http://localhost:5173` or `http://localhost:5175`).

---

## 4. Seeded Test Credentials
Use the following seeded accounts to verify the workflow panels:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Super Admin** | `admin@agilisium.com` | `Admin@123` |
| **HR Admin** | `hr_admin@agilisium.com` | `Admin@123` |
| **Employee 1** | `emp1@agilisium.com` | `Employee@123` |
| **Employee 2** | `emp2@agilisium.com` | `Employee@123` |
| **Employee 3** | `emp3@agilisium.com` | `Employee@123` |
