# Material Catalog Schema Proposal

## 1. Scope And Design Goals

This document proposes a normalized PostgreSQL-compatible database design for Donna's Material Catalog MVP. It is a planning document only and does not create a migration or modify the database.

Design goals:

- Separate general product identity from purchasable product variants.
- Keep supplier-specific SKU, price, product URL, and purchase unit off the general product table.
- Allow one product variant to be sold by multiple suppliers.
- Allow supplier listings to have different SKUs, prices, URLs, and units.
- Support receipt-driven historical prices, where every approved receipt line item can later create a price history record.
- Store flexible specifications without creating a new product table column for every attribute.
- Reference local documents by relative storage key under a configured local storage root instead of storing large files directly in PostgreSQL.
- Preserve a QuickBooks-aware export path without embedding QuickBooks-specific assumptions into core material catalog tables.
- Include active/inactive flags and audit timestamps on user-managed catalog records.
- Allow unlimited category nesting in the database while the MVP user interface initially displays three levels: Category, Subcategory, and Material Type.
- Use the internal database primary key as the authoritative product variant identity. This primary key is not intended to function as a user-facing SKU.
- Keep core catalog, supplier, receipt, pricing, and document tables QuickBooks-neutral. QuickBooks-aware exports use separate mapping and staging records, with live QuickBooks integration deferred.

Active/inactive behavior:

- Inactive records are hidden by default in normal lists, searches, selectors, lookup screens, and APIs.
- Users must use an explicit filter such as `Show inactive records` or `Include inactive` to display them.
- Inactive records remain available for historical receipts, historical price records, reports, existing relationships, auditing, and reactivation.
- Inactive records must not be deleted solely because they are no longer used.
- Inactive records must not be selectable for new transactions, new supplier listings, new receipt mappings, or other new operational relationships unless an authorized user reactivates them.
- Existing historical relationships to inactive records must continue to resolve and display correctly.
- Inactive records should be clearly labeled when displayed.
- Authorized users may reactivate records.
- APIs should exclude inactive records by default unless an explicit include-inactive parameter or administrative operation is used.
- Reports containing historical data must not silently omit records merely because the related current catalog record is inactive.

## 2. Entity List

- Categories
- Subcategories
- Manufacturers
- Brands
- Products
- Product variants
- Suppliers/vendors
- Supplier product listings
- Supplier listing SKU exceptions
- Product identifiers
- Product identifier types
- External systems or marketplaces for scoped identifiers
- Identifier exceptions
- Units of measure
- Product dimensions
- Flexible product specifications
- Product links
- Spec-sheet links and local document references
- Current supplier prices
- Historical prices
- Internal notes
- Active/inactive records
- Accounting export profiles
- Accounting export mappings
- Accounting export batches
- Accounting export staged transactions
- Accounting export staged lines
- Accounting export validation results

## 3. Table-By-Table Field Proposal

### material_categories

Stores an unlimited category tree. The MVP user interface should initially display three levels: Category, Subcategory, and Material Type. The database must not enforce a three-level limit.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| parent_id | bigint null foreign key to material_categories.id | Null for top-level categories; populated for subcategories. |
| name | varchar(160) not null | Display name. |
| slug | varchar(180) not null | Stable human-readable key. |
| normalized_slug | varchar(180) not null | Normalized comparison value for case-insensitive uniqueness and lookup. |
| description | text null | Optional internal description. |
| sort_order | integer not null default 0 | Manual ordering. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### manufacturers

Stores the company that manufactures a product.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| name | varchar(200) not null | Manufacturer name. |
| normalized_name | varchar(200) not null | Case-insensitive matching key. |
| website_url | text null | Manufacturer website. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### brands

Stores brand names. A brand may optionally belong to a manufacturer.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| manufacturer_id | bigint null foreign key to manufacturers.id | Optional owner or primary manufacturer. |
| name | varchar(200) not null | Brand name. |
| normalized_name | varchar(200) not null | Case-insensitive matching key. |
| website_url | text null | Brand website. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### products

Stores the general product concept. This table must not store supplier-specific SKU, supplier price, supplier URL, or supplier purchase unit.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| category_id | bigint null foreign key to material_categories.id | Product category or subcategory. |
| manufacturer_id | bigint null foreign key to manufacturers.id | Manufacturer when known. |
| brand_id | bigint null foreign key to brands.id | Brand when known. |
| name | varchar(240) not null | General product name. |
| normalized_name | varchar(240) not null | Case-insensitive matching key. |
| description | text null | Product-level description. |
| manufacturer_model_number | varchar(160) null | General manufacturer model number when it applies to the product as a whole. |
| default_uom_id | bigint null foreign key to units_of_measure.id | Default internal reporting unit. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### product_variants

Stores the purchasable or distinguishable version of a product, such as size, color, finish, pack count, grade, or formulation.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint not null foreign key to products.id | Parent general product. |
| variant_name | varchar(240) not null | Human-readable variant name. |
| normalized_variant_name | varchar(240) not null | Case-insensitive matching key. |
| manufacturer_variant_code | varchar(160) null | Manufacturer variant code when distinct from product model number. |
| default_purchase_uom_id | bigint null foreign key to units_of_measure.id | Default unit for purchasing if known. |
| default_usage_uom_id | bigint null foreign key to units_of_measure.id | Default unit for reporting or usage. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### units_of_measure

Stores purchase, reporting, and dimensional units.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| code | varchar(40) not null | Example: each, box, roll, ft, sqft, gal. |
| name | varchar(120) not null | Display name. |
| unit_type | varchar(40) not null | Example: count, length, area, volume, weight, package. |
| base_unit_id | bigint null foreign key to units_of_measure.id | Optional conversion base unit. |
| conversion_factor_to_base | numeric(18,6) null | Multiplier to base unit when fixed. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Approved MVP seed set:

