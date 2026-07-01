# AGILISIUM INTERN PORTAL
# EXISTING PROJECT

The repository already contains the initial application scaffold.
## AI IMPLEMENTATION SPECIFICATION

Version: 2.0

This document is the official implementation guide for the Agilisium Intern Portal.

The repository already contains the initial project scaffold.

Your responsibility is to COMPLETE the application.

Do NOT redesign the architecture.

Do NOT create another architecture.

Do NOT recreate folder structures that already exist.

Instead,

inspect the repository,

understand the existing scaffold,

and extend it into a production-ready enterprise application.

---

# PRIMARY SOURCE OF TRUTH

AIRP.md is available inside the repository.

Read it completely before implementing anything.

Everything implemented must follow AIRP.md.

If AIRP.md and this document conflict,

AIRP.md takes precedence.

If implementation assumptions are required,

choose the most scalable enterprise solution.

---

# PROJECT

Application Name

Agilisium Intern Portal

The application manages the complete lifecycle of interns inside Agilisium.

It combines

Employee Referral

Recruitment

Offer Management

Internship Management

Attendance

Projects

Documentation

Reports

Notifications

into a single enterprise platform.

---

# COMPLETE WORKFLOW

The application follows this exact lifecycle.

Employee Registration

↓

Employee Login

↓

Employee creates Referral

↓

Intern receives Referral Email

↓

Intern Registration

↓

Employee Approval

↓

Intern Account Created

↓

Intern Profile Creation

↓

Admin Review

↓

Admin Approval / Rejection

↓

Offer Letter Upload

↓

Offer Letter Sent

↓

Intern Accepts / Rejects

↓

Internship Activated

↓

Internship Workspace Created

↓

Attendance

↓

Project

↓

Documentation

↓

Internship Completion

Every state transition must be enforced.

No workflow may bypass another workflow.

Every transition must be validated.

---

# USER ROLES

There are only four system roles.

1.

Main Admin

Full platform ownership.

2.

Admin

Recruitment and internship management.

3.

Employee

Can refer interns.

Can approve referral requests.

Can track referred interns.

4.

Intern

Can only access their own internship workspace.

---

# EMAIL DOMAIN RULES

These rules are mandatory.

Main Admin

Must use

@agilisium.com

Admin

Must use

@agilisium.com

Employee

Must use

@agilisium.com

Intern

Must NEVER use

@agilisium.com

Interns register using personal email only.

Examples

Allowed

john@gmail.com

alice@yahoo.com

student@ssn.edu.in

student@gmail.com

Rejected

intern@agilisium.com

abc@agilisium.com

If an intern attempts registration using an Agilisium email,

reject registration.

Show an appropriate validation message.

---

# EMPLOYEE REGISTRATION

Employees create an account using

their official

@agilisium.com

email.

Registration Flow

Enter Agilisium Email

↓

Validate domain

↓

Generate OTP

↓

Send OTP via Email

↓

OTP Verification

↓

Create Password

↓

Create Employee Profile

↓

Employee Dashboard

Employee fields

Full Name

Employee ID (optional)

Department

Designation

Official Email

Phone Number

Profile Picture

Password

Created Date

Status

Every employee account must be verified before activation.

---

# EMPLOYEE LOGIN

Employee logs in using

Official Email

+

Password

OR

OTP Login

Support

Remember Me

Forgot Password

Reset Password

Session Management

Secure Cookies

JWT

Route Protection

Automatic Logout on session expiry

---

# INTERN REGISTRATION

Interns DO NOT create an account directly.

They must first be referred by an employee.

Registration Flow

Employee creates referral

↓

System sends referral email

↓

Intern clicks referral link

↓

Intern Registration

↓

Pending Employee Approval

↓

Employee Accepts

↓

Intern Account Created

↓

Intern Login

↓

Complete Profile

Intern fields

Personal Email

Password

Name

Phone Number

College

Degree

Department

Graduation Year

LinkedIn

GitHub

Portfolio

Current Location

Resume

Preferred Internship Role

Skills

Resume upload must support PDF only.

Maximum size configurable.

---

# EMPLOYEE REFERRAL FLOW

This is the most important workflow.

Employees should have a page

"My Referrals"

and another page

"Create Referral"

Employee clicks

Create Referral

↓

Enter

Intern Name

Intern Email

College

Phone

Preferred Role

Department

Notes

Resume (optional)

↓

Submit

↓

Referral Request Created

↓

Intern receives referral email

↓

Intern registers

↓

Referral moves to

Pending Employee Approval

↓

Employee receives notification

↓

Employee can

Approve

Reject

Approve creates the intern account.

Reject deletes the pending registration.

The employee must see

Pending Referrals

Approved Referrals

Rejected Referrals

Accepted Offers

Current Interns

Each referral should display

Intern Name

College

Role

Created Date

Current Status

Latest Activity

Quick Actions

---

# INTERN ACCOUNT CREATION

Intern account should NOT exist until employee approval.

Before approval,

store registration temporarily.

Recommended

Redis

Database temporary table

Cache

Do not create the user record.

Upon employee approval

Create

User

Intern Profile

Authentication Credentials

Notifications

Audit Logs

Send Welcome Email

---

# INTERN PROFILE

After first login,

intern must complete profile.

Fields

Full Name

College

University

Degree

Branch

Current Semester

Graduation Year

Phone

Emergency Contact

LinkedIn

GitHub

Portfolio

Skills

Resume

Preferred Role

Bio

Profile completion percentage should be shown.

Intern cannot proceed until mandatory fields are completed.

---

# REFERRAL STATUS

Use a centralized state machine.

Allowed states

Referral Created

↓

Invitation Sent

↓

Intern Registered

↓

Pending Employee Approval

↓

Employee Approved

↓

Profile Pending

↓

Profile Submitted

↓

Admin Review

↓

Rejected

OR

Approved

↓

Offer Uploaded

↓

Offer Sent

↓

Offer Accepted

↓

Internship Active

↓

Internship Completed

Every status transition must be validated.

Manual database updates should never bypass business rules.

---

# ROLE PERMISSIONS

Main Admin

Everything.

Admin

Everything except system configuration.

Employee

Own referrals only.

Intern

Own profile only.

Never expose another user's data.

All permissions should be enforced

Backend

Frontend

Middleware

API

Database Services

---

# BRANDING

Application Name

Agilisium Intern Portal

Do NOT display

AIRP

inside the UI.

AIRP may remain only as an internal repository name.

Use

Agilisium Intern Portal

throughout the application.

Browser Title

Sidebar

Navbar

Dashboard

Authentication

Emails

Notifications

Metadata

Footer

Loading Screens

Settings

Help Pages

---

# LOGO

The repository contains

favicon.ico

Use this as the official logo.

Do NOT generate another logo.

Configure it as

Browser Favicon

Sidebar Logo

Navbar Logo

Authentication Pages

Dashboard Header

Loading Screen

Email Header

Metadata

Manifest

Use the same branding consistently throughout the application.

Never distort or recolor the icon.

---

# IMPLEMENTATION RULES

Never generate placeholder implementations.

Never generate mock APIs.

Never leave TODO comments.

Never duplicate existing utilities.

Never recreate components already present.

Inspect before implementing.

Extend before replacing.

Every feature should be fully integrated across

Frontend

Backend

Database

API

Validation

Authentication

Authorization

Notifications

Emails

Logging

Tests

The repository should remain buildable after every implementation.

Every completed feature should feel production-ready.

# DATABASE IMPLEMENTATION

Implement a production-ready PostgreSQL database using Prisma ORM.

Do NOT create duplicate models.

Normalize wherever appropriate.

Use UUIDs as primary keys.

Every table should include:

- id
- createdAt
- updatedAt
- createdBy (where applicable)
- updatedBy (where applicable)
- deletedAt (Soft Delete)

Never hard delete important business data.

Soft delete should be the default.

---

# CORE DATABASE TABLES

Implement the following models.

## User

This is the authentication table.

Fields

- id
- email
- passwordHash
- role
- isVerified
- isActive
- lastLogin
- createdAt
- updatedAt

Every user belongs to exactly one role.

Roles

- MAIN_ADMIN
- ADMIN
- EMPLOYEE
- INTERN

---

## Employee

Fields

- id
- userId
- employeeId
- fullName
- designation
- department
- officialEmail
- phone
- profilePhoto
- status

Relations

One Employee

↓

Many Referrals

---

## Intern

Fields

