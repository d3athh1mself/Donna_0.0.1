# Denali Craft Operations Platform — Project Status

## Completed Milestones

- MVP requirements defined
- Development prerequisites installed and verified
- PostgreSQL installed and verified
- Local Git repository initialized
- GitHub private repository connected
- Base project folders created
- .gitignore created
- Environment-variable template created

## Current Milestone

Project foundation setup

## Remaining Milestones

- Create local storage structure
- Create project documentation
- Create backend project
- Configure PostgreSQL database
- Create material catalog schema
- Create frontend project
- Build material catalog MVP
- Add receipt uploads
- Add price history
- Add reporting and exports
- Add OCR and AI-assisted extraction

## Known Issues

None currently.

## Deferred Features

- Live QuickBooks integration
- Job management
- Full job costing
- Cloud storage
- Semantic/vector search
- Email integration
- Banking integration
- Payroll integration

## Architectural Decisions

- Backend: Python and FastAPI
- Database: PostgreSQL
- Frontend: React
- Phase 1 storage: Local file system
- Deployment: Local network
- Initial roles: Admin and User
- MVP priority: Material Catalog
- First document type: Receipts
- Documents may be uploaded before OCR is implemented
- AI-extracted data requires human approval
- Search will cover database records and document text
- Exports will be designed with QuickBooks compatibility in mind
- Storage paths will be configurable for redeployment
- Backup architecture will support external destinations

## Pending Decisions

- Final production storage location
- Backup destination and schedule
- QuickBooks export format
- Network hostname and production port
- OCR provider configuration

## Current Git Checkpoint

8f8c7a2 — Add FastAPI backend skeleton and health endpoint