| Category | Unit | Stable code | Notes |
| --- | --- | --- | --- |
| Count | Each | EA | Count unit. |
| Count | Piece | PC | Count unit. |
| Count | Pair | PR | Count unit. |
| Count | Set | SET | Count unit. |
| Count | Dozen | DOZ | 12 each. |
| Count | Hundred | HUN | 100 each. |
| Count | Thousand | THOU | 1,000 each. |
| Packaging and material forms | Pack | PACK | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Box | BOX | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Carton | CARTON | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Case | CASE | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Bundle | BUNDLE | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Pallet | PALLET | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Bag | BAG | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Roll | ROLL | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Spool | SPOOL | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Coil | COIL | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Tube | TUBE | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Cartridge | CARTRIDGE | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Can | CAN | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Pail | PAIL | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Bucket | BUCKET | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Bottle | BOTTLE | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Jar | JAR | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Drum | DRUM | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Sheet | SHEET | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Panel | PANEL | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Board | BOARD | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Stick | STICK | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Length | LENGTH | Product-specific quantity; no universal conversion. |
| Packaging and material forms | Lot | LOT | Product-specific quantity; no universal conversion. |
| U.S. customary length | Inch | IN | Convertible length unit. |
| U.S. customary length | Foot | FT | Convertible length unit. |
| U.S. customary length | Yard | YD | Convertible length unit. |
| U.S. customary length | Linear Inch | LIN | Linear length unit. |
| U.S. customary length | Linear Foot | LFT | Linear length unit. |
| U.S. customary length | Linear Yard | LYD | Linear length unit. |
| Metric length | Millimeter | MM | Convertible length unit. |
| Metric length | Centimeter | CM | Convertible length unit. |
| Metric length | Meter | M | Convertible length unit. |
| Metric length | Kilometer | KM | Convertible length unit. |
| U.S. customary area | Square Inch | SQIN | Convertible area unit. |
| U.S. customary area | Square Foot | SQFT | Convertible area unit. |
| U.S. customary area | Square Yard | SQYD | Convertible area unit. |
| U.S. customary area | Acre | ACRE | Convertible area unit. |
| U.S. customary area | Roofing Square | ROOF_SQ | Defined as 100 square feet. |
| Metric area | Square Millimeter | SQMM | Convertible area unit. |
| Metric area | Square Centimeter | SQCM | Convertible area unit. |
| Metric area | Square Meter | SQM | Convertible area unit. |
| Metric area | Hectare | HA | Convertible area unit. |
| U.S. customary volume | Fluid Ounce | FLOZ | U.S. customary liquid volume. |
| U.S. customary volume | Cup | CUP | U.S. customary liquid volume. |
| U.S. customary volume | Pint | PT | U.S. customary liquid volume. |
| U.S. customary volume | Quart | QT | U.S. customary liquid volume. |
| U.S. customary volume | Gallon | GAL | U.S. liquid gallon. |
| U.S. customary volume | Cubic Inch | CUIN | Convertible volume unit. |
| U.S. customary volume | Cubic Foot | CUFT | Convertible volume unit. |
| U.S. customary volume | Cubic Yard | CUYD | Convertible volume unit. |
| U.S. customary volume | Board Foot | BF | Defined as 144 cubic inches. |
| Metric volume | Milliliter | ML | Convertible volume unit. |
| Metric volume | Liter | L | Convertible volume unit. |
| Metric volume | Cubic Centimeter | CUCM | Convertible volume unit. |
| Metric volume | Cubic Meter | CUM | Convertible volume unit. |
| U.S. customary weight | Ounce | OZ | U.S. customary weight. |
| U.S. customary weight | Pound | LB | U.S. customary weight. |
| U.S. customary weight | US Short Ton | TON_US | 2,000 pounds; distinct from Metric Tonne. |
| Metric weight | Gram | G | Metric weight. |
| Metric weight | Kilogram | KG | Metric weight. |
| Metric weight | Metric Tonne | TONNE | 1,000 kilograms; distinct from US Short Ton. |

Units remain user-manageable so authorized users can add or deactivate units after MVP launch. Convertible physical units may use unit_type, base_unit_id, and conversion_factor_to_base metadata. Packaging and material-form units such as Box, Bag, Roll, and Pallet must not receive universal conversions because quantities depend on the specific supplier listing or product. Product-specific package quantities and purchase-unit relationships should remain on supplier_product_listings or other appropriate product-specific records.

### product_dimension_sets

Stores zero, one, or multiple dimension sets for product variants. Dimension sets usually apply to variants rather than the general product. Each set must have either a standardized dimension_set_type or a custom_label describing its context.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_variant_id | bigint not null foreign key to product_variants.id | Variant being described. |
| dimension_set_type | varchar(60) null | Standardized type such as nominal, actual, product, package, shipping, inside, outside, assembled, or folded. |
| custom_label | varchar(160) null | Custom label for unusual products or contexts not covered by standardized types. |
| is_primary | boolean not null default false | Marks the primary display set for the variant. |
| notes | text null | Optional clarification. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

A product variant is not required to have a primary dimension set. At most one dimension set per product variant may be marked as primary. Standardized dimension-set types should be supported for consistency, while custom labels remain available for unusual products.

### product_dimension_measurements

Stores individual measurements within a dimension set. Different dimension sets do not need to contain the same measurement fields.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_dimension_set_id | bigint not null foreign key to product_dimension_sets.id | Dimension set containing this measurement. |
| measurement_type | varchar(60) not null | Example: length, width, height, thickness, diameter, depth, weight. |
| measurement_value | numeric(18,6) not null | Measurement value. |
| uom_id | bigint not null foreign key to units_of_measure.id | Unit for this measurement. |
| sort_order | integer not null default 0 | Display ordering inside the set. |
| notes | text null | Optional clarification. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### product_spec_definitions

Defines flexible specification names without adding columns to the products or variants tables. Flexible specifications are for product attributes, not dimensions, identifiers, supplier data, or prices; those remain in their dedicated schema areas.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| category_id | bigint null foreign key to material_categories.id | Optional category-specific spec. |
| name | varchar(160) not null | Example: finish, color, grade, fire_rating. |
| label | varchar(180) not null | Display label. |
| data_type | varchar(40) not null | Example: text, number, boolean, date, enum. |
| value_scope | varchar(40) not null | Allowed value ownership: product_only, variant_only, or product_and_variant. |
| uom_id | bigint null foreign key to units_of_measure.id | Optional unit for numeric specs. |
| allowed_values | jsonb null | Optional enum choices or validation metadata. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### product_spec_values

