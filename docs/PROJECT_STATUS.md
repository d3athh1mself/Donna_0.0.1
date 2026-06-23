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

## Current Milestone

Approved unit-of-measure seed script implemented and dry-run/default mode verified. Unit seed data has not been loaded.

## Current Database Migration State

- `da757d56fbd8 (head)` — create initial catalog supplier tables

## Remaining Milestones

- Review and explicitly apply unit-of-measure seed data
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
- Unit-of-measure seed approach is reviewed and approved. The standalone seed script is implemented and dry-run/default mode is verified. Seed data has not been loaded.
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

## Pending Decisions

- Final production storage location
- Backup destination and schedule
- QuickBooks export format
- Network hostname and production port
- OCR provider configuration

## Latest Completed Implementation Checkpoint

053ed0b — Implement initial catalog supplier models and migration
