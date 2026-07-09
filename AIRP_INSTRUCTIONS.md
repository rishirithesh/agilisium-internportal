# AIRP IMPLEMENTATION SPECIFICATION
Version: 1.0

# Agilisium Intern & Referral Portal (AIRP)

## Objective

Build a production-ready enterprise web application for managing the complete lifecycle of internship referrals, approvals, onboarding, internship tracking, project management, and completion.

This repository already contains an initial scaffold.

Do NOT recreate the architecture.

Inspect the existing repository first and extend it into a complete production-ready system.

---

# Branding

Application Name:
**Agilisium Intern & Referral Portal (AIRP)**

Use this branding consistently across:

- Browser title
- Navbar
- Sidebar
- Login page
- Loading screen
- Dashboard
- Emails
- Metadata
- Footer

The repository contains `favicon.ico`.

Use it everywhere as the official branding.

Do not generate another logo.

---

# UI / UX

The UI should feel like a premium enterprise SaaS product.

Design language:

- Light theme by default
- Professional appearance
- Cool blue / gray palette
- Clean white surfaces
- Minimalistic
- Modern
- Fast
- Responsive
- Accessible

Inspiration:

- Linear
- Stripe Dashboard
- Microsoft Fluent
- GitHub
- Ashby

Typography:

- Inter or Geist

Animations:

- Subtle only
- Framer Motion
- No excessive gradients
- No glassmorphism

---

# Preferred Tech Stack

Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- React Hook Form
- Zod
- TanStack Table
- Framer Motion

Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic v2
- JWT Authentication
- bcrypt

Database

- PostgreSQL

Emails

- SMTP only

Do NOT use:

- Redis
- BullMQ
- Celery
- Docker-only dependencies

---

# Authentication

There are ONLY FOUR roles.

1. Super Admin
2. Admin
3. Employee
4. Intern

There is NO public registration page.

Only pages available without login:

- Login
- Apply for Internship

---

# Super Admin

Hardcode:

admin@agilisium.com

The Super Admin account always exists.

Responsibilities:

- Create Admin accounts
- Create Employee accounts
- View platform analytics
- View audit logs
- Manage SMTP configuration
- View system settings

Admins and Employees never self-register.

---

# Admin

Admins are created only by Super Admin.

Responsibilities:

- Review internship applications
- Approve / Reject internships
- Upload offer letters
- Send emails
- Track attendance
- Monitor projects
- Manage company project ideas
- View intern progress

---

# Employee

Employees are created only by Super Admin.

They login using their official
@agilisium.com email.

Responsibilities:

- View referral requests
- Accept or reject referrals
- Track referred interns

---

# Intern Application Flow

The workflow is:

Intern clicks "Apply"

↓

Enters:

- Name
- Personal Email
- College
- Resume (PDF only)
- Referring Employee Email (@agilisium.com)

↓

Temporary account created

↓

Status:

Waiting for Employee Approval

↓

Employee receives referral request

↓

Employee accepts OR rejects

Reject:

Notify intern.

Accept:

Intern account becomes active.

Status:

Referral Accepted

Intern now completes profile.

---

# Internship Profile

Intern submits:

- Name
- College
- Internship Duration
- Tentative Start Date
- Tentative End Date
- Preferred Role
- Resume (PDF)
- Referring Employee

Submit

↓

Admin Review

↓

Approve or Reject

---

# Offer Workflow

Admin approves application

↓

Uploads Offer Letter (PDF)

↓

SMTP Email sent

↓

Intern portal displays

Accept

Decline

↓

Accept

Internship Activated

↓

Automatic onboarding email

↓

Intern Dashboard enabled

---

# Phase 2 — Internship Journey

Modules:

## Attendance

Calendar-based attendance.

Intern marks:

- Present
- Absent

Admins can view all attendance.

Employees cannot.

---

## Project Selection

Intern can either:

- Choose own problem statement

OR

- Choose company project

Admins can create company projects.

---

## Project Tracking

Intern regularly updates:

- Progress
- Status
- Notes

Admin monitors progress.

---

## Presentation Template

Repository contains PPT template.

Intern should be able to:

- Download template
- Prepare presentation
- Upload final PPT

---

## Internship Completion

Intern uploads:

- Final Presentation PPT

Admin reviews.

Marks internship complete.

---

# Emails

Every workflow should generate SMTP emails.

Examples:

- Referral received
- Referral accepted
- Referral rejected
- Internship profile submitted
- Internship approved
- Offer letter sent
- Offer accepted
- Offer rejected
- Internship activated

No Redis or queue infrastructure.

Use centralized SMTP services.

---

# Security

Implement:

- JWT Authentication
- RBAC
- Password hashing
- Route protection
- File validation
- Audit logging
- Input validation
- Secure uploads

---

# File Uploads

Support:

- Resume (PDF)
- Offer Letter (PDF)
- PPT Template
- Final PPT

Validate:

- Type
- Size

---

# General Requirements

Every feature must include:

- Frontend
- Backend
- Database
- Validation
- APIs
- Emails
- Notifications
- Audit Logs

Never implement UI only.

Never leave placeholders.

Repository must always build successfully.

---

# Definition of Done

The application is complete only when:

- Referral workflow functions end-to-end.
- Admin approval works.
- Offer workflow works.
- Internship activation works.
- Attendance works.
- Project tracking works.
- Final PPT upload works.
- SMTP emails work.
- RBAC works.
- Responsive UI works.
- Zero build errors.
- Production-ready quality.