Stores flexible specification values for either a general product or a variant. Product-level values describe specifications shared by the product's variants. Variant-level values describe specifications specific to one variant.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint null foreign key to products.id | Product-level spec when applicable. |
| product_variant_id | bigint null foreign key to product_variants.id | Variant-level spec when applicable. |
| spec_definition_id | bigint not null foreign key to product_spec_definitions.id | Specification definition. |
| value_text | text null | Text value. |
| value_number | numeric(18,6) null | Numeric value. |
| value_boolean | boolean null | Boolean value. |
| value_date | date null | Date value. |
| value_json | jsonb null | Structured value when needed. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Exactly one of product_id or product_variant_id should be populated. Application validation or a PostgreSQL check constraint should enforce that exactly one typed value column is populated when practical. Validation must also prevent product-level values when the definition is variant_only and prevent variant-level values when the definition is product_only.

Effective variant specifications are resolved by inheritance and override. A variant inherits product-level specification values from its parent product when no variant-level value exists for the same specification. When both product-level and variant-level values exist for the same specification, Donna uses the variant-level value for display and export of that variant's effective specifications.

### suppliers

Stores vendors and suppliers.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| name | varchar(240) not null | Supplier display name. |
| normalized_name | varchar(240) not null | Case-insensitive matching key. |
| website_url | text null | Supplier website. |
| phone | varchar(80) null | General phone number. |
| email | varchar(254) null | General email address. |
| account_reference | varchar(120) null | Non-secret internal account label or vendor reference. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### supplier_product_listings

Connects a product variant to a supplier and stores supplier-specific purchase details.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| supplier_id | bigint not null foreign key to suppliers.id | Supplier selling the item. |
| product_variant_id | bigint not null foreign key to product_variants.id | Variant being sold. |
| supplier_sku | varchar(160) null | Supplier-specific SKU. |
| normalized_supplier_sku | varchar(160) null | Normalized supplier SKU for supplier-scoped duplicate detection. |
| supplier_model_number | varchar(160) null | Supplier-specific model or catalog number. |
| listing_name | varchar(260) null | Supplier listing title. |
| product_url | text null | Supplier product page URL. |
| purchase_uom_id | bigint null foreign key to units_of_measure.id | Unit used by this supplier listing. |
| package_quantity | numeric(18,6) null | Quantity per package or listing unit. |
| package_uom_id | bigint null foreign key to units_of_measure.id | Unit represented by package_quantity. |
| is_preferred | boolean not null default false | Preferred supplier listing for this variant. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Supplier SKUs are normally unique within one supplier after normalization, but approved duplicates may be allowed through a controlled exception workflow. The same SKU text may exist for different suppliers.

### supplier_listing_sku_exceptions

Records authorized exceptions for duplicate normalized supplier SKUs within the same supplier. Supplier SKU exceptions use this separate audited mechanism because supplier SKUs remain on supplier_product_listings rather than being moved into product_identifiers.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| supplier_product_listing_id | bigint not null foreign key to supplier_product_listings.id | Listing receiving the exception. |
| conflicting_supplier_product_listing_id | bigint not null foreign key to supplier_product_listings.id | Other supplier listing with the same normalized supplier SKU. |
| exception_reason | text not null | Required business reason. |
| approved_by_user_id | bigint not null | Future foreign key to users table; required approver. |
| approved_at | timestamptz not null | Approval timestamp. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

The two supplier listing IDs must be different and should belong to the same supplier. Repeated supplier SKUs involving more than two listings may require multiple pairwise conflict records unless a future grouped-conflict design replaces this approach.

### product_identifier_types

Configures identifier types so Donna does not hard-code every identifier type in application logic.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| code | varchar(80) not null | Stable identifier type code, such as upc_a, ean_13, gtin_14, manufacturer_part_number, asin, or legacy_receipt_code. |
| label | varchar(160) not null | Display label. |
| uniqueness_scope | varchar(40) not null | Supported values: global, manufacturer, supplier, external_system, none. |
| normalization_rule | varchar(80) not null | Configured rule for deriving normalized values. |
| description | text null | Optional guidance for users and import workflows. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Example uniqueness-scope mappings:

- UPC-A: global
- EAN-13: global
- GTIN-14: global
- Manufacturer part number: manufacturer
- Supplier SKU: supplier, stored on supplier_product_listings
- ASIN: external_system, scoped to the applicable marketplace or external system
- Legacy or unreliable receipt code: none

Identifier comparison should use normalized values while retaining the original entered value for display and audit purposes. Normalization may vary by identifier type. For example, punctuation or spaces may be removed where appropriate, but leading zeroes must not be discarded from barcode identifiers.

### external_systems

Stores external systems or marketplaces used for externally scoped identifiers and future integrations.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| code | varchar(80) not null | Stable code, such as amazon_marketplace. |
| name | varchar(180) not null | Display name. |
| system_type | varchar(60) null | Example: marketplace, accounting, supplier_portal. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### product_identifiers

Stores additional identifiers for products, variants, and supplier listings. Donna can store multiple manufacturer, barcode, and other identifiers for a product variant. Supplier-specific SKUs remain on supplier_product_listings and must not be moved onto the general product or product-variant tables. The internal database id remains the authoritative record identity, but it is not a user-facing SKU.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint null foreign key to products.id | General product identifier. |
| product_variant_id | bigint null foreign key to product_variants.id | Variant identifier. |
| supplier_product_listing_id | bigint null foreign key to supplier_product_listings.id | Supplier listing identifier. |
| identifier_type_id | bigint not null foreign key to product_identifier_types.id | Configured identifier type. |
| manufacturer_id | bigint null foreign key to manufacturers.id | Required scope owner for manufacturer-scoped identifiers when not determined by the product or variant. |
| supplier_id | bigint null foreign key to suppliers.id | Required scope owner for supplier-scoped non-SKU identifiers when not determined by the supplier listing. |
| external_system_id | bigint null foreign key to external_systems.id | Required scope owner for external-system identifiers. |
| identifier_value | varchar(200) not null | Original entered identifier value retained for display and audit. |
| normalized_identifier_value | varchar(200) not null | Normalized matching value. |
| is_primary | boolean not null default false | Marks preferred identifier for this scope/type. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Exactly one of product_id, product_variant_id, or supplier_product_listing_id should be populated. The applicable scope owner is determined from the identifier type and target record where possible: manufacturer-scoped identifiers use the target product or variant's manufacturer unless manufacturer_id is explicitly needed; supplier-scoped identifiers use supplier_product_listing.supplier_id when attached to a listing; external-system identifiers require external_system_id. Supplier SKUs remain in supplier_product_listings, where supplier_id provides the uniqueness scope.