- id
- userId
- referralId
- fullName
- personalEmail
- phone
- college
- university
- degree
- specialization
- graduationYear
- preferredRole
- linkedin
- github
- portfolio
- bio
- resumeUrl
- profileCompletion
- internshipStatus

Relations

One Intern

↓

One Referral

↓

One Internship

---

## Referral

This is one of the most important tables.

Fields

- id
- employeeId
- internEmail
- internName
- college
- phone
- preferredRole
- department
- notes
- status
- invitationToken
- invitationExpiry
- employeeApprovedAt
- adminReviewedAt

Relations

Employee

↓

Referral

↓

Intern

---

## PendingInternRegistration

This table stores intern registrations BEFORE employee approval.

DO NOT create intern accounts immediately.

Fields

- id
- referralId
- email
- passwordHash
- enteredDetails
- createdAt
- expiresAt

Upon employee approval

↓

Move data into

Intern

Delete pending record

---

## Internship

Created ONLY after

Offer Accepted.

Fields

- id
- internId
- department
- mentorId (nullable)
- joiningDate
- completionDate
- currentStatus
- overallProgress

---

## Offer

Fields

- id
- internshipId
- offerLetterUrl
- uploadedBy
- status
- acceptedAt
- rejectedAt

---

## Attendance

Fields

- internshipId
- date
- checkIn
- checkOut
- hoursWorked
- workSummary
- learningSummary
- blockers
- nextDayPlan
- adminRemarks
- status

One row

per intern

per day.

---

## DailyWorkLog

Fields

- internshipId
- title
- description
- hoursSpent
- githubLink
- attachments
- submittedAt

---

## Project

Fields

- internshipId
- title
- problemStatement
- description
- objectives
- techStack
- githubRepository
- documentationLink
- presentationLink
- progress
- status

---

## CompanyProblemStatement

Admin-created table.

Fields

- title
- department
- description
- expectedOutcome
- skillsRequired
- difficulty
- mentor
- status

Interns can request assignment.

---

## Announcement

Admin-created announcements.

Fields

- title
- body
- attachments
- publishDate
- expiryDate
- priority

---

## Resource

Stores learning materials.

Fields

- title
- description
- category
- fileUrl
- uploadedBy

---

## Notification

Supports

Email

Portal Notifications

Fields

- userId
- title
- message
- type
- isRead
- relatedEntity
- createdAt

---

## EmailLog

Track every email.

Fields

- recipient
- template
- status
- sentAt
- retries
- error

---

## AuditLog

Track every important action.

Fields

- user
- action
- entity
- entityId
- previousValue
- newValue
- timestamp

Never skip audit logging.

---

# AUTHENTICATION

Implement Auth.js (NextAuth v5).

Support

Password Login

OTP Login

Forgot Password

Reset Password

Remember Me

Session Refresh

Logout

Secure Cookies

CSRF

JWT

Middleware

Route Protection

---

# EMAIL VALIDATION

Employee

Admin

Main Admin

Must ONLY register using

@agilisium.com

Reject every other domain.

Intern

Must NEVER register using

@agilisium.com

Reject immediately.

Examples

Employee

john@agilisium.com

✓

Intern

john@gmail.com

✓

Intern

john@agilisium.com

✕

---

# OTP FLOW

Employee Registration

↓

Enter Agilisium Email

↓

Generate OTP

↓

Store OTP securely

↓

Email OTP

↓

Verify OTP

↓

Create Password

↓

Create Employee Account

↓

Login

OTP expires.

Implement retry limits.

Prevent brute force attacks.

---

# PASSWORD POLICY

Minimum 8 characters.

At least

Uppercase

Lowercase

Number

Special Character

Never store plaintext passwords.

Use bcrypt.

---

# SESSION MANAGEMENT

Support

Multiple Devices

Remember Me

Session Expiry

Refresh Tokens

Secure Cookies

Automatic Logout

---

# ROLE BASED ACCESS CONTROL

Every request must pass

Authentication

↓

Authorization

↓

Business Validation

↓

Database

Never expose unauthorized data.

---

# PERMISSION MATRIX

Main Admin

Everything

Admin

Referral Management

Offer Management

Intern Management

Attendance Review

Reports

Announcements

Resources

Employee

Own Profile

Own Referrals

Referral Approval

Track Referrals

Intern

Own Profile

Own Attendance

Own Project

Own Reports

Own Documentation

Never access another intern's data.

---

# REFERRAL STATE MACHINE

Allowed transitions

Referral Created

↓

Invitation Sent

↓

Intern Registered

↓

Pending Employee Approval

↓

Employee Approved

↓

Intern Account Created

↓

Profile Pending

↓

Profile Submitted

↓

Admin Review

↓

Approved

↓

Offer Uploaded

↓

Offer Sent

↓

Offer Accepted

↓

Internship Active

↓

Internship Completed

Reject Flow

↓

Rejected

Do not allow skipping states.

Validate every transition.

---

# EMPLOYEE APPROVAL

Employee receives notification

↓

Employee opens Pending Referrals

↓

Approve

OR

Reject

Approve

↓

Create Intern Account

↓

Create User

↓

Create Intern Profile

↓

Delete Pending Registration

↓

Send Welcome Email

Reject

↓

Delete Pending Registration

↓

Notify Intern

↓

Update Referral Status

---

# ADMIN REVIEW

Admin reviews completed profile.

Admin can

Approve

Reject

Request Changes

Approve

↓

Upload Offer Letter

↓

Send Email

↓

Offer Sent

Reject

↓

Reason Mandatory

↓

Email Sent

↓

Referral Closed

Request Changes

↓

Intern edits profile

↓

Resubmits

↓

Admin Review

---

# API DESIGN

Every endpoint must

Authenticate

Authorize

Validate

Log

Return consistent response

Response format

success

message

data

meta

errors

Use proper HTTP status codes.

Never return raw Prisma errors.

---

# SERVER ACTIONS

Prefer Server Actions where appropriate.

Use API Routes only when external consumption is required.

Keep business logic inside Services.

Never inside UI.

---

# MIDDLEWARE

Protect

Admin Pages

Employee Pages

Intern Pages

API

Server Actions

Redirect unauthorized users.

Never rely on frontend protection alone.

---

# IMPLEMENTATION REQUIREMENTS

Whenever implementing a feature

Update

Database

Prisma

Validation

Services

API

Frontend

Types

Notifications

Emails

Audit Logs

Tests

Do not implement features partially.

Every feature should be fully integrated before moving to the next.

# PART 3 — EMPLOYEE MODULE & REFERRAL MANAGEMENT

The Employee Module is the entry point of the entire application.

Every intern must originate from an Employee Referral.

Interns should NEVER be able to bypass this workflow.

There should NEVER be a public "Create Intern Account" page.

The only way for an intern to join the platform is:

Employee Referral
↓

Referral Email
↓

Intern Registration
↓

Employee Approval
↓

Intern Account Creation

--------------------------------------------------

# EMPLOYEE DASHBOARD

After successful login, employees land on the Employee Dashboard.

Dashboard should include:

• Welcome Card

- Employee Name
- Department
- Profile Completion

• Quick Statistics

- Total Referrals
- Pending Referrals
- Pending Employee Approvals
- Active Interns
- Completed Internships

• Recent Activity

Recent referrals

Status updates

Offer acceptances

Admin messages

• Notifications

Unread notifications

Recent notifications

Notification Bell

• Quick Actions

Create Referral

My Referrals

Pending Approvals

Current Interns

Profile

Settings

--------------------------------------------------

# EMPLOYEE SIDEBAR

Dashboard

Create Referral

My Referrals

Pending Approvals

Current Interns

Notifications

Profile

Settings

Logout

--------------------------------------------------

# CREATE REFERRAL PAGE

This is one of the most important pages.

Employee clicks

Create Referral

Display a multi-step form.

--------------------------------------------------

STEP 1

Intern Information

Required Fields

• Full Name

• Personal Email

Must NOT be @agilisium.com

• Phone Number

• College

• University

• Degree

• Branch / Department

• Graduation Year

• Preferred Internship Role

Optional

LinkedIn

GitHub

Portfolio

Employee Notes

Resume Upload

(PDF only)

--------------------------------------------------

VALIDATIONS

Email

Cannot already exist

Cannot already have an active referral

Must not belong to @agilisium.com

Phone Number

Unique where applicable

Resume

PDF only

Maximum size configurable

Every required field must be validated.

--------------------------------------------------

STEP 2

Review

