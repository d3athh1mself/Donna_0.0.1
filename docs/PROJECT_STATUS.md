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
- Material catalog schema design completed and consistency-reviewed in `docs/MATERIAL_CATALOG_SCHEMA.md`

## Current Milestone

Material catalog implementation planning

## Remaining Milestones

- Create local storage structure
- Create project documentation
- Create backend project
- Configure PostgreSQL database
- Plan material-catalog SQLAlchemy models and first Alembic migration
- Create frontend project
- Build material catalog MVP
- Add receipt uploads
- Add price history
- Add reporting and exports
- Add OCR and AI-assisted extraction

## Known Issues

- Receipt entry is not ready.
- Sample receipts must wait until the required catalog, supplier, receipt, review, storage, migration, duplicate-detection, and backup workflows exist.

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
- Material catalog schema design is complete as a planning document only; no SQLAlchemy catalog models, seed scripts, Alembic migrations, or database tables have been created from it.
- No unresolved material-catalog schema decisions remain.
- Material catalog categories support unlimited nesting, with three levels initially displayed in the MVP UI.
- Product variants do not require a Denali-created SKU.
- Donna supports multiple external identifiers and supplier-specific SKUs.
- Units of measure are comprehensive and user-manageable.
- Product variants may have multiple labeled dimension sets.
- Flexible specifications may apply at the product level, variant level, or both.
- Identifier uniqueness scopes are configurable and support audited exceptions.
- Receipt-driven price updates are conditional and include discount handling.
- Document records use relative local-storage keys under a configured storage root.
- Inactive records are hidden by default.
- Accounting export mappings and staging remain QuickBooks-neutral.
- After this documentation milestone is verified, committed, and pushed, start a new Codex conversation for implementation planning.

## Pending Decisions

- Final production storage location
- Backup destination and schedule
- QuickBooks export format
- Network hostname and production port
- OCR provider configuration

## Current Git Checkpoint

fea1d3d — Add database constraint naming convention
