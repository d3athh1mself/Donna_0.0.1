from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.catalog import UnitOfMeasure


@dataclass(frozen=True)
class UnitSeed:
    code: str
    name: str
    unit_type: str
    is_active: bool = True
    base_unit_code: str | None = None
    conversion_factor_to_base: Decimal | None = None


PACKAGING_UNIT_CODES = {
    "PACK",
    "BOX",
    "CARTON",
    "CASE",
    "BUNDLE",
    "PALLET",
    "BAG",
    "ROLL",
    "SPOOL",
    "COIL",
    "TUBE",
    "CARTRIDGE",
    "CAN",
    "PAIL",
    "BUCKET",
    "BOTTLE",
    "JAR",
    "DRUM",
    "SHEET",
    "PANEL",
    "BOARD",
    "STICK",
    "LENGTH",
    "LOT",
}


DEFAULT_UNITS: tuple[UnitSeed, ...] = (
    UnitSeed("EA", "Each", "count"),
    UnitSeed("PC", "Piece", "count"),
    UnitSeed("SET", "Set", "count"),
    UnitSeed("PR", "Pair", "count", base_unit_code="EA", conversion_factor_to_base=Decimal("2")),
    UnitSeed("DOZ", "Dozen", "count", base_unit_code="EA", conversion_factor_to_base=Decimal("12")),
    UnitSeed("HUN", "Hundred", "count", base_unit_code="EA", conversion_factor_to_base=Decimal("100")),
    UnitSeed("THOU", "Thousand", "count", base_unit_code="EA", conversion_factor_to_base=Decimal("1000")),
    UnitSeed("PACK", "Pack", "package"),
    UnitSeed("BOX", "Box", "package"),
    UnitSeed("CARTON", "Carton", "package"),
    UnitSeed("CASE", "Case", "package"),
    UnitSeed("BUNDLE", "Bundle", "package"),
    UnitSeed("PALLET", "Pallet", "package"),
    UnitSeed("BAG", "Bag", "package"),
    UnitSeed("ROLL", "Roll", "package"),
    UnitSeed("SPOOL", "Spool", "package"),
    UnitSeed("COIL", "Coil", "package"),
    UnitSeed("TUBE", "Tube", "package"),
    UnitSeed("CARTRIDGE", "Cartridge", "package"),
    UnitSeed("CAN", "Can", "package"),
    UnitSeed("PAIL", "Pail", "package"),
    UnitSeed("BUCKET", "Bucket", "package"),
    UnitSeed("BOTTLE", "Bottle", "package"),
    UnitSeed("JAR", "Jar", "package"),
    UnitSeed("DRUM", "Drum", "package"),
    UnitSeed("SHEET", "Sheet", "package"),
    UnitSeed("PANEL", "Panel", "package"),
    UnitSeed("BOARD", "Board", "package"),
    UnitSeed("STICK", "Stick", "package"),
    UnitSeed("LENGTH", "Length", "package"),
    UnitSeed("LOT", "Lot", "package"),
    UnitSeed("IN", "Inch", "length"),
    UnitSeed("FT", "Foot", "length", base_unit_code="IN", conversion_factor_to_base=Decimal("12")),
    UnitSeed("YD", "Yard", "length", base_unit_code="IN", conversion_factor_to_base=Decimal("36")),
    UnitSeed("LIN", "Linear Inch", "length", base_unit_code="IN", conversion_factor_to_base=Decimal("1")),
    UnitSeed("LFT", "Linear Foot", "length", base_unit_code="IN", conversion_factor_to_base=Decimal("12")),
    UnitSeed("LYD", "Linear Yard", "length", base_unit_code="IN", conversion_factor_to_base=Decimal("36")),
    UnitSeed("MM", "Millimeter", "length"),
    UnitSeed("CM", "Centimeter", "length", base_unit_code="MM", conversion_factor_to_base=Decimal("10")),
    UnitSeed("M", "Meter", "length", base_unit_code="MM", conversion_factor_to_base=Decimal("1000")),
    UnitSeed("KM", "Kilometer", "length", base_unit_code="MM", conversion_factor_to_base=Decimal("1000000")),
    UnitSeed("SQFT", "Square Foot", "area"),
    UnitSeed("SQIN", "Square Inch", "area", base_unit_code="SQFT", conversion_factor_to_base=Decimal("0.006944")),
    UnitSeed("SQYD", "Square Yard", "area", base_unit_code="SQFT", conversion_factor_to_base=Decimal("9")),
    UnitSeed("ACRE", "Acre", "area", base_unit_code="SQFT", conversion_factor_to_base=Decimal("43560")),
    UnitSeed("ROOF_SQ", "Roofing Square", "area", base_unit_code="SQFT", conversion_factor_to_base=Decimal("100")),
    UnitSeed("SQM", "Square Meter", "area"),
    UnitSeed("SQMM", "Square Millimeter", "area", base_unit_code="SQM", conversion_factor_to_base=Decimal("0.000001")),
    UnitSeed("SQCM", "Square Centimeter", "area", base_unit_code="SQM", conversion_factor_to_base=Decimal("0.000100")),
    UnitSeed("HA", "Hectare", "area", base_unit_code="SQM", conversion_factor_to_base=Decimal("10000")),
    UnitSeed("FLOZ", "Fluid Ounce", "volume"),
    UnitSeed("CUP", "Cup", "volume", base_unit_code="FLOZ", conversion_factor_to_base=Decimal("8")),
    UnitSeed("PT", "Pint", "volume", base_unit_code="FLOZ", conversion_factor_to_base=Decimal("16")),
    UnitSeed("QT", "Quart", "volume", base_unit_code="FLOZ", conversion_factor_to_base=Decimal("32")),
    UnitSeed("GAL", "Gallon", "volume", base_unit_code="FLOZ", conversion_factor_to_base=Decimal("128")),
    UnitSeed("CUIN", "Cubic Inch", "volume"),
    UnitSeed("CUFT", "Cubic Foot", "volume", base_unit_code="CUIN", conversion_factor_to_base=Decimal("1728")),
    UnitSeed("CUYD", "Cubic Yard", "volume", base_unit_code="CUIN", conversion_factor_to_base=Decimal("46656")),
    UnitSeed("BF", "Board Foot", "volume", base_unit_code="CUIN", conversion_factor_to_base=Decimal("144")),
    UnitSeed("ML", "Milliliter", "volume"),
    UnitSeed("L", "Liter", "volume", base_unit_code="ML", conversion_factor_to_base=Decimal("1000")),
    UnitSeed("CUCM", "Cubic Centimeter", "volume", base_unit_code="ML", conversion_factor_to_base=Decimal("1")),
    UnitSeed("CUM", "Cubic Meter", "volume", base_unit_code="ML", conversion_factor_to_base=Decimal("1000000")),
    UnitSeed("OZ", "Ounce", "weight"),
    UnitSeed("LB", "Pound", "weight", base_unit_code="OZ", conversion_factor_to_base=Decimal("16")),
    UnitSeed("TON_US", "US Short Ton", "weight", base_unit_code="LB", conversion_factor_to_base=Decimal("2000")),
    UnitSeed("G", "Gram", "weight"),
    UnitSeed("KG", "Kilogram", "weight", base_unit_code="G", conversion_factor_to_base=Decimal("1000")),
    UnitSeed("TONNE", "Metric Tonne", "weight", base_unit_code="KG", conversion_factor_to_base=Decimal("1000")),
)