Employee reviews entered information.

Display summary.

Buttons

Back

Submit Referral

--------------------------------------------------

STEP 3

Submission

Upon clicking Submit

System should

Create Referral

Generate Invitation Token

Generate Expiry Date

Store Referral

Send Referral Email

Create Notification

Create Audit Log

Update Dashboard Statistics

Everything must happen inside a transaction.

--------------------------------------------------

REFERRAL EMAIL

Immediately after referral creation

Automatically send email.

Email contains

Greeting

Referral Information

Portal Introduction

Registration Link

Expiry Information

Support Contact

Button

Create Account

SMTP must be used.

Do not send synchronously.

Queue email.

--------------------------------------------------

INVITATION TOKEN

Generate secure random token.

Store hashed token.

Set expiry.

Example

7 Days

Expired links must not allow registration.

Display

Invitation Expired

Contact your referring employee.

--------------------------------------------------

MY REFERRALS PAGE

Display every referral created by this employee.

Modern Data Table

Columns

Intern Name

College

Preferred Role

Current Status

Created Date

Last Updated

Latest Activity

Actions

Support

Search

Filter

Sorting

Pagination

Export CSV

--------------------------------------------------

FILTERS

Referral Status

Department

Preferred Role

Date Range

College

Search by Name

Search by Email

--------------------------------------------------

STATUS COLORS

Referral Created

Blue

Invitation Sent

Purple

Intern Registered

Orange

Pending Employee Approval

Amber

Approved

Green

Rejected

Red

Offer Sent

Indigo

Offer Accepted

Emerald

Internship Active

Cyan

Completed

Slate

Status chips should remain consistent throughout the application.

--------------------------------------------------

REFERRAL DETAILS PAGE

Clicking a referral opens detailed page.

Sections

Referral Summary

Intern Information

Employee Notes

Resume

Timeline

Notifications

Audit History

Admin Activity

Current Status

Buttons

Approve

Reject

View Timeline

--------------------------------------------------

TIMELINE

Every referral should have a visual timeline.

Example

Referral Created

↓

Invitation Sent

↓

Intern Registered

↓

Employee Approval Pending

↓

Employee Approved

↓

Intern Profile Created

↓

Admin Review

↓

Offer Uploaded

↓

Offer Sent

↓

Accepted

↓

Internship Started

Use reusable timeline component.

--------------------------------------------------

PENDING APPROVALS

Employee receives approval requests only after intern completes registration.

Display

Pending Approval Queue

Columns

Intern

College

Email

Registered On

Days Waiting

Actions

Approve

Reject

--------------------------------------------------

APPROVE FLOW

Employee clicks Approve.

Show confirmation modal.

Approve Referral?

Buttons

Cancel

Approve

Upon approval

Create User

Create Intern

Create Authentication

Delete Pending Registration

Update Referral Status

Send Welcome Email

Notify Admin

Notify Intern

Create Audit Log

Update Statistics

All inside one database transaction.

--------------------------------------------------

REJECT FLOW

Employee clicks Reject.

Reason mandatory.

Minimum 20 characters.

Upon rejection

Delete Pending Registration

Update Referral

Notify Intern

Notify Admin

Audit Log

Notification

Employee can later create another referral.

--------------------------------------------------

CURRENT INTERNS PAGE

Employee can track interns they referred.

Display

Intern Name

Department

Project

Attendance

Current Status

Joining Date

Completion %

Project Progress

Buttons

View Profile

View Progress

--------------------------------------------------

EMPLOYEE PROFILE

Fields

Full Name

Employee ID

Department

Designation

Official Email

Phone

Profile Picture

Password

Notification Preferences

Email Preferences

Theme

--------------------------------------------------

SETTINGS

Allow employee to configure

Theme

Notification Preferences

Email Preferences

Profile Picture

Password

Two Factor Authentication (Future Ready)

--------------------------------------------------

NOTIFICATIONS

Employee receives notifications for

Intern Registered

Approval Required

Admin Approved

Admin Rejected

Offer Accepted

Offer Rejected

Internship Started

Internship Completed

System Announcements

Notifications should support

Mark Read

Mark All Read

Delete

Filter

--------------------------------------------------

SEARCH

Every employee table should support

Search

Filtering

Sorting

Pagination

Server-side implementation preferred.

--------------------------------------------------

API ENDPOINTS

POST

/referrals

Create Referral

GET

/referrals

Employee Referrals

GET

/referrals/{id}

Referral Details

PATCH

/referrals/{id}/approve

Approve Referral

PATCH

/referrals/{id}/reject

Reject Referral

GET

/referrals/current-interns

Current Interns

GET

/referrals/statistics

Dashboard Statistics

--------------------------------------------------

AUDIT LOGGING

Log

Referral Created

Invitation Sent

Intern Registered

Employee Approved

Employee Rejected

Email Sent

Notification Sent

Status Updated

Never skip audit logging.

--------------------------------------------------

EDGE CASES

Duplicate email

Duplicate referral

Expired invitation

Already registered intern

Intern using @agilisium.com email

Employee deleting referral

Employee changing department

Intern registering twice

Invitation already accepted

Referral cancelled

All edge cases must be handled gracefully.

--------------------------------------------------

ACCEPTANCE CRITERIA

✓ Employee can register using only @agilisium.com

✓ Employee can log in securely

✓ Employee can create referral

✓ Referral email sent

✓ Invitation token generated

✓ Intern registers

✓ Employee approval required

✓ Intern account created only after approval

✓ Dashboard updates automatically

✓ Notifications generated

✓ Audit logs created

✓ Search/filter/sort work

✓ Referral timeline works

✓ Everything remains fully integrated

Employee Module is complete only after every workflow functions end-to-end.

# PART 4 — ADMIN MODULE & MAIN ADMIN MODULE

The Admin Module is responsible for managing the recruitment lifecycle after an intern has been approved by the referring employee.

Admins review intern profiles, approve or reject applications, manage offer letters, monitor internship progress, publish company resources, create announcements, and oversee intern activities.

Main Admin has complete control over the platform, including administrative users, global settings, analytics, and system-wide configurations.

---

# ADMIN LOGIN

Admins authenticate using their official Agilisium email.

Requirements

• Email must end with @agilisium.com

• Password Login

• OTP Login (Future Ready)

• Forgot Password

• Reset Password

• Secure Session

• JWT

• Middleware Protection

Reject every login attempt using a non-Agilisium email.

---

# ADMIN SIDEBAR

Dashboard

Intern Applications

Pending Reviews

Offer Management

Internships

Employees

Company Problem Statements

Resources

Announcements

Reports

Notifications

Profile

Settings

Logout

---

# ADMIN DASHBOARD

The dashboard should provide a complete overview of the recruitment pipeline.

Display cards

Pending Employee Approved Interns

Profiles Awaiting Review

Offers Pending Upload

Offers Sent

Offers Accepted

Offers Rejected

Active Internships

Completed Internships

Current Attendance %

Total Active Interns

Recent Activities

Notifications

Quick Actions

Charts

Applications per Month

Department Distribution

College Distribution

Offer Acceptance Rate

Internship Completion Rate

Attendance Overview

Project Progress

All widgets should support clicking to navigate to the relevant page.

---

# PENDING REVIEWS PAGE

Display every intern awaiting administrative review.

Columns

Profile Photo

Name

College

Degree

Department

Preferred Role

Employee Referrer

Registration Date

Profile Completion %

Current Status

Actions

View

Approve

Reject

Request Changes

Support

Search

Filtering

Sorting

Pagination

---

# INTERN PROFILE REVIEW

Admin opens intern profile.

Sections

Personal Details

Academic Details

Skills

Resume

Portfolio

LinkedIn

GitHub

Employee Notes

Referral Timeline

Profile Completion

Audit History

Attachments

Buttons

Approve

Reject

Request Changes

---

# PROFILE VALIDATION

Before approval verify

Required fields completed

Resume uploaded

Profile completion = 100%

Valid email

Referral approved

No duplicate intern

If validation fails

Show validation summary

Prevent approval

---

# REQUEST CHANGES

Instead of rejecting immediately

Admin can request profile modifications.

Fields

Reason

Required Changes

Deadline

Upon submission

Send notification

Send email

Profile returns to intern

Intern edits profile

Resubmits

Admin notified

---

# APPROVE APPLICATION

Upon approval

Update Referral Status

Create Approval Record

Generate Offer Record

Create Notification

Send Approval Email

Audit Log

