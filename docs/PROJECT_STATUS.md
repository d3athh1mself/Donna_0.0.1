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
- First material catalog/supplier implementation slice completed:
  - Created SQLAlchemy models for `material_categories`, `manufacturers`, `brands`, `units_of_measure`, `products`, `product_variants`, `suppliers`, and `supplier_product_listings`.
  - Wired `app.models` into Alembic autogeneration through `backend/alembic/env.py`.
  - Created first Alembic migration: `da757d56fbd8_create_initial_catalog_supplier_tables.py`.
  - Applied migration `da757d56fbd8` to local PostgreSQL.
  - Verified all expected tables exist.
  - Verified Alembic version is `da757d56fbd8`.
  - Ran downgrade to base and upgrade back to head successfully.
  - Re-verified all expected tables after downgrade/upgrade.
- Approved unit-of-measure seed data applied to local PostgreSQL:
  - 69 UOM rows exist.
  - Verified key conversions: `PR = 2 EA`, `ROOF_SQ = 100 SQFT`, and `BF = 144 CUIN`.
  - Verified selected packaging/material-form units have no universal conversions.
  - Verified post-apply dry-run idempotency: 0 rows would be inserted and 69 existing rows were detected.

## Current Milestone

Approved unit-of-measure seed data has been applied and verified. The next milestone is frontend project setup.

## Current Database Migration State

- `da757d56fbd8 (head)` — create initial catalog supplier tables

## Remaining Milestones

- Build frontend project
- Build material catalog MVP
- Build receipt upload workflow
- Build human review workflow for receipt extraction
- Add price history
- Add reporting and exports
- Add OCR and AI-assisted extraction
- Verify backup workflow before real receipt entry

## Known Issues

- Receipt entry is not ready.
- Sample receipt testing is not ready.
- Real receipt entry is not ready.
- Receipt tables, receipt upload workflow, human review workflow, and backup verification are not implemented yet.
- Sample receipts must wait until the required catalog, supplier, receipt, review, storage, migration, duplicate-detection, and backup workflows exist.

## Deferred Features

- Live QuickBooks integration
- Database-backed company/profile settings with admin editing
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
- Material catalog schema design is complete as a planning document.
- The first approved catalog/supplier model and migration slice is implemented and verified locally.
- Unit-of-measure seed approach is reviewed and approved. The standalone seed script is implemented, applied locally, and verified idempotent after apply.
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
- Donna must not permanently hard-code `Denali Craft LLC` throughout the app. Early MVP may use app configuration for company display name, but later UI, reports, exports, documents, and headings should read company/profile branding from editable settings.

## Future Company/Profile Settings

- App name: `Donna`
- Legal company name example: `Denali Craft LLC`
- Display name example: `Denali Craft`
- Trade name / DBA: optional
- Early MVP can use app configuration for the company display name.
- Later, company/profile settings should be stored in the database and editable through an admin/settings screen.
- Future fields may include `legal_name`, `display_name`, `dba_name`, address fields, `phone`, `email`, `logo_file_path`, `timezone`, `is_active`, `created_at`, and `updated_at`.

## Pending Decisions

- Final production storage location
- Backup destination and schedule
- QuickBooks export format
- Network hostname and production port
- OCR provider configuration

## Latest Completed Implementation Checkpoint

053ed0b — Implement initial catalog supplier models and migration