def validate_seed_data() -> None:
    seen_codes: set[str] = set()

    for unit in DEFAULT_UNITS:
        if unit.code in seen_codes:
            raise ValueError(f"Duplicate seed unit code: {unit.code}")

        seen_codes.add(unit.code)

        if not unit.code or not unit.name or not unit.unit_type:
            raise ValueError(f"Seed unit is missing a required field: {unit.code}")

        if unit.code in PACKAGING_UNIT_CODES:
            if unit.base_unit_code is not None or unit.conversion_factor_to_base is not None:
                raise ValueError(f"Packaging unit must not define a conversion: {unit.code}")

        if unit.base_unit_code == unit.code:
            raise ValueError(f"Seed unit cannot use itself as a base unit: {unit.code}")


def format_codes(codes: list[str]) -> str:
    return ", ".join(codes) if codes else "(none)"


def run_seed(*, apply: bool) -> int:
    validate_seed_data()

    seed_codes = [unit.code for unit in DEFAULT_UNITS]
    inserted_codes: list[str] = []
    existing_codes: list[str] = []
    skipped_codes: list[str] = []

    session = SessionLocal()
    try:
        existing_units = session.execute(
            select(UnitOfMeasure).where(UnitOfMeasure.code.in_(seed_codes))
        ).scalars()
        units_by_code = {unit.code: unit for unit in existing_units}
        available_codes = set(units_by_code)

        for unit_seed in DEFAULT_UNITS:
            if unit_seed.code in units_by_code:
                existing_codes.append(unit_seed.code)
                continue

            base_unit_id = None
            if unit_seed.base_unit_code is not None:
                if unit_seed.base_unit_code not in available_codes:
                    skipped_codes.append(unit_seed.code)
                    continue

                if apply:
                    base_unit = units_by_code.get(unit_seed.base_unit_code)
                    if base_unit is None:
                        skipped_codes.append(unit_seed.code)
                        continue
                    base_unit_id = base_unit.id

            if not apply:
                inserted_codes.append(unit_seed.code)
                available_codes.add(unit_seed.code)
                continue

            unit = UnitOfMeasure(
                code=unit_seed.code,
                name=unit_seed.name,
                unit_type=unit_seed.unit_type,
                base_unit_id=base_unit_id,
                conversion_factor_to_base=unit_seed.conversion_factor_to_base,
                is_active=unit_seed.is_active,
            )
            session.add(unit)
            session.flush()

            units_by_code[unit.code] = unit
            available_codes.add(unit.code)
            inserted_codes.append(unit.code)

        if apply:
            session.commit()
        else:
            session.rollback()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    insert_label = "Inserted" if apply else "Would insert"
    print(f"Mode: {'apply' if apply else 'dry-run'}")
    print(f"{insert_label} ({len(inserted_codes)}): {format_codes(inserted_codes)}")
    print(f"Existing ({len(existing_codes)}): {format_codes(existing_codes)}")
    print(f"Skipped ({len(skipped_codes)}): {format_codes(skipped_codes)}")

    if not apply:
        print("No database changes committed.")

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed reviewed default units of measure.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview units without writing data.")
    mode.add_argument("--apply", action="store_true", help="Insert missing default units.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_seed(apply=args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