Status Timeline Update

Dashboard Statistics Update

Everything inside one transaction.

---

# REJECT APPLICATION

Reject reason mandatory.

Minimum

20 characters.

Workflow

Reject

↓

Reason

↓

Confirmation

↓

Update Referral

↓

Notify Employee

↓

Notify Intern

↓

Audit Log

↓

Dashboard Update

Referral becomes closed.

---

# OFFER MANAGEMENT

Only approved interns appear here.

Columns

Intern

Department

Offer Status

Offer Uploaded

Offer Sent

Offer Accepted

Offer Rejected

Joining Date

Actions

Upload

Replace

Preview

Download

Resend

---

# OFFER LETTER UPLOAD

Upload

PDF only

Maximum size configurable.

Store securely.

Version history supported.

Replacing an offer should archive previous versions.

---

# SEND OFFER

After upload

Admin clicks

Send Offer

Automatically

Generate secure offer link

Send email

Portal notification

Audit Log

Timeline update

Dashboard update

Offer Status

Offer Sent

SMTP queue should be used.

Never send synchronously.

---

# OFFER ACCEPTANCE

Intern receives

Email

↓

Clicks secure link

↓

Views offer

↓

Accept

OR

Reject

Accept

↓

Internship Activated

Reject

↓

Status Updated

↓

Admin Notification

↓

Employee Notification

---

# INTERNSHIPS PAGE

Shows every active internship.

Columns

Intern

Employee Referrer

Department

Current Project

Attendance %

Current Progress

Joining Date

Completion Date

Current Status

Actions

View

Project

Attendance

Timeline

Reports

---

# EMPLOYEE DIRECTORY

Admins can search employees.

View

Department

Designation

Referrals

Active Interns

Completed Internships

Contact Information

Admins cannot modify employee accounts unless authorized by Main Admin.

---

# COMPANY PROBLEM STATEMENTS

Admins manage organization-wide projects.

Fields

Title

Department

Business Problem

Detailed Description

Expected Outcome

Required Skills

Difficulty

Preferred Tech Stack

Estimated Duration

Mentor

Status

Attachments

Actions

Create

Edit

Archive

Delete

Assign

Interns browse these inside Internship Workspace.

---

# RESOURCES

Admins upload learning material.

Categories

Company Policies

Coding Standards

Architecture

Videos

Documentation

Reference Material

Training

Each resource

Title

Description

Category

Attachment

Visibility

Created Date

Download Count

---

# ANNOUNCEMENTS

Admins publish announcements.

Fields

Title

Description

Priority

Publish Date

Expiry Date

Attachments

Audience

Support

Draft

Scheduled

Published

Expired

Pinned

Interns receive

Portal notification

Email notification

---

# REPORTS

Generate reports.

Referral Report

Employee Report

College Report

Department Report

Intern Report

Attendance Report

Offer Report

Completion Report

Support

CSV

Excel

PDF

---

# ADMIN NOTIFICATIONS

Receive notifications when

Intern registers

Employee approves referral

Intern submits profile

Offer accepted

Offer rejected

Attendance flagged

Project overdue

Daily report missed

Announcement published

---

# ADMIN PROFILE

Fields

Name

Department

Designation

Official Email

Phone

Profile Picture

Password

Notification Preferences

Theme

Security Settings

---

# MAIN ADMIN

Main Admin inherits all Admin permissions.

Additionally

Manage Admin Users

Create Admin

Deactivate Admin

Reset Password

Assign Departments

Manage Employees

View System Logs

Manage Roles

Manage Platform Configuration

Manage SMTP

Manage Storage

Manage Environment Settings (where applicable)

View Audit Logs

View Security Logs

Manage Global Templates

Manage Email Templates

Manage Internship Template

Manage Report Template

Manage Notification Templates

---

# SYSTEM ANALYTICS

Main Admin Dashboard

Display

Total Employees

Total Interns

Pending Referrals

Pending Reviews

Offers Sent

Offers Accepted

Active Internships

Completed Internships

Attendance %

Average Project Progress

Storage Usage

Email Delivery Statistics

Daily Active Users

Monthly Active Users

Most Active Departments

Most Referred Colleges

Charts

Monthly Referrals

Internship Growth

Department Distribution

College Distribution

Offer Funnel

Attendance Trend

Project Completion Trend

---

# EMAIL TEMPLATE MANAGEMENT

Main Admin manages reusable templates.

Templates

Referral Invitation

Employee Approval

Profile Review

Request Changes

Offer Letter

Offer Accepted

Offer Rejected

Internship Welcome

Attendance Reminder

Announcement

Certificate Ready

Support

Preview

Versioning

Variables

Test Email

---

# DOCUMENT TEMPLATE MANAGEMENT

The repository contains a default internship report template.

Main Admin should be able to

Replace

Preview

Download

Archive

Restore

Every intern automatically receives the latest active version.

Never hardcode document templates.

---

# AUDIT LOGS

Every important action must be recorded.

Examples

Login

Logout

Referral Created

Referral Approved

Intern Registered

Offer Uploaded

Offer Sent

Offer Accepted

Attendance Edited

Project Updated

Announcement Published

Template Changed

Admin Created

Settings Changed

Audit logs should be searchable.

Support

Filtering

Export

Pagination

---

# API ENDPOINTS

GET

/admin/dashboard

GET

/admin/reviews

PATCH

/admin/reviews/{id}/approve

PATCH

/admin/reviews/{id}/reject

PATCH

/admin/reviews/{id}/request-changes

POST

/admin/offers/upload

POST

/admin/offers/send

GET

/admin/internships

GET

/admin/employees

GET

/admin/problem-statements

POST

/admin/problem-statements

PATCH

/admin/problem-statements/{id}

DELETE

/admin/problem-statements/{id}

GET

/admin/resources

POST

/admin/resources

GET

/admin/reports

GET

/admin/analytics

GET

/main-admin/system

POST

/main-admin/admins

PATCH

/main-admin/admins/{id}

DELETE

/main-admin/admins/{id}

---

# EDGE CASES

Prevent duplicate offer uploads.

Prevent approval if profile is incomplete.

Prevent sending offers without uploaded PDF.

Prevent deleting active announcements.

Prevent deleting active problem statements.

Prevent editing archived templates.

Prevent duplicate admin accounts.

Prevent unauthorized role escalation.

---

# ACCEPTANCE CRITERIA

✓ Admin can review every employee-approved intern.

✓ Admin can request profile changes.

✓ Admin can approve or reject applications.

✓ Offer letters can be uploaded, versioned, previewed, and resent.

✓ SMTP emails are queued and delivered correctly.

✓ Notifications are generated for every workflow.

✓ Company Problem Statements, Resources, and Announcements are fully manageable.

✓ Reports and analytics are available.

✓ Main Admin has complete platform control with proper RBAC.

✓ Every action creates audit logs and updates dashboard statistics.

The Admin Module is complete only when the entire recruitment and offer lifecycle functions seamlessly end-to-end.

# PART 5 — INTERN MODULE & INTERNSHIP WORKSPACE

The Internship Workspace is automatically created ONLY after an intern accepts their offer letter.

Interns must NEVER be able to manually activate their internship.

The activation flow is strictly controlled.

Employee Referral

↓

Employee Approval

↓

Admin Review

↓

Offer Uploaded

↓

Offer Sent

↓

Intern Accepts Offer

↓

Internship Activated

↓

Internship Workspace Created

↓

Welcome Email Sent

↓

Intern Begins Internship

--------------------------------------------------

# AUTOMATIC ACTIVATION

When the intern clicks "Accept Offer"

The backend must automatically:

• Update Offer Status

• Update Referral Status

• Create Internship record

• Initialize Internship Workspace

• Initialize Attendance module

• Initialize Project module

• Initialize Notifications

• Initialize Documentation

• Initialize Deliverables

• Initialize Timeline

• Generate Audit Logs

• Send Welcome Email (SMTP Queue)

Everything must execute inside a database transaction.

--------------------------------------------------

# INTERNSHIP WELCOME EMAIL

Immediately after activation

Automatically send email.

Email should include

Congratulations

Internship Start Date

Joining Instructions

Portal Link

Attendance Instructions

Project Instructions

Internship Documentation Instructions

Support Contact

Resources

The email must be generated from reusable templates.

Never hardcode templates.

--------------------------------------------------

# INTERNSHIP DASHBOARD

This becomes the intern's home page.

Dashboard should contain

Welcome Banner