Global, manufacturer, supplier, and external-system identifiers are normally unique within their applicable scopes. Donna must perform duplicate detection and scope validation transactionally before saving. A duplicate must be rejected unless an authorized exception is created as part of the same controlled workflow. Ordinary users must not be able to bypass duplicate detection. Where necessary to prevent concurrent duplicate inserts, implementation should use an appropriate PostgreSQL-safe concurrency mechanism, such as transaction-level locking or advisory locking.

### product_identifier_exceptions

Records authorized exceptions for incorrect, ambiguous, or genuinely reused real-world identifiers. Exceptions must require a reason and audit information rather than silently bypassing duplicate detection.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_identifier_id | bigint not null foreign key to product_identifiers.id | Identifier receiving the exception. |
| conflicting_product_identifier_id | bigint not null foreign key to product_identifiers.id | Other identifier involved in the approved conflict. |
| exception_reason | text not null | Required business reason. |
| approved_by_user_id | bigint not null | Future foreign key to users table; required approver. |
| approved_at | timestamptz not null | Approval timestamp. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

The two identifier IDs must be different. Repeated identifiers involving more than two catalog targets may require multiple pairwise conflict records unless a future grouped-conflict design replaces this approach.

### product_links

Stores general product, variant, or supplier-listing links.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint null foreign key to products.id | Product-level link. |
| product_variant_id | bigint null foreign key to product_variants.id | Variant-level link. |
| supplier_product_listing_id | bigint null foreign key to supplier_product_listings.id | Supplier listing link. |
| link_type | varchar(60) not null | Example: product_page, install_guide, safety_data_sheet, spec_sheet. |
| url | text not null | Link target. |
| label | varchar(200) null | Display label. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Exactly one of product_id, product_variant_id, or supplier_product_listing_id should be populated.

### product_documents

References local files or document repository records without storing large binary files in PostgreSQL. Donna stores document files in local file storage. Application configuration defines the local storage root, and database records store a normalized relative storage key beneath that root.

`product_documents` is only the material-catalog association for documents attached to products, variants, or supplier listings. Receipt files, supplier-level documents, generated accounting exports, and other non-product documents must not be forced into `product_documents`. Those files should use a future general document repository or document-record table that follows the same approved local-storage rules: configured storage root, relative storage key, generated filename, original filename, SHA-256 hash, metadata, and integrity status.

Example configured storage root:

```text
D:\AI\Donna_0.0.1\storage
```

Example stored database key:

```text
documents/receipts/2026/06/a8f34c2d.pdf
```

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint null foreign key to products.id | Product-level document. |
| product_variant_id | bigint null foreign key to product_variants.id | Variant-level document. |
| supplier_product_listing_id | bigint null foreign key to supplier_product_listings.id | Supplier listing document. |
| document_type | varchar(60) not null | Example: spec_sheet, receipt, safety_data_sheet, warranty, photo. |
| storage_kind | varchar(40) not null | Example: local_file, document_record. |
| storage_key | text null | Normalized relative key beneath the configured storage root. Must not be an absolute path. |
| document_record_id | bigint null | Optional future foreign key to the general document repository table. |
| original_filename | varchar(260) null | Original uploaded filename. |
| stored_filename | varchar(260) null | Safe generated stored filename. User-provided filenames must not determine this value. |
| file_extension | varchar(32) null | File extension retained for metadata and validation. |
| content_type | varchar(120) null | MIME type when known. |
| file_size_bytes | bigint null | File size for display and validation. |
| checksum_sha256 | char(64) null | Optional deduplication and integrity check. |
| integrity_verified_at | timestamptz null | Last successful file existence and hash verification timestamp. |
| document_status | varchar(40) not null default 'active' | Supported values: active, archived, deleted. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Exactly one of product_id, product_variant_id, or supplier_product_listing_id should be populated. Large files remain on local storage; PostgreSQL stores only metadata and references.

Future receipt document references, accounting export generated-document references, and other broad document references point to the future general document repository, not `product_documents`.

Path and display rules:

- Database records must not store full absolute Windows paths.
- The relative storage key must be normalized into a consistent application format. Prefer forward slashes in stored database keys, even when the application runs on Windows.
- The application may convert stored keys to operating-system paths when accessing files.
- Reject absolute paths and path traversal components such as `..`.
- Resolve and validate every path before file access. The resolved path must remain beneath the configured storage root.
- User-provided filenames must not determine the stored filename or folder path. Stored filenames should be generated safely and uniquely.
- Preserve the original filename separately for display and audit purposes.
- Do not expose the absolute Windows storage path through normal API responses or the user interface.
- Display the original filename, document type, date, status, and other useful metadata instead.
- Do not permit users to enter arbitrary server or local computer paths.

Supported logical relative folders include:

- `documents/receipts/YYYY/MM/`
- `documents/products/`
- `documents/suppliers/`
- `exports/`
- `temp/`

Temporary files must not be treated as permanent document records unless they are finalized and moved into permanent storage.

Hash, duplicate, and portability rules:

- Calculate SHA-256 for permanent uploaded documents.
- Use the hash for duplicate detection and integrity verification.
- Do not automatically assume that two records with the same file hash represent the same business document without human or workflow review.
- The database may reference the same physical file from multiple business records only if the application explicitly supports that behavior.
- Do not use the content hash as the required folder structure for MVP.
- Moving Donna's storage folder or using a different drive should require changing configuration rather than updating every document row.
- Database backups and document-storage backups must be coordinated, because restoring only one may leave missing files or orphaned records.
- Document records should support detecting a missing or corrupted physical file.

### supplier_price_history

