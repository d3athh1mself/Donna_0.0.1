from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = (
        Index("ix_suppliers_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(240), nullable=False, unique=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    account_reference: Mapped[str | None] = mapped_column(String(120), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    product_listings: Mapped[list["SupplierProductListing"]] = relationship(
        "SupplierProductListing",
        back_populates="supplier",
    )


class SupplierProductListing(Base):
    __tablename__ = "supplier_product_listings"
    __table_args__ = (
        Index("ix_supplier_product_listings_supplier_id", "supplier_id"),
        Index("ix_supplier_product_listings_product_variant_id", "product_variant_id"),
        Index("ix_supplier_product_listings_supplier_sku", "supplier_sku"),
        Index("ix_supplier_product_listings_normalized_supplier_sku", "normalized_supplier_sku"),
        Index("ix_supplier_product_listings_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variants.id"), nullable=False)
    supplier_sku: Mapped[str | None] = mapped_column(String(160), nullable=True)
    normalized_supplier_sku: Mapped[str | None] = mapped_column(String(160), nullable=True)
    supplier_model_number: Mapped[str | None] = mapped_column(String(160), nullable=True)
    listing_name: Mapped[str | None] = mapped_column(String(260), nullable=True)
    product_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    purchase_uom_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    package_quantity: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    package_uom_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    is_preferred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="product_listings")
    product_variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="supplier_listings")
    purchase_uom: Mapped["UnitOfMeasure | None"] = relationship(
        "UnitOfMeasure",
        foreign_keys=[purchase_uom_id],
    )
    package_uom: Mapped["UnitOfMeasure | None"] = relationship(
        "UnitOfMeasure",
        foreign_keys=[package_uom_id],
    )