Internship Status

Remaining Internship Days

Current Week

Attendance Percentage

Project Progress

Documentation Progress

Pending Deliverables

Assigned Department

Assigned Mentor (Future Ready)

Recent Activity

Announcements

Notifications

Upcoming Deadlines

Quick Actions

Resume Profile Completion

Profile Card

--------------------------------------------------

# SIDEBAR

Dashboard

Attendance

Daily Work Log

Project

Company Problem Statements

Documentation

Deliverables

Resources

Announcements

Timeline

Notifications

Profile

Settings

Logout

--------------------------------------------------

# PROFILE

Intern profile should contain

Personal Information

Academic Information

Skills

Resume

LinkedIn

GitHub

Portfolio

Emergency Contact

Current Address

Preferred Technologies

Biography

Profile Completion

Admins can view.

Interns can edit allowed fields.

--------------------------------------------------

# DOCUMENTATION PAGE

The repository contains

Default Internship Report Template

The system should automatically detect this template.

Interns should be able to

Preview

Download

Upload Updated Version

View Version History

Replace Latest Submission

Each upload should create a new version.

Never overwrite previous versions.

Admins can review every submission.

--------------------------------------------------

# PROJECT MODULE

Every intern must maintain a project.

Fields

Project Title

Problem Statement

Project Description

Objectives

Expected Outcome

Business Value

Technology Stack

Repository URL

Documentation URL

Presentation URL

Current Progress

Current Status

Start Date

Expected Completion

Attachments

Remarks

Intern updates project regularly.

Admins monitor progress.

--------------------------------------------------

# COMPANY PROBLEM STATEMENTS

Dedicated page.

Admins publish available company use cases.

Each problem statement should display

Title

Department

Business Problem

Detailed Description

Expected Deliverables

Required Skills

Preferred Tech Stack

Difficulty

Mentor

Estimated Duration

Current Status

Attachments

Intern can

Search

Filter

Bookmark

View Details

Request Assignment

If not already assigned a project,

intern may request one of these.

Admins approve assignment.

--------------------------------------------------

# DAILY ATTENDANCE

Attendance is mandatory.

Interns submit attendance every working day.

Table columns

Date

Check-In Time

Check-Out Time

Hours Worked

Attendance Status

Work Summary

Learning Summary

Challenges

Tomorrow's Plan

Admin Remarks

Submission Status

Attendance should calculate

Working Hours

Weekly Hours

Monthly Hours

Attendance Percentage

Attendance Streak

Late Entries

Missed Entries

Admins can review attendance.

--------------------------------------------------

# DAILY WORK LOG

Separate from attendance.

Intern submits

Title

Tasks Completed

Features Developed

Learning

Challenges

Blockers

Tomorrow Plan

GitHub Repository

Commit Links

Attachments

Screenshots

Documentation Links

Each submission

Timestamped

Versioned

Searchable

Editable before review

Locked after approval

--------------------------------------------------

# PROJECT PROGRESS

Visual progress tracker.

Status

Not Started

Planning

Development

Testing

Review

Completed

Display

Progress Bar

Milestones

Completed Tasks

Remaining Tasks

Estimated Completion

Recent Updates

--------------------------------------------------

# DELIVERABLES

Intern uploads

Source Code

Presentation

Documentation

Demo Video

Research

Architecture

Testing Report

Final Report

Each deliverable

Supports Version History

Preview

Download

Comments

Approval Status

Submission Date

--------------------------------------------------

# TIMELINE

Automatically generated.

Display

Offer Accepted

↓

Internship Started

↓

Week 1

↓

Week 2

↓

Project Started

↓

Mid Review

↓

Project Completed

↓

Final Report

↓

Internship Completed

Timeline updates automatically.

--------------------------------------------------

# RESOURCES

Admins upload

Training Videos

Company Policies

Coding Standards

Architecture Guides

Reference Material

Documentation

Templates

Interns can

View

Download

Bookmark

Search

--------------------------------------------------

# ANNOUNCEMENTS

Admins publish

Company Updates

Holiday Notices

Meeting Invitations

Deadlines

Training Sessions

Interns can

View

Filter

Mark Read

Bookmark

Receive Notifications

--------------------------------------------------

# NOTIFICATIONS

Notification Center

Display

Unread

Read

Priority

Recent

Archived

Support

Search

Filtering

Mark Read

Mark All Read

Delete

--------------------------------------------------

# SETTINGS

Intern can configure

Theme

Profile Picture

Password

Notification Preferences

Email Preferences

Language (Future)

Accessibility Options

--------------------------------------------------

# SEARCH

Every page should support

Search

Filtering

Sorting

Pagination

Server-side implementation preferred.

--------------------------------------------------

# APIs

GET

/intern/dashboard

GET

/intern/profile

PATCH

/intern/profile

GET

/intern/attendance

POST

/intern/attendance

PATCH

/intern/attendance/{id}

GET

/intern/worklogs

POST

/intern/worklogs

GET

/intern/project

PATCH

/intern/project

GET

/intern/problem-statements

POST

/intern/problem-statements/request

GET

/intern/documentation

POST

/intern/documentation

GET

/intern/resources

GET

/intern/announcements

GET

/intern/timeline

GET

/intern/notifications

PATCH

/intern/notifications/{id}

--------------------------------------------------

# EDGE CASES

Prevent attendance for future dates.

Prevent duplicate attendance for same day.

Prevent duplicate work logs.

Prevent editing approved submissions.

Prevent deleting approved deliverables.

Prevent project progress exceeding 100%.

Prevent uploads beyond configured size.

Handle internship completion gracefully.

Handle inactive internships.

Handle archived resources.

--------------------------------------------------

# ACCEPTANCE CRITERIA

✓ Internship Workspace is automatically created after offer acceptance.

✓ Welcome email is sent automatically.

✓ Dashboard displays internship overview.

✓ Attendance system works end-to-end.

✓ Daily Work Logs support versioning and review.

✓ Project management is fully functional.

✓ Company Problem Statements are searchable and assignable.

✓ Documentation template is automatically available.

✓ Deliverables support uploads, comments, and approvals.

✓ Timeline updates automatically throughout the internship.

✓ Resources and announcements are fully integrated.

✓ Notifications work across all internship activities.

✓ All APIs, permissions, validations, audit logs, and database updates are fully integrated.

The Intern Module is complete only when an intern can successfully complete their entire internship journey using the portal from onboarding to completion.

# PART 6 — EMAILS, NOTIFICATIONS, FILE MANAGEMENT, REPORTS & ANALYTICS

These modules are shared across the entire application.

Every module should reuse these services.

Never duplicate implementations.

All emails, notifications, uploads, reports and analytics should use centralized services.

--------------------------------------------------

# EMAIL INFRASTRUCTURE

Implement a centralized Email Service.

Never send emails directly from controllers or pages.

All email requests should be queued.

Recommended

BullMQ

Redis

SMTP

Queue Workers

Retry Logic

Delivery Tracking

Dead Letter Queue

--------------------------------------------------

# EMAIL TEMPLATES

Create reusable HTML email templates.

Templates include

Employee OTP

Password Reset

Referral Invitation

Referral Registered

Employee Approval Required

Employee Approved Referral

Employee Rejected Referral

Profile Submitted

Admin Requested Changes

Admin Approved Profile

Admin Rejected Profile

Offer Letter

Offer Reminder

Offer Accepted

Offer Rejected

Internship Activated

Internship Welcome

Attendance Reminder

Daily Log Reminder

Weekly Reminder

Monthly Reminder

Announcement

Internship Completion

Certificate Ready

General Notification

All templates should support placeholders.

Example

{{internName}}

{{employeeName}}

{{department}}

{{joiningDate}}

{{offerLink}}

{{companyName}}

Never hardcode values.

--------------------------------------------------

# SMTP

SMTP configuration should be managed by Main Admin.

Configuration

Host

Port

Username

Password

Encryption

Sender Name

Reply-To

Test Connection

Allow administrators to send a test email.

--------------------------------------------------

# EMAIL DELIVERY

Every email should create an EmailLog.

Track

Recipient

Template

Status

Attempts

Failure Reason

Sent Time

Delivered Time

Retry Count

Admins should be able to view email history.

--------------------------------------------------

# IN-APP NOTIFICATIONS

Create a centralized notification service.

Notification Types

Success

Info

Warning

Error

System

Reminder

Announcement

Workflow

Notification should support

Title

Description

Related Entity

Action URL

Priority