Stores immutable historical approved prices, including prices created from fully human-approved receipt line items that are valid for price tracking.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| supplier_product_listing_id | bigint not null foreign key to supplier_product_listings.id | Listing being priced. |
| receipt_id | bigint null | Future integration boundary: optional foreign key to approved receipt. |
| receipt_line_item_id | bigint null | Future integration boundary: optional foreign key to approved receipt line item. |
| transaction_type | varchar(60) not null default 'purchase' | Example: purchase, return, refund, rebate_payment, void, reversal. |
| gross_line_amount | numeric(18,4) null | Pre-discount line amount when available. |
| discount_amount | numeric(18,4) null | Confirmed discount amount applied to this line. |
| discount_type | varchar(60) null | Example: sale, coupon, contractor_discount, volume_discount, loyalty_discount, rebate, clearance, manual_adjustment, receipt_level_discount_allocation, unknown_discount. |
| discount_scope | varchar(40) null | Supported values: line_level, receipt_level. |
| net_line_amount | numeric(18,4) null | Final line amount after confirmed discounts. |
| quantity | numeric(18,6) not null | Purchased quantity confirmed for price tracking. |
| purchase_uom_id | bigint not null foreign key to units_of_measure.id | Confirmed purchase unit. |
| package_quantity | numeric(18,6) null | Confirmed package quantity when applicable. |
| package_uom_id | bigint null foreign key to units_of_measure.id | Unit represented by package_quantity. |
| gross_unit_price | numeric(18,4) null | Regular or pre-discount unit price when available. |
| net_unit_price_paid | numeric(18,4) not null | Net unit price actually paid after confirmed discounts. |
| currency_code | char(3) not null default 'USD' | ISO-style currency code. |
| price_uom_id | bigint not null foreign key to units_of_measure.id | Unit the unit prices apply to. |
| observed_at | timestamptz not null | Effective or purchase date, usually receipt date or approval time. |
| source_type | varchar(60) not null | Example: receipt, manual, supplier_site, import. |
| source_document_id | bigint null | Future integration boundary: optional foreign key to document repository. |
| current_regular_price_update_decision | varchar(60) not null default 'not_applicable' | Example: not_applicable, auto_updated, reviewer_approved, reviewer_rejected, blocked_by_rule. |
| approved_by_user_id | bigint not null | Future foreign key to users table; required approver for finalized price-history records. |
| approved_at | timestamptz not null | Approval timestamp. |
| created_at | timestamptz not null | Creation timestamp. |

`supplier_price_history` stores only finalized, fully human-approved price-history records. Pending, rejected, or needs-review receipt lines belong in future receipt-review tables and must not create supplier_price_history rows. Approval audit information is retained through approved_by_user_id and approved_at as future user-table integration boundaries. When a receipt extraction is fully approved by a human, each valid receipt line item should create one immutable supplier_price_history record linked by receipt_line_item_id. Approved historical records should not be overwritten when a later current price is established, except for narrowly defined administrative corrections that would require an auditable correction mechanism later.

Donna must preserve both gross/pre-discount and net-paid values when available. Receipt-level discounts must be allocated to applicable receipt lines before final net unit prices are calculated. Allocation may be proportional or manually assigned, but any automatic allocation must be shown to and confirmed by a human reviewer before final approval. Donna should preserve the original receipt-level discount amount in future receipt records and preserve allocated line-level discount amounts in supplier_price_history for auditability. OCR or AI extraction may suggest discount information, but a human must confirm it before the data is finalized. Donna must not silently infer that every difference between expected and paid price is a discount.

Conditional current-price update rules:

- The receipt and receipt line have completed human review.
- The line is linked to a confirmed supplier product listing.
- Purchase quantity, purchase unit, package quantity, and unit-price calculation are confirmed.
- The transaction is a normal purchase rather than a return, refund, rebate payment, void, or reversal.
- The receipt date is not older than the source date of the existing current regular price.
- The receipt line has not already produced a duplicate price-history record.
- The price is not flagged by configurable abnormal-price or variance-review rules.
- The line is approved for price-history use.
- The price is not a temporary or exceptional discount unless a reviewer explicitly approves it as representative of the current regular price.

Every fully human-approved receipt line that is valid for price tracking creates supplier_price_history and may update supplier_current_prices.latest_confirmed_net_paid. Donna may automatically update supplier_current_prices.current_regular_price only when all conditional current-price update rules pass. Returns, refunds, rebates, voids, and reversals should be identified by transaction_type and must not automatically become the current regular supplier price. Rebate payments may be tracked separately from point-of-sale discounts when necessary.

### supplier_current_prices

Stores current price concepts for a supplier listing. Donna maintains separate current records for the current regular supplier price and the latest confirmed net price actually paid. This section follows supplier_price_history because current-price rows may reference a supporting historical price row.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| supplier_product_listing_id | bigint not null foreign key to supplier_product_listings.id | Listing being priced. |
| price_kind | varchar(40) not null | Supported values: current_regular_price, latest_confirmed_net_paid. |
| price_amount | numeric(18,4) not null | Current price. |
| currency_code | char(3) not null default 'USD' | ISO-style currency code. |
| price_uom_id | bigint not null foreign key to units_of_measure.id | Unit the price applies to. |
| source_date | date not null | Receipt, supplier quote, manual entry, or approval source date for comparison. |
| source_type | varchar(60) not null | Example: manual, receipt, supplier_site, import. |
| source_receipt_line_item_id | bigint null | Future integration boundary: optional foreign key to approved receipt line item. |
| source_supplier_price_history_id | bigint null foreign key to supplier_price_history.id | Historical price record supporting this current price, when applicable. |
| approved_by_user_id | bigint null | Optional future foreign key to users table. |
| approved_at | timestamptz null | Approval timestamp. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Only one current price should exist per supplier listing, currency, price unit, and price_kind. A temporary or exceptional discount normally updates supplier_price_history and the latest_confirmed_net_paid record, but does not automatically replace the current_regular_price. A reviewer may explicitly approve a discounted price as the new current_regular_price when appropriate.

### material_internal_notes

Stores internal notes without cluttering product and supplier listing records.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| product_id | bigint null foreign key to products.id | Product-level note. |
| product_variant_id | bigint null foreign key to product_variants.id | Variant-level note. |
| supplier_product_listing_id | bigint null foreign key to supplier_product_listings.id | Supplier listing note. |
| supplier_id | bigint null foreign key to suppliers.id | Supplier-level note. |
| note_body | text not null | Internal note content. |
| created_by_user_id | bigint null | Optional future foreign key to users table. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Exactly one parent reference should be populated.

### accounting_export_profiles

