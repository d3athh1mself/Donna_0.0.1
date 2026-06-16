# Donna — Denali Craft Operations Platform

Donna is the internal company database and operations platform for Denali Craft LLC.

This is an internal system, not a customer portal.

## MVP Objective

The first usable version will focus on:

- Material catalog management
- Supplier records
- Receipt uploads
- Receipt line-item review
- Material price history
- Database and document search
- Spending reports
- Monthly bills reports
- CSV and Excel exports

## Technology Stack

- Backend: Python and FastAPI
- Database: PostgreSQL
- Frontend: React
- File storage: Local file system
- Deployment: Local network
- Reports: CSV, Excel, and PDF
- OCR: OpenAI Vision with future Tesseract fallback
- Search: PostgreSQL full-text search

## Project Structure

- `backend/` — FastAPI application
- `frontend/` — React application
- `database/` — Database design and migration resources
- `docs/` — Project documentation and status
- `scripts/` — Setup, backup, restore, and maintenance scripts
- `storage/` — Local runtime documents, exports, temporary files, and backups
- `tests/` — Automated tests

## Security Principles

- No secrets committed to Git
- Passwords and API keys stored in environment variables
- Human approval required before saving AI-extracted data
- Local-network deployment with no direct internet exposure
- Admin and regular-user access levels

## Project Status

See:

`docs/PROJECT_STATUS.md`