Read Status

Created Date

Expiry Date

--------------------------------------------------

# WHEN TO CREATE NOTIFICATIONS

Employee

Intern Registered

Approval Required

Offer Accepted

Offer Rejected

Internship Started

Internship Completed

Admin

Profile Submitted

Offer Accepted

Attendance Missing

Project Overdue

Announcement Published

Main Admin

Admin Created

Storage Warning

SMTP Failure

Audit Alerts

Intern

Referral Invitation

Employee Approved

Request Changes

Offer Sent

Offer Reminder

Internship Started

Attendance Reminder

Project Reminder

Announcement

Documentation Reminder

Certificate Ready

--------------------------------------------------

# NOTIFICATION CENTER

Every user role has Notification Center.

Features

Unread Count

Mark Read

Mark All Read

Delete

Archive

Search

Filter

Pagination

Notification Badge

Priority Indicator

--------------------------------------------------

# FILE MANAGEMENT

Create centralized File Service.

Support

Resume

Offer Letter

Documentation

Deliverables

Presentations

Videos

Certificates

Resources

Templates

--------------------------------------------------

# STORAGE

Abstract storage layer.

Support future providers.

Examples

Local

AWS S3

Azure Blob

Cloudflare R2

MinIO

Never tightly couple implementation.

--------------------------------------------------

# FILE VALIDATION

Validate

File Type

Maximum Size

Virus Scan Hook

Unique Filename

Safe Filename

Storage Path

Generate secure download URLs.

--------------------------------------------------

# FILE VERSIONING

Support version history for

Offer Letters

Internship Reports

Deliverables

Documentation

Templates

Never overwrite files.

Archive previous versions.

--------------------------------------------------

# REPORTS

Generate reports automatically.

Reports

Referral Report

Employee Performance

Intern Report

Attendance Report

Project Progress

Offer Report

Internship Completion

Department Report

College Report

Resource Usage

Announcement Reach

Email Delivery

System Audit

--------------------------------------------------

# EXPORTS

Every report should support

CSV

Excel

PDF

Exports should respect filters.

--------------------------------------------------

# DASHBOARD ANALYTICS

Employee Dashboard

Referral Count

Pending Approvals

Active Interns

Completed Internships

--------------------------------------------------

Admin Dashboard

Pending Reviews

Offer Funnel

Internships

Attendance

Projects

Resources

Announcements

--------------------------------------------------

Main Admin Dashboard

Total Employees

Total Admins

Total Interns

Monthly Referrals

Offer Conversion

Internship Completion

Storage Usage

Email Delivery

System Health

Database Health

--------------------------------------------------

Intern Dashboard

Attendance

Project Progress

Remaining Days

Pending Deliverables

Announcements

Resources

Notifications

--------------------------------------------------

# SEARCH

Every data table should support

Global Search

Filtering

Sorting

Pagination

Column Visibility

Export

Saved Filters (future ready)

--------------------------------------------------

# GLOBAL SEARCH

Implement global search.

Search across

Employees

Interns

Projects

Referrals

Announcements

Resources

Reports

Deliverables

Documentation

Only return records user has permission to access.

--------------------------------------------------

# DOCUMENT MANAGEMENT

Repository contains

Default Internship Report Template

Automatically detect template.

Display

Preview

Download

Current Version

Version History

Admins

Replace Template

Archive Template

Restore Previous Version

Interns always receive latest active template.

--------------------------------------------------

# CERTIFICATES

Future-ready architecture.

Prepare module for

Internship Completion Certificate

Certificate Number

Issue Date

Verification URL

Digital Signature

Not implemented yet

but database and services should be future-ready.

--------------------------------------------------

# LOGGING

Centralized Logger

Log

Authentication

API Requests

Email

Notifications

Uploads

Downloads

Attendance

Projects

Reports

Errors

Performance

Do not expose logs to end users.

--------------------------------------------------

# API ENDPOINTS

GET

/notifications

PATCH

/notifications/{id}

PATCH

/notifications/read-all

DELETE

/notifications/{id}

GET

/resources

GET

/announcements

GET

/reports

GET

/analytics

GET

/files/{id}

POST

/files/upload

DELETE

/files/{id}

GET

/templates

PATCH

/templates

POST

/emails/test

GET

/emails/logs

--------------------------------------------------

# EDGE CASES

Handle failed SMTP gracefully.

Retry failed emails.

Prevent duplicate notifications.

Prevent invalid file uploads.

Prevent oversized files.

Prevent unsupported file formats.

Prevent downloading unauthorized files.

Handle deleted resources.

Handle archived templates.

Handle expired announcements.

Handle broken download links.

--------------------------------------------------

# ACCEPTANCE CRITERIA

✓ Email service is centralized and queue-based.

✓ SMTP configuration is manageable.

✓ All workflows generate emails automatically.

✓ Notification Center works for every role.

✓ File uploads support validation and versioning.

✓ Reports can be exported.

✓ Analytics dashboards update automatically.

✓ Global search works with RBAC.

✓ Internship report template is managed through the portal.

✓ Logging and audit services are centralized.

All shared infrastructure should be reusable across every module of the application.

# PART 7 — SECURITY, PERFORMANCE, TESTING, DEVOPS & PRODUCTION READINESS

The application should be built as production-ready enterprise software.

Security, performance and maintainability are mandatory.

Never sacrifice security for convenience.

Every implementation should be scalable enough to support thousands of interns, employees and administrators.

--------------------------------------------------

# SECURITY

Implement security at every layer.

Frontend

↓

Middleware

↓

API

↓

Business Layer

↓

Database

Never rely on frontend validation.

--------------------------------------------------

# AUTHENTICATION SECURITY

Use Auth.js (NextAuth v5).

Support

JWT

Secure Cookies

HTTP Only Cookies

SameSite Protection

Session Expiry

Session Refresh

Device-aware Sessions (Future Ready)

Remember Me

Logout Everywhere (Future Ready)

--------------------------------------------------

# PASSWORD SECURITY

Passwords must

Never be stored in plaintext.

Use bcrypt.

Minimum Requirements

• Minimum 8 characters

• Uppercase

• Lowercase

• Number

• Special Character

Prevent

Common passwords

Previous password reuse (future ready)

Weak passwords

--------------------------------------------------

# OTP SECURITY

OTP should

Expire automatically

Maximum Attempts

Rate Limited

Single Use

Encrypted Storage

Automatic Cleanup

Never expose OTPs in logs.

--------------------------------------------------

# RATE LIMITING

Implement rate limiting.

Protect

Login

OTP

Forgot Password

Referral Creation

Registration

Offer Acceptance

Attendance Submission

Work Log Submission

File Upload

Notification APIs

Email APIs

Prevent brute-force attacks.

--------------------------------------------------

# INPUT VALIDATION

Every request must validate

Body

Query

Headers

Params

Files

Never trust client input.

Use Zod validation.

Reject invalid requests immediately.

--------------------------------------------------

# XSS PROTECTION

Sanitize all rich text.

Escape HTML.

Validate Markdown.

Never render unsafe HTML.

--------------------------------------------------

# SQL INJECTION

Never build raw SQL.

Always use Prisma ORM.

Parameterized queries only.

--------------------------------------------------

# CSRF

Protect all authenticated requests.

Validate CSRF tokens.

--------------------------------------------------

# FILE SECURITY

Every upload must validate

Type

Size

Extension

Content Type

Virus Scan Hook

Safe Filename

Secure Storage

Generate random filenames.

Never trust original filename.

--------------------------------------------------

# AUTHORIZATION

RBAC must be enforced

Frontend

Backend

Middleware

Services

API

Never expose unauthorized resources.

Every API must verify ownership.

--------------------------------------------------

# AUDIT LOGGING

Log

Authentication

Role Changes

Offer Upload

Attendance

Project Updates

Announcements

Templates

Resource Uploads

Report Downloads

Configuration Changes

Never allow audit logs to be deleted.

--------------------------------------------------

# PERFORMANCE

Optimize for

Fast initial load

Low server response

Minimal bundle size

Efficient database queries

--------------------------------------------------

# DATABASE PERFORMANCE

Use

Indexes

Relations

Pagination

Selective Queries

Avoid N+1 queries.

Avoid unnecessary joins.

Use transactions where appropriate.

--------------------------------------------------

# FRONTEND PERFORMANCE

Use

Server Components

Streaming

Suspense

Lazy Loading

Dynamic Imports

Memoization

Optimized Images

Code Splitting