Stores configurable export profiles for reviewed CSV or Excel exports. Live QuickBooks integration remains deferred. Do not claim an exported file is directly importable into QuickBooks until the specific QuickBooks workflow and format are verified.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| name | varchar(160) not null | Profile display name. |
| export_mode | varchar(60) not null | Example: expense_line, item_based. |
| export_format | varchar(40) not null | Example: csv, xlsx. |
| required_fields | jsonb not null default '{}' | Profile-specific required transaction and line fields. |
| column_config | jsonb not null default '{}' | Column names, order, optional fields, and profile-specific layout. |
| date_format | varchar(40) null | Export date format. |
| number_format | varchar(40) null | Export numeric format. |
| include_tax_fields | boolean not null default false | Whether tax columns are included. |
| include_customer_job | boolean not null default false | Whether customer/job columns are included. |
| include_class | boolean not null default false | Whether class columns are included. |
| include_location | boolean not null default false | Whether location columns are included. |
| is_active | boolean not null default true | Soft visibility control. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### accounting_export_mappings

Stores reusable mapping records for accounting exports without making those mappings Donna's authoritative record identity. Not every Donna product or material must have a QuickBooks item mapping.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| profile_id | bigint null foreign key to accounting_export_profiles.id | Optional profile-specific mapping. |
| mapping_type | varchar(60) not null | Example: vendor, item_service, expense_account, cogs_account, customer_job, class, location, unit_of_measure. |
| donna_entity_type | varchar(80) null | Example: supplier, product, product_variant, supplier_product_listing, unit_of_measure. |
| donna_entity_id | bigint null | ID of the mapped Donna record, interpreted with donna_entity_type. |
| external_name | varchar(240) not null | Accounting-system display name used for export. |
| external_reference | varchar(240) null | Optional accounting-system reference when known. |
| mapping_payload | jsonb not null default '{}' | Profile-specific mapping details. |
| is_active | boolean not null default true | Inactive mappings are retained for history and hidden from new selection by default. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Unmapped materials may export as expense lines when an account mapping exists. Missing or inactive mappings must be detected during export validation.

### accounting_export_batches

Stores reviewed export snapshots and generated-file references. Export staging must be a snapshot, not a live view.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| profile_id | bigint not null foreign key to accounting_export_profiles.id | Export profile used. |
| status | varchar(40) not null default 'draft' | Supported values: draft, needs_mapping, ready, exported, failed, cancelled. |
| export_format | varchar(40) not null | Example: csv, xlsx. |
| generated_storage_key | text null | Interim or snapshot relative local-storage key for generated files, using Donna's document storage architecture. |
| generated_document_id | bigint null | Optional future foreign key to the general document repository, not product_documents. |
| validation_summary | jsonb not null default '{}' | Counts and summary of warnings and errors. |
| warning_count | integer not null default 0 | Number of non-blocking warnings. |
| error_count | integer not null default 0 | Number of blocking errors. |
| created_by_user_id | bigint null | Optional future foreign key to users table. |
| reviewed_by_user_id | bigint null | Optional future foreign key to users table. |
| reviewed_at | timestamptz null | Human review timestamp. |
| exported_at | timestamptz null | Export completion timestamp. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

Do not silently overwrite exported batches. Corrections must create auditable changes, such as a new batch, corrected batch, or explicit correction record. An export batch may become ready only when it has no unresolved blocking errors, and it may become exported only from a valid ready state. Status, validation counts, and validation results must remain consistent.

### accounting_export_transactions

Stores staged transaction rows for reviewed export batches.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| export_batch_id | bigint not null foreign key to accounting_export_batches.id | Parent export batch. |
| source_receipt_id | bigint null | Future integration boundary: stable Donna source receipt reference. |
| vendor_name | varchar(240) not null | Vendor name for export snapshot. |
| transaction_date | date not null | Transaction date. |
| due_date | date null | Due date when applicable. |
| reference_number | varchar(160) null | Receipt, invoice, or reference number. |
| memo | text null | Transaction memo. |
| currency_code | char(3) not null default 'USD' | Currency. |
| tax_total | numeric(18,4) null | Transaction tax total. |
| status | varchar(40) not null default 'draft' | Supported values: draft, needs_mapping, ready, exported, failed, cancelled. |
| validation_status | varchar(40) not null default 'needs_review' | Example: needs_review, valid, warning, error. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### accounting_export_lines

Stores staged transaction-line rows for reviewed export batches.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| export_transaction_id | bigint not null foreign key to accounting_export_transactions.id | Parent staged transaction. |
| source_receipt_line_item_id | bigint null | Future integration boundary: stable Donna source receipt-line reference. |
| item_service_mapping_id | bigint null foreign key to accounting_export_mappings.id | Optional QuickBooks item/service mapping. |
| account_mapping_id | bigint null foreign key to accounting_export_mappings.id | Expense or cost-of-goods account mapping. |
| customer_job_mapping_id | bigint null foreign key to accounting_export_mappings.id | Optional customer/job mapping. |
| class_mapping_id | bigint null foreign key to accounting_export_mappings.id | Optional class mapping. |
| location_mapping_id | bigint null foreign key to accounting_export_mappings.id | Optional location mapping. |
| line_description | text null | Line description or memo. |
| quantity | numeric(18,6) not null | Quantity. |
| uom_id | bigint null foreign key to units_of_measure.id | Donna unit of measure. |
| export_uom_text | varchar(80) null | Unit text used in the export snapshot. |
| unit_price | numeric(18,4) not null | Unit price. |
| gross_amount | numeric(18,4) not null | Gross line amount. |
| discount_amount | numeric(18,4) null | Discount amount. |
| net_amount | numeric(18,4) not null | Net amount. |
| tax_amount | numeric(18,4) null | Tax amount. |
| tax_treatment | varchar(80) null | Tax treatment or code for export. |
| status | varchar(40) not null default 'draft' | Supported values: draft, needs_mapping, ready, exported, failed, cancelled. |
| validation_status | varchar(40) not null default 'needs_review' | Example: needs_review, valid, warning, error. |
| created_at | timestamptz not null | Creation timestamp. |
| updated_at | timestamptz not null | Last update timestamp. |

### accounting_export_validation_results

Stores validation results for batches, transactions, and lines.

