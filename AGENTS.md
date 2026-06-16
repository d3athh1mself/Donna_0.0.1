# Donna Agent Instructions

## Project

- Name: Donna -- Denali Craft Operations Platform
- Company: Denali Craft LLC
- Purpose: Local internal company database, document repository, reporting system, and operations platform.
- Donna is not a customer portal.

## Current Stack

- Windows
- PowerShell
- Python 3.13
- FastAPI
- PostgreSQL 17
- SQLAlchemy
- Alembic
- React
- Local file storage for Phase 1

## Security And Privacy

- Do not open, read, display, quote, modify, copy, or expose the `.env` file.
- Never display passwords, API keys, secret keys, tokens, credentials, or other secrets.
- Never hardcode secrets or credentials.
- Do not assume software, services, accounts, or credentials exist.
- Verify prerequisites before using them.
- Keep source documents local unless explicitly approved otherwise.
- Do not bypass CAPTCHAs, login restrictions, paywalls, anti-bot protections, or access controls.

## Working Rules

- Preserve the existing architecture and files.
- Use PowerShell for Windows commands.
- Work in small, reviewable increments.
- Explain what a command or change does before proposing it.
- Ask for explicit approval before installing or downloading software.
- Ask for explicit approval before deleting, overwriting, moving, or renaming existing files.
- Ask for explicit approval before modifying anything outside the repository.
- Do not create Git commits or push to GitHub unless explicitly requested.
- Recommend a Git checkpoint before high-risk changes.
- Run appropriate verification after changes.
- Stop and report errors instead of continuing past them.
- Keep core business logic separate from third-party integrations.
- Require human review before saving AI-extracted business data.
- Maintain `docs/PROJECT_STATUS.md` as the project develops.

## MVP Priority

- Material catalog
- Supplier records
- Receipt uploads before OCR
- Human-reviewed receipt extraction
- Price history
- Search
- Spending reports
- Monthly bills reports
- CSV and Excel exports
- QuickBooks-aware architecture without requiring live QuickBooks integration