Skeleton Loaders

--------------------------------------------------

# API PERFORMANCE

Return only required fields.

Support

Pagination

Filtering

Sorting

Search

Never return unnecessary data.

--------------------------------------------------

# CACHING

Use caching where appropriate.

Dashboard Statistics

Problem Statements

Resources

Announcements

Reports

Do not cache user-sensitive data incorrectly.

Invalidate cache after updates.

--------------------------------------------------

# BACKGROUND JOBS

Use queues for

Emails

Notifications

Report Generation

Analytics

Large Imports

Future Certificate Generation

Never block user requests.

--------------------------------------------------

# ERROR HANDLING

Create centralized error handling.

Never expose stack traces.

Return meaningful errors.

Log complete exception details internally.

Support

Validation Errors

Authentication Errors

Authorization Errors

Business Errors

Database Errors

Unexpected Errors

--------------------------------------------------

# LOADING STATES

Every async page should include

Skeleton Loading

Spinner (where appropriate)

Optimistic Updates

Retry Actions

--------------------------------------------------

# EMPTY STATES

Every table should display meaningful empty states.

Examples

No Referrals

No Notifications

No Attendance

No Reports

No Announcements

Provide clear next actions.

--------------------------------------------------

# ACCESSIBILITY

Support

Keyboard Navigation

Focus Management

ARIA Labels

Semantic HTML

Accessible Forms

High Contrast Compatibility

Responsive Layouts

--------------------------------------------------

# RESPONSIVENESS

Support

Desktop

Laptop

Tablet

Mobile

All dashboards should remain usable across screen sizes.

--------------------------------------------------

# TESTING

Implement

Unit Tests

Integration Tests

API Tests

Component Tests

Playwright End-to-End Tests

--------------------------------------------------

# UNIT TESTS

Test

Services

Utilities

Validation

Business Logic

Repositories

--------------------------------------------------

# INTEGRATION TESTS

Authentication

Referral Workflow

Offer Workflow

Attendance

Projects

Notifications

Emails

Reports

--------------------------------------------------

# END-TO-END TESTS

Employee Registration

Employee Login

Create Referral

Intern Registration

Employee Approval

Intern Profile Completion

Admin Approval

Offer Upload

Offer Acceptance

Internship Activation

Attendance Submission

Project Update

Report Upload

Logout

--------------------------------------------------

# SEED DATA

Generate realistic seed data.

Employees

Admins

Main Admin

Interns

Referrals

Projects

Attendance

Announcements

Resources

Reports

Use meaningful fake data.

--------------------------------------------------

# LOGGING

Centralize logging.

Support

Info

Warning

Error

Critical

Debug (Development)

--------------------------------------------------

# MONITORING

Architecture should be ready for

Sentry

OpenTelemetry

Prometheus

Grafana

Health Checks

Application Metrics

Future integration should require minimal code changes.

--------------------------------------------------

# HEALTH CHECKS

Implement

Application Health

Database Health

SMTP Health

Storage Health

Redis Health

Queue Health

Return structured health status.

--------------------------------------------------

# DEVOPS

Prepare project for

Docker

Docker Compose

Production Deployment

Environment Variables

CI/CD

--------------------------------------------------

# ENVIRONMENT VARIABLES

Validate all required variables during startup.

Application should fail fast if configuration is missing.

Separate

Development

Staging

Production

--------------------------------------------------

# DOCKER

Prepare

Dockerfile

docker-compose.yml

Development Containers

Health Checks

Volume Mounts

Environment Variables

--------------------------------------------------

# CI/CD

Prepare workflows for

Lint

Type Check

Tests

Build

Prisma Migration Check

Deployment

Do not deploy if tests fail.

--------------------------------------------------

# CODE QUALITY

Every implementation must

Pass TypeScript

Pass ESLint

Avoid duplicate code

Avoid dead code

Avoid unused imports

Avoid console.log in production

--------------------------------------------------

# DOCUMENTATION

Generate

README

API Documentation

Setup Guide

Deployment Guide

Environment Guide

Folder Structure

Developer Guide

Contributing Guide

Architecture Guide

--------------------------------------------------

# FUTURE READY

Architecture should support future modules without major refactoring.

Examples

Mentor Portal

HR Portal

Certificate Generation

AI Resume Analysis

AI Performance Evaluation

Campus Recruitment

Placement Tracking

Employee Feedback

Mentor Feedback

Alumni Portal

Company LMS Integration

Calendar Integration

Microsoft Teams Integration

Slack Integration

AI Chat Assistant

--------------------------------------------------

# IMPLEMENTATION ORDER

Every feature should follow this order.

1.

Understand existing implementation.

2.

Identify affected files.

3.

Update Database (if required).

4.

Update Validation.

5.

Update Services.

6.

Update APIs.

7.

Update Frontend.

8.

Update Notifications.

9.

Update Emails.

10.

Update Audit Logs.

11.

Update Tests.

12.

Verify Build.

Never implement only the UI.

Never implement only the backend.

Every feature should be complete before moving forward.

--------------------------------------------------

# FINAL PRODUCTION CHECKLIST

Before considering Phase 1 + Phase 2 complete, verify:

✓ Zero TypeScript errors

✓ Zero ESLint errors

✓ All pages functional

✓ All APIs authenticated

✓ RBAC enforced

✓ Employee referral flow works end-to-end

✓ Employee approval flow works

✓ Intern account created only after employee approval

✓ Admin review works

✓ Offer management works

✓ Offer acceptance activates internship

✓ Internship Workspace is created automatically

✓ Attendance works

✓ Daily Work Logs work

✓ Project tracking works

✓ Company Problem Statements work

✓ Resources work

✓ Announcements work

✓ Deliverables work

✓ Documentation template works

✓ SMTP emails work

✓ Notifications work

✓ Reports export correctly

✓ Dashboard analytics update correctly

✓ File uploads validated

✓ Audit logs generated

✓ Search, filters and pagination work

✓ Responsive UI

✓ Dark Mode & Light Mode

✓ Security implemented

✓ Performance optimized

✓ Tests passing

✓ Project builds successfully

--------------------------------------------------

# COPILOT AGENT EXECUTION RULES

You are working inside an existing repository.

Before writing code:

Inspect the repository.

Understand existing implementations.

Reuse existing components.

Reuse services.

Reuse hooks.

Reuse utilities.

Never duplicate code.

Never regenerate existing files unnecessarily.

Modify existing files whenever appropriate.

Keep changes small and logically grouped.

Treat every response as a production-ready commit.

Do not stop at scaffolding.

Do not leave placeholders.

Do not leave TODO comments.

If a feature requires changes across multiple layers (database, services, API, frontend, notifications, emails), update all of them together.

The application should remain buildable after every implementation step.

Only consider a feature complete when it is fully integrated, tested, and production-ready.

# PART 8 — IMPLEMENTATION ROADMAP, DESIGN SYSTEM, DEFINITION OF DONE & COPILOT EXECUTION GUIDE

This is the final section of the implementation guide.

The goal is to ensure the application is implemented consistently, remains maintainable, and is production-ready.

Do not randomly implement pages.

Always follow the implementation order below.

--------------------------------------------------

# IMPLEMENTATION ROADMAP

Complete the application in the following order.

## Phase 0

Project Initialization

- Verify project builds successfully.
- Verify Prisma configuration.
- Verify Authentication.
- Verify SMTP.
- Verify Storage.
- Verify Environment Variables.
- Verify Database Connection.
- Verify Tailwind.
- Verify Theme.

Application should compile before adding features.

--------------------------------------------------

## Phase 1

Authentication

Implement

✓ Employee Registration

✓ Employee Login

✓ Admin Login

✓ Main Admin Login

✓ Intern Invitation Registration

✓ Password Reset

✓ OTP

✓ Middleware

✓ RBAC

✓ Sessions

Verify authentication completely before proceeding.

--------------------------------------------------

## Phase 2

Referral System

Implement

Employee Dashboard

Create Referral

Referral Timeline

Referral Status

Pending Approval

Employee Approval

Referral APIs

Referral Notifications

Referral Emails

Audit Logs

--------------------------------------------------

## Phase 3

Intern Registration

Implement

Invitation Link

Registration

Temporary Registration

Employee Approval

Intern Account Creation

Intern Login

Intern Profile

Resume Upload

Profile Completion

--------------------------------------------------

## Phase 4

Admin Module

Pending Reviews

Approve

Reject

Request Changes

Offer Upload