| Field | Type | Notes |
| --- | --- | --- |
| id | bigint primary key | Surrogate primary key. |
| export_batch_id | bigint not null foreign key to accounting_export_batches.id | Related export batch. |
| export_transaction_id | bigint null foreign key to accounting_export_transactions.id | Related staged transaction when applicable. |
| export_line_id | bigint null foreign key to accounting_export_lines.id | Related staged line when applicable. |
| severity | varchar(40) not null | Supported values: blocking_error, warning. |
| rule_code | varchar(120) not null | Stable validation rule code. |
| message | text not null | Human-readable validation message. |
| details | jsonb not null default '{}' | Supporting validation details. |
| reviewed_by_user_id | bigint null | Optional future foreign key to users table. |
| reviewed_at | timestamptz null | Human review timestamp. |
| created_at | timestamptz not null | Creation timestamp. |

Before final export, Donna must validate vendor and transaction date; required account or item mappings; quantity, price, total, discount, and tax consistency; missing or inactive mappings; duplicate export risk; unsupported units; and any customer/job, class, or location required by the selected profile. Donna must distinguish blocking errors from warnings. A final export must be prohibited while any unresolved blocking_error exists. Human review alone does not convert or bypass a blocking error; the underlying data, mapping, or configuration must be corrected and validation rerun. If Donna later supports an authorized override, it must require a documented reason, approving user, timestamp, and audit record; that override workflow is not part of this design. Non-blocking warnings may remain after human review when the selected export profile permits them.

## 4. Relationships

- material_categories is self-referencing through parent_id and supports unlimited category nesting.
- products belongs to one optional category, manufacturer, brand, and default unit of measure.
- brands may belong to one manufacturer.
- product_variants belongs to one product.
- supplier_product_listings belongs to one supplier and one product_variant.
- One product_variant can have many supplier_product_listings.
- supplier_listing_sku_exceptions belongs to two supplier_product_listings involved in an approved duplicate SKU conflict.
- supplier_current_prices belongs to one supplier_product_listing.
- supplier_price_history belongs to one supplier_product_listing and can later reference one approved receipt line item.
- product_dimension_sets belongs to one product_variant.
- product_dimension_measurements belongs to one product_dimension_set.
- product_spec_values belongs to one spec definition and either one product or one product_variant.
- product_identifier_types configures uniqueness scope and normalization rules for product_identifiers.
- product_identifiers can identify one product, one product_variant, or one supplier_product_listing.
- An externally scoped product_identifier belongs to one external_system.
- product_identifier_exceptions belongs to two product_identifiers involved in an approved identifier conflict.
- product_links and product_documents can attach to one product, one product_variant, or one supplier_product_listing.
- material_internal_notes can attach to one product, product_variant, supplier_product_listing, or supplier.
- accounting_export_mappings can optionally belong to one accounting_export_profile.
- accounting_export_batches belongs to one accounting_export_profile.
- accounting_export_transactions belongs to one accounting_export_batch and preserves a stable Donna source receipt reference when available.
- accounting_export_lines belongs to one accounting_export_transaction and preserves a stable Donna source receipt-line reference when available.
- accounting_export_lines can reference reusable item/service, account, customer/job, class, and location mappings.
- accounting_export_validation_results belongs to one accounting_export_batch and can optionally attach to one staged transaction or staged line.

## 5. Uniqueness Rules

Actual unconditional database unique constraints:

- material_categories: unique parent_id plus normalized_slug.
- manufacturers: unique normalized_name.
- brands: unique manufacturer_id plus normalized_name, with a separate rule for brands without a manufacturer.
- units_of_measure: unique code.
- products: unique manufacturer_id plus brand_id plus normalized_name plus manufacturer_model_number when manufacturer_model_number is present.
- product_variants: unique product_id plus normalized_variant_name.
- product_dimension_sets: at most one primary display set per product_variant_id, enforced with a partial unique index where is_primary is true.
- product_dimension_measurements: unique product_dimension_set_id plus measurement_type when a set should have only one value for that measurement type.
- product_spec_definitions: unique category_id plus name, with a separate rule for global definitions where category_id is null.
- product_spec_values: unique product_id plus spec_definition_id for product-level specs.
- product_spec_values: unique product_variant_id plus spec_definition_id for variant-level specs.
- suppliers: unique normalized_name.
- supplier_product_listings: unique supplier_id plus product_variant_id plus supplier_model_number when supplier_model_number is present.
- product_identifier_types: unique code.
- external_systems: unique code.
- product_links: unique parent scope plus link_type plus url.
- product_documents: unique storage_key for permanent local files unless a future shared physical-file design intentionally permits multiple business records to reference the same stored object.
- supplier_current_prices: unique supplier_product_listing_id plus currency_code plus price_uom_id plus price_kind.
- supplier_price_history: unique receipt_line_item_id plus supplier_product_listing_id when receipt_line_item_id is present, to prevent duplicate history rows for the same approved receipt line.
- accounting_export_profiles: unique name.
- accounting_export_batches: exported batches must not be silently overwritten; corrections should be represented by auditable new or corrected batches.
- accounting_export_lines: duplicate export risk should be validated against source_receipt_line_item_id and prior exported batches before final export.

Normal business uniqueness enforced through duplicate-protected workflows:

- supplier_product_listings: normalized_supplier_sku is normally unique within supplier_id. The same SKU text may exist for different suppliers. Duplicates within one supplier require a supplier_listing_sku_exceptions record created as part of the same controlled workflow.
- product_identifiers with global scope: identifier_type_id plus normalized_identifier_value normally identifies only one catalog target.
- product_identifiers with manufacturer scope: identifier_type_id plus manufacturer_id plus normalized_identifier_value is normally unique.
- product_identifiers with supplier scope: identifier_type_id plus supplier_id plus normalized_identifier_value is normally unique, except supplier SKUs remain on supplier_product_listings.
- product_identifiers with external_system scope: identifier_type_id plus external_system_id plus normalized_identifier_value is normally unique.
- product_identifiers with none scope: no uniqueness rule beyond the row primary key; duplicate detection may still warn users.

For duplicate-protected workflow rules, Donna must validate scope and duplicates transactionally before saving. A duplicate must be rejected unless the appropriate audited exception record is created in the same controlled workflow. Ordinary users must not be able to bypass duplicate detection. Implementation should use PostgreSQL-safe concurrency control, such as transaction-level locking or advisory locking, when needed to prevent concurrent duplicate inserts.

## 6. Important Indexes

Ordinary lookup indexes:

