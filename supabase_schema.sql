-- ============================================================
-- AIRP - Supabase SQL Schema
-- ============================================================
-- Run this in: Supabase Dashboard > SQL Editor > New Query
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,  -- 'Super Admin', 'Admin', 'Employee', 'Intern'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Internships table
CREATE TABLE IF NOT EXISTS internships (
    id SERIAL PRIMARY KEY,
    intern_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR NOT NULL,
    college VARCHAR NOT NULL,
    duration_months INTEGER,
    tentative_start_date DATE,
    tentative_end_date DATE,
    preferred_role VARCHAR,
    resume_path VARCHAR,         -- Supabase Storage public URL
    referrer_email VARCHAR NOT NULL,
    referrer_id INTEGER REFERENCES users(id),
    status VARCHAR NOT NULL DEFAULT 'WAITING_EMPLOYEE',
    offer_letter_path VARCHAR,   -- Supabase Storage public URL
    final_ppt_path VARCHAR,      -- Supabase Storage public URL
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    intern_id INTEGER NOT NULL REFERENCES users(id),
    date DATE NOT NULL,
    status VARCHAR NOT NULL,  -- 'Present', 'Absent'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Company Projects table
CREATE TABLE IF NOT EXISTS company_projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    intern_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
    project_type VARCHAR NOT NULL,  -- 'Company' or 'Own'
    company_project_id INTEGER REFERENCES company_projects(id),
    own_project_title VARCHAR,
    own_project_description TEXT,
    status VARCHAR NOT NULL DEFAULT 'In Progress',  -- 'In Progress', 'Completed'
    progress_pct INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Settings table (for SMTP config etc.)
CREATE TABLE IF NOT EXISTS settings (
    key VARCHAR PRIMARY KEY,
    value VARCHAR NOT NULL
);

-- Audit Logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- Seed: Super Admin account
-- Password: SuperAdmin@123 (bcrypt hash)
-- Change password immediately after first login!
-- ============================================================
INSERT INTO users (email, hashed_password, role, is_active)
VALUES (
    'superadmin@agilisium.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'Super Admin',
    true
)
ON CONFLICT (email) DO NOTHING;