Offer Versioning

Offer Email

Offer Acceptance

--------------------------------------------------

## Phase 5

Internship Activation

Offer Accepted

↓

Create Internship

↓

Initialize Workspace

↓

Welcome Email

↓

Dashboard

↓

Timeline

↓

Attendance

↓

Project

↓

Documentation

--------------------------------------------------

## Phase 6

Intern Portal

Dashboard

Attendance

Daily Logs

Projects

Problem Statements

Documentation

Deliverables

Resources

Announcements

Notifications

Timeline

Settings

--------------------------------------------------

## Phase 7

Reports

Analytics

Search

Filtering

Export

Audit Logs

Email Logs

--------------------------------------------------

## Phase 8

Optimization

Caching

Performance

Accessibility

Testing

Deployment

Documentation

--------------------------------------------------

# DESIGN SYSTEM

The application should follow one consistent design language.

--------------------------------------------------

# DESIGN STYLE

Professional Enterprise SaaS

Minimal

Clean

Modern

Fast

Highly Readable

No visual clutter.

No excessive gradients.

No excessive shadows.

Animations should be subtle.

--------------------------------------------------

# DESIGN INSPIRATION

Use inspiration from

Linear

Notion

Vercel Dashboard

Ashby

Greenhouse

Rippling

Stripe Dashboard

GitHub

Microsoft Fluent

Do NOT copy.

Take inspiration only.

--------------------------------------------------

# COLOR SYSTEM

Primary

Use Agilisium-inspired branding colors based on the existing favicon/logo.

Do not invent unrelated branding.

Use a professional enterprise palette.

Status Colors

Success

Green

Error

Red

Warning

Amber

Information

Blue

Neutral

Gray

Status colors should remain consistent across every page.

--------------------------------------------------

# TYPOGRAPHY

Clear hierarchy.

Large page titles.

Readable body text.

Consistent spacing.

Avoid giant paragraphs.

Use strong visual hierarchy.

--------------------------------------------------

# SPACING

Maintain consistent spacing throughout.

Use an 8-point spacing system.

Avoid inconsistent margins.

--------------------------------------------------

# COMPONENT LIBRARY

Build reusable components.

Examples

Button

Input

Select

Checkbox

Radio

Textarea

Dialog

Modal

Drawer

Toast

Tooltip

Popover

Dropdown

Command Palette

Card

Stat Card

Data Table

Search Bar

Timeline

Progress Card

File Upload

Notification Card

Avatar

Breadcrumb

Pagination

Status Badge

Loading Skeleton

Empty State

Error State

Charts

Calendar

Date Picker

Every page should reuse these components.

Never duplicate UI.

--------------------------------------------------

# TABLE STANDARD

Every table should support

Sorting

Filtering

Searching

Pagination

Column Visibility

Responsive Design

Loading State

Empty State

Export

Consistent action menus.

--------------------------------------------------

# FORMS

Every form should support

Validation

Error Messages

Loading State

Success State

Auto Save (where appropriate)

File Upload

Responsive Layout

--------------------------------------------------

# DASHBOARDS

Every dashboard should contain

Summary Cards

Charts

Recent Activity

Notifications

Quick Actions

Timeline

Search

Widgets

Dashboard should never feel empty.

--------------------------------------------------

# LOADING EXPERIENCE

Every async page should have

Skeleton Loader

Progress Indicator

Retry Button

Meaningful Messages

--------------------------------------------------

# EMPTY STATES

Never display empty blank pages.

Examples

No Referrals Yet

Create your first referral.

No Attendance

Submit today's attendance.

No Projects

Create your project.

Always guide users.

--------------------------------------------------

# RESPONSIVENESS

Support

Desktop

Laptop

Tablet

Mobile

No broken layouts.

--------------------------------------------------

# ACCESSIBILITY

Keyboard Navigation

Screen Readers

Semantic HTML

ARIA Labels

Focus Indicators

Color Contrast

--------------------------------------------------

# BUILD QUALITY

Every feature should satisfy

✓ UI Complete

✓ Backend Complete

✓ Database Updated

✓ Validation Added

✓ Tests Added

✓ Emails Integrated

✓ Notifications Integrated

✓ Audit Logs Added

✓ RBAC Verified

✓ Responsive

✓ Accessible

✓ Production Ready

--------------------------------------------------

# FEATURE COMPLETION RULE

A feature is NOT complete until

Frontend works

Backend works

Database works

Emails work

Notifications work

Validation works

Audit Logs work

Permissions work

Tests pass

Build succeeds

Never stop after building only the UI.

--------------------------------------------------

# BEFORE CREATING NEW CODE

Always inspect existing repository.

Ask

Does this already exist?

Can this component be reused?

Can this service be extended?

Can this hook be reused?

Can this utility be reused?

Avoid duplication.

--------------------------------------------------

# BEFORE MODIFYING DATABASE

Whenever Prisma changes

Also update

Validation

Types

Repositories

Services

APIs

Frontend Types

Tests

Seed Data

Documentation

Never update Prisma alone.

--------------------------------------------------

# BEFORE CREATING A PAGE

Ensure

Route exists

Permission exists

Sidebar updated

Navigation updated

Breadcrumb added

Metadata added

SEO metadata added (where applicable)

Loading state exists

Error state exists

--------------------------------------------------

# BEFORE CREATING AN API

Ensure

Authentication

Authorization

Validation

Transactions

Logging

Error Handling

Consistent Responses

Pagination

Filtering

Documentation

--------------------------------------------------

# BEFORE CREATING EMAILS

Ensure

Template exists

Variables defined

Queue configured

SMTP configured

Retry Logic

Email Logs

--------------------------------------------------

# BEFORE CREATING FILE UPLOADS

Ensure

Validation

Storage

Versioning

Preview

Download

Delete

Permissions

Audit Logs

--------------------------------------------------

# BEFORE MERGING A FEATURE

Run

TypeScript

Lint

Unit Tests

Integration Tests

Playwright

Build

Prisma Validation

Environment Validation

Fix every issue.

--------------------------------------------------

# FINAL DEFINITION OF DONE

The project is complete only if

✓ Every authentication flow works.

✓ Employees register only with @agilisium.com.

✓ Admins register only with @agilisium.com.

✓ Main Admin registers only with @agilisium.com.

✓ Interns register only using referral invitations.

✓ Interns cannot use @agilisium.com emails.

✓ Intern accounts are created ONLY after employee approval.

✓ Referral workflow functions end-to-end.

✓ Admin approval workflow functions end-to-end.

✓ Offer workflow functions end-to-end.

✓ Internship activates automatically after offer acceptance.

✓ Internship Workspace is created automatically.

✓ Attendance works.

✓ Daily Work Logs work.

✓ Project Management works.

✓ Company Problem Statements work.

✓ Documentation Template is available and versioned.

✓ Deliverables work.

✓ Resources work.

✓ Announcements work.

✓ Reports work.

✓ Analytics work.

✓ Notifications work.

✓ Emails work.

✓ Dashboard widgets update automatically.

✓ Global Search works.

✓ Audit Logs are generated for every important action.

✓ File uploads are secure and versioned.

✓ APIs are documented and consistent.

✓ RBAC is enforced everywhere.

✓ Security best practices are implemented.

✓ Performance is optimized.

✓ Accessibility is maintained.

✓ Responsive design works.

✓ Dark Mode and Light Mode work correctly.

✓ Application builds successfully with zero TypeScript errors.

✓ Application passes linting.

✓ Database migrations run successfully.

✓ Seed data works.

✓ Production build succeeds.

--------------------------------------------------

# FINAL COPILOT EXECUTION INSTRUCTIONS

Treat this repository as if you are a senior software engineer joining an existing enterprise project.

Read the repository before making changes.

Read AIRP.md before implementing any feature.

Follow this IMPLEMENTATION_GUIDE.md throughout development.

Do not redesign the architecture unless absolutely necessary.

Prefer modifying existing files over creating duplicate implementations.

Implement features incrementally.

Keep each change cohesive and production-ready.

Maintain consistency in coding style, naming, validation, and UI.

Whenever a feature spans multiple layers (database, backend, frontend, notifications, emails, analytics), implement all affected layers together.

Never leave placeholder code, incomplete workflows, or TODOs.

Always leave the repository in a buildable, testable state.

The objective is not to generate code quickly—it is to deliver a polished, secure, scalable, enterprise-grade Agilisium Intern Portal that is ready for real-world deployment and future expansion.