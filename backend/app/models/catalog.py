from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MaterialCategory(Base):
    __tablename__ = "material_categories"
    __table_args__ = (
        Index(
            "uq_material_categories_parent_normalized_slug",
            "parent_id",
            "normalized_slug",
            unique=True,
            postgresql_where=text("parent_id IS NOT NULL"),
        ),
        Index(
            "uq_material_categories_top_level_normalized_slug",
            "normalized_slug",
            unique=True,
            postgresql_where=text("parent_id IS NULL"),
        ),
        Index("ix_material_categories_parent_id", "parent_id"),
        Index("ix_material_categories_normalized_slug", "normalized_slug"),
        Index("ix_material_categories_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("material_categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), nullable=False)
    normalized_slug: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    parent: Mapped["MaterialCategory | None"] = relationship(
        "MaterialCategory",
        back_populates="children",
        remote_side="MaterialCategory.id",
    )
    children: Mapped[list["MaterialCategory"]] = relationship(
        "MaterialCategory",
        back_populates="parent",
    )
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = (
        Index("ix_manufacturers_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    brands: Mapped[list["Brand"]] = relationship("Brand", back_populates="manufacturer")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="manufacturer")


class Brand(Base):
    __tablename__ = "brands"
    __table_args__ = (
        Index(
            "uq_brands_manufacturer_normalized_name",
            "manufacturer_id",
            "normalized_name",
            unique=True,
            postgresql_where=text("manufacturer_id IS NOT NULL"),
        ),
        Index(
            "uq_brands_no_manufacturer_normalized_name",
            "normalized_name",
            unique=True,
            postgresql_where=text("manufacturer_id IS NULL"),
        ),
        Index("ix_brands_manufacturer_id", "manufacturer_id"),
        Index("ix_brands_normalized_name", "normalized_name"),
        Index("ix_brands_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    manufacturer_id: Mapped[int | None] = mapped_column(ForeignKey("manufacturers.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(200), nullable=False)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    manufacturer: Mapped["Manufacturer | None"] = relationship("Manufacturer", back_populates="brands")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")


class UnitOfMeasure(Base):
    __tablename__ = "units_of_measure"
    __table_args__ = (
        Index("ix_units_of_measure_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    unit_type: Mapped[str] = mapped_column(String(40), nullable=False)
    base_unit_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    conversion_factor_to_base: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    base_unit: Mapped["UnitOfMeasure | None"] = relationship(
        "UnitOfMeasure",
        remote_side="UnitOfMeasure.id",
    )


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("ix_products_category_id", "category_id"),
        Index("ix_products_manufacturer_id", "manufacturer_id"),
        Index("ix_products_brand_id", "brand_id"),
        Index("ix_products_normalized_name", "normalized_name"),
        Index("ix_products_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("material_categories.id"), nullable=True)
    manufacturer_id: Mapped[int | None] = mapped_column(ForeignKey("manufacturers.id"), nullable=True)
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    manufacturer_model_number: Mapped[str | None] = mapped_column(String(160), nullable=True)
    default_uom_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    category: Mapped["MaterialCategory | None"] = relationship("MaterialCategory", back_populates="products")
    manufacturer: Mapped["Manufacturer | None"] = relationship("Manufacturer", back_populates="products")
    brand: Mapped["Brand | None"] = relationship("Brand", back_populates="products")
    default_uom: Mapped["UnitOfMeasure | None"] = relationship("UnitOfMeasure")
    variants: Mapped[list["ProductVariant"]] = relationship("ProductVariant", back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (
        Index(
            "uq_product_variants_product_normalized_variant_name",
            "product_id",
            "normalized_variant_name",
            unique=True,
        ),
        Index("ix_product_variants_product_id", "product_id"),
        Index("ix_product_variants_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    variant_name: Mapped[str] = mapped_column(String(240), nullable=False)
    normalized_variant_name: Mapped[str] = mapped_column(String(240), nullable=False)
    manufacturer_variant_code: Mapped[str | None] = mapped_column(String(160), nullable=True)
    default_purchase_uom_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    default_usage_uom_id: Mapped[int | None] = mapped_column(ForeignKey("units_of_measure.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    product: Mapped["Product"] = relationship("Product", back_populates="variants")
    default_purchase_uom: Mapped["UnitOfMeasure | None"] = relationship(
        "UnitOfMeasure",
        foreign_keys=[default_purchase_uom_id],
    )
    default_usage_uom: Mapped["UnitOfMeasure | None"] = relationship(
        "UnitOfMeasure",
        foreign_keys=[default_usage_uom_id],
    )
    supplier_listings: Mapped[list["SupplierProductListing"]] = relationship(
        "SupplierProductListing",
        back_populates="product_variant",
    )