- material_categories(parent_id)
- material_categories(normalized_slug)
- material_categories(is_active)
- manufacturers(normalized_name)
- brands(manufacturer_id)
- brands(normalized_name)
- products(category_id)
- products(manufacturer_id)
- products(brand_id)
- products(normalized_name)
- products(is_active)
- product_variants(product_id)
- product_variants(is_active)
- product_dimension_sets(product_variant_id)
- product_dimension_sets(product_variant_id) where is_primary is true
- product_dimension_measurements(product_dimension_set_id)
- product_dimension_measurements(measurement_type)
- suppliers(normalized_name)
- suppliers(is_active)
- supplier_product_listings(supplier_id)
- supplier_product_listings(product_variant_id)
- supplier_product_listings(supplier_sku)
- supplier_product_listings(normalized_supplier_sku)
- supplier_product_listings(is_active)
- supplier_listing_sku_exceptions(supplier_product_listing_id)
- supplier_listing_sku_exceptions(conflicting_supplier_product_listing_id)
- product_identifier_types(code)
- product_identifier_types(uniqueness_scope)
- external_systems(code)
- product_identifiers(identifier_type_id, normalized_identifier_value)
- product_identifiers(manufacturer_id, normalized_identifier_value)
- product_identifiers(supplier_id, normalized_identifier_value)
- product_identifiers(external_system_id, normalized_identifier_value)
- product_identifier_exceptions(product_identifier_id)
- product_identifier_exceptions(conflicting_product_identifier_id)
- product_spec_values(product_id)
- product_spec_values(product_variant_id)
- product_spec_values(spec_definition_id)
- product_links(product_id)
- product_links(product_variant_id)
- product_links(supplier_product_listing_id)
- product_documents(product_id)
- product_documents(product_variant_id)
- product_documents(supplier_product_listing_id)
- product_documents(storage_key)
- product_documents(checksum_sha256)
- product_documents(document_status)
- supplier_current_prices(supplier_product_listing_id)
- supplier_current_prices(price_kind)
- supplier_price_history(supplier_product_listing_id, observed_at)
- supplier_price_history(receipt_line_item_id)
- supplier_price_history(transaction_type)
- supplier_price_history(discount_type)
- supplier_price_history(current_regular_price_update_decision)
- accounting_export_profiles(is_active)
- accounting_export_mappings(profile_id)
- accounting_export_mappings(mapping_type)
- accounting_export_mappings(donna_entity_type, donna_entity_id)
- accounting_export_mappings(is_active)
- accounting_export_batches(profile_id)
- accounting_export_batches(status)
- accounting_export_batches(generated_storage_key)
- accounting_export_transactions(export_batch_id)
- accounting_export_transactions(source_receipt_id)
- accounting_export_transactions(status)
- accounting_export_lines(export_transaction_id)
- accounting_export_lines(source_receipt_line_item_id)
- accounting_export_lines(status)
- accounting_export_validation_results(export_batch_id)
- accounting_export_validation_results(export_transaction_id)
- accounting_export_validation_results(export_line_id)
- accounting_export_validation_results(severity)
- material_internal_notes(product_id)
- material_internal_notes(product_variant_id)
- material_internal_notes(supplier_product_listing_id)
- material_internal_notes(supplier_id)

PostgreSQL full-text search or trigram indexes can be added later for product names, supplier listing names, SKUs, model numbers, and identifiers after search behavior is approved.

## 7. Product-Versus-Variant Example

General product:

- Product: Interior latex paint
- Category: Paint
- Manufacturer: Acme Coatings
- Brand: Acme Pro
- Manufacturer model number: PRO-INTERIOR

Variants:

- Interior latex paint, eggshell, white, 1 gallon
- Interior latex paint, semi-gloss, white, 1 gallon
- Interior latex paint, eggshell, white, 5 gallon

The general product describes the shared product family. Variants describe purchasable differences such as finish, color, and container size.

## 8. Supplier-Listing Example

One product variant can be sold by multiple suppliers:

- Variant: Interior latex paint, eggshell, white, 1 gallon
- Supplier listing 1:
  - Supplier: Supplier A
  - Supplier SKU: A-PAINT-100
  - Product URL: Supplier A product page
  - Purchase unit: each
  - Current price: 34.9900 USD per each
- Supplier listing 2:
  - Supplier: Supplier B
  - Supplier SKU: B-88917
  - Product URL: Supplier B product page
  - Purchase unit: case
  - Package quantity: 4 each
  - Current price: 128.0000 USD per case

The supplier-specific SKU, URL, unit, package quantity, and price live on supplier listing and price tables, not on products.

## 9. Price-History Example

Approved receipt line item:

- Receipt date: 2026-06-16
- Supplier: Supplier A
- Supplier SKU: A-PAINT-100
- Quantity: 2 each
- Gross unit price: 34.9900 USD
- Line-level contractor discount: 5.0000 USD
- Net unit price paid: 32.4900 USD
- Net line amount: 64.9800 USD

Resulting supplier_price_history row:

- supplier_product_listing_id: listing for Supplier A and the paint variant
- receipt_line_item_id: approved receipt line item id
- transaction_type: purchase
- gross_line_amount: 69.9800
- discount_amount: 5.0000
- discount_type: contractor_discount
- discount_scope: line_level
- net_line_amount: 64.9800
- quantity: 2
- purchase_uom_id: each
- package_quantity: null
- package_uom_id: null
- gross_unit_price: 34.9900
- net_unit_price_paid: 32.4900
- currency_code: USD
- price_uom_id: each
- observed_at: 2026-06-16
- source_type: receipt
- approved_by_user_id: approving user id
- approved_at: human approval timestamp

This preserves historical receipt evidence and allows current price updates to remain an explicit business decision.

## 10. Deferred Fields And Future Extensions

- User and approval tables for approved_by_user_id and created_by_user_id.
- Receipt and receipt_line_item tables that connect OCR, human review, and approved line items.
- Document repository table for shared file metadata across receipts, product documents, and reports.
- Unit conversion rules for complex package conversions.
- Search indexes using PostgreSQL full-text search, trigram matching, or both.
- Vendor normalization and merge tooling.
- Product merge and duplicate detection tooling.
- Attachment previews and document retention rules.
- Live QuickBooks integration, pending verified workflow and format requirements.
- Audit log tables for high-risk edits.
- Import batch tables for CSV and Excel imports.

## 11. Open Decisions Requiring User Approval

No unresolved open decisions remain in this schema proposal.
