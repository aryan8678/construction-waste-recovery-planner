"""
Sample Dataset Generator for Construction Waste Recovery Planning.
Creates a comprehensive, realistic reference dataset covering all 11 material types,
various degradation stages, contamination levels, and all 5 recovery pathways.
"""

import os
import csv
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = DATA_DIR / "sample_waste_dataset.csv"

MATERIALS = [
    "Concrete", "Brick", "Steel", "Wood", "Glass", "Plastic",
    "Gypsum", "Asphalt", "Soil", "Ceramic / Tiles", "Mixed Construction Waste"
]

CONDITIONS = ["Excellent", "Good", "Moderate", "Damaged", "Severely Damaged"]
CONTAMINATIONS = ["None", "Low", "Moderate", "High", "Hazardous"]
UNITS = ["kg", "tonnes", "units", "cubic metres"]

ORDINAL_COND = {"Excellent": 4.0, "Good": 3.0, "Moderate": 2.0, "Damaged": 1.0, "Severely Damaged": 0.0}
ORDINAL_CONT = {"None": 0.0, "Low": 1.0, "Moderate": 2.0, "High": 3.0, "Hazardous": 4.0}

def generate_row(idx: int):
    material = random.choice(MATERIALS)
    condition = random.choice(CONDITIONS)
    contamination = random.choice(CONTAMINATIONS)
    unit = random.choice(UNITS)
    quantity = round(random.uniform(50.0, 5000.0), 1)

    cond_score = ORDINAL_COND[condition]
    cont_score = ORDINAL_CONT[contamination]

    has_cracks = 1.0 if (condition in ["Damaged", "Severely Damaged"] and random.random() > 0.2) else (1.0 if condition == "Moderate" and random.random() > 0.7 else 0.0)
    struct_comp = 1.0 if (condition in ["Damaged", "Severely Damaged"] and random.random() > 0.35) else 0.0
    broken_pct = (
        round(random.uniform(50.0, 95.0), 1) if condition == "Severely Damaged" else
        round(random.uniform(20.0, 55.0), 1) if condition == "Damaged" else
        round(random.uniform(5.0, 25.0), 1) if condition == "Moderate" else
        round(random.uniform(0.0, 8.0), 1)
    )
    has_rust = 1.0 if (material == "Steel" and condition in ["Moderate", "Damaged", "Severely Damaged"] and random.random() > 0.25) else 0.0
    has_rot = 1.0 if (material == "Wood" and condition in ["Damaged", "Severely Damaged"] and random.random() > 0.3) else 0.0
    is_moist = 1.0 if (material in ["Gypsum", "Wood", "Soil"] and random.random() > 0.5) else (1.0 if random.random() > 0.88 else 0.0)
    has_hazardous_coating = 1.0 if (contamination in ["High", "Hazardous"] and random.random() > 0.4) else 0.0
    is_separable = 1.0 if (material != "Mixed Construction Waste") else (1.0 if random.random() > 0.35 else 0.0)

    # Ground truth circular pathway labeling logic (BS EN ISO 59010:2024 hierarchy)
    # Priority 1: Safety guardrail
    if contamination == "Hazardous" or cont_score >= 4.0 or has_hazardous_coating == 1.0:
        target = "DISPOSAL / SPECIALIZED HANDLING"
    # Priority 2: REUSE - high condition, clean, intact geometry
    elif cond_score >= 3.0 and cont_score == 0.0 and broken_pct < 10.0 and struct_comp == 0.0 and has_cracks == 0.0 and has_rust == 0.0 and has_rot == 0.0:
        target = "REUSE"
    # Priority 3: REPAIR - repairable materials with localized/superficial damage
    elif material in ["Steel", "Wood", "Brick", "Glass", "Ceramic / Tiles", "Concrete"] and cond_score >= 2.0 and cont_score <= 1.0 and broken_pct < 40.0 and (has_rust or struct_comp or has_cracks or has_rot):
        target = "REPAIR"
    # Priority 4: Good moderate-condition clean material
    elif cond_score >= 2.0 and cont_score == 0.0 and broken_pct < 20.0:
        target = "REUSE"
    # Priority 5: RECOVER - combustible/energy-recoverable with moderate contamination
    elif material in ["Wood", "Plastic", "Asphalt", "Mixed Construction Waste", "Gypsum"] and cont_score <= 2.0 and cond_score <= 2.0:
        target = "RECOVER"
    # Priority 6: RECYCLE - damaged but acceptably clean
    elif cont_score <= 2.0 and not has_hazardous_coating:
        target = "RECYCLE"
    else:
        target = "DISPOSAL / SPECIALIZED HANDLING"

    return {
        "material": material,
        "condition": condition,
        "contamination": contamination,
        "unit": unit,
        "quantity": quantity,
        "broken_percentage": broken_pct,
        "condition_score": cond_score,
        "contamination_score": cont_score,
        "has_cracks": has_cracks,
        "structural_compromised": struct_comp,
        "has_rust": has_rust,
        "has_rot": has_rot,
        "is_moist": is_moist,
        "has_hazardous_coating": has_hazardous_coating,
        "is_separable": is_separable,
        "recommended_pathway": target
    }

def generate_targeted_row(target_class: str, rng: random.Random) -> dict:
    """Generate a row guaranteed to belong to a specific target class."""
    if target_class == "REUSE":
        material = rng.choice(["Concrete", "Brick", "Steel", "Glass", "Ceramic / Tiles"])
        condition = rng.choice(["Excellent", "Good"])
        contamination = "None"
        cond_score = ORDINAL_COND[condition]
        cont_score = 0.0
        broken_pct = round(rng.uniform(0.0, 8.0), 1)
        has_cracks = 0.0; struct_comp = 0.0; has_rust = 0.0; has_rot = 0.0
        is_moist = 0.0; has_hazardous_coating = 0.0; is_separable = 1.0
    elif target_class == "REPAIR":
        material = rng.choice(["Steel", "Wood", "Brick", "Glass", "Ceramic / Tiles", "Concrete"])
        condition = rng.choice(["Good", "Moderate", "Damaged"])
        contamination = rng.choice(["None", "Low"])
        cond_score = ORDINAL_COND[condition]
        cont_score = ORDINAL_CONT[contamination]
        broken_pct = round(rng.uniform(5.0, 35.0), 1)
        # Ensure at least one damage flag for repairability
        has_cracks = 1.0 if material in ["Concrete", "Brick", "Glass"] else (1.0 if rng.random() > 0.4 else 0.0)
        struct_comp = 1.0 if condition == "Damaged" and rng.random() > 0.5 else 0.0
        has_rust = 1.0 if material == "Steel" and rng.random() > 0.2 else 0.0
        has_rot = 1.0 if material == "Wood" and condition == "Damaged" and rng.random() > 0.3 else 0.0
        # Guarantee at least one flag
        if not (has_cracks or struct_comp or has_rust or has_rot):
            has_cracks = 1.0
        is_moist = 0.0; has_hazardous_coating = 0.0; is_separable = 1.0
    elif target_class == "RECYCLE":
        material = rng.choice(["Concrete", "Brick", "Glass", "Soil", "Asphalt", "Gypsum"])
        condition = rng.choice(["Moderate", "Damaged", "Severely Damaged"])
        contamination = rng.choice(["None", "Low", "Moderate"])
        cond_score = ORDINAL_COND[condition]
        cont_score = ORDINAL_CONT[contamination]
        broken_pct = round(rng.uniform(25.0, 80.0), 1)
        has_cracks = 1.0 if condition != "Excellent" and rng.random() > 0.4 else 0.0
        struct_comp = 1.0 if condition in ["Damaged", "Severely Damaged"] and rng.random() > 0.5 else 0.0
        has_rust = 0.0; has_rot = 0.0
        is_moist = 1.0 if material in ["Gypsum", "Soil"] and rng.random() > 0.5 else 0.0
        has_hazardous_coating = 0.0; is_separable = 1.0
    elif target_class == "RECOVER":
        material = rng.choice(["Wood", "Plastic", "Asphalt", "Mixed Construction Waste", "Gypsum"])
        condition = rng.choice(["Moderate", "Damaged", "Severely Damaged"])
        contamination = rng.choice(["Low", "Moderate"])
        cond_score = ORDINAL_COND[condition]
        cont_score = ORDINAL_CONT[contamination]
        broken_pct = round(rng.uniform(20.0, 75.0), 1)
        has_cracks = 0.0; struct_comp = 0.0
        has_rust = 0.0
        has_rot = 1.0 if material == "Wood" and rng.random() > 0.5 else 0.0
        is_moist = 1.0 if material in ["Wood", "Gypsum"] and rng.random() > 0.5 else 0.0
        has_hazardous_coating = 0.0; is_separable = 1.0 if material != "Mixed Construction Waste" else (1.0 if rng.random() > 0.3 else 0.0)
    else:  # DISPOSAL / SPECIALIZED HANDLING
        material = rng.choice(MATERIALS)
        condition = rng.choice(CONDITIONS)
        contamination = rng.choice(["Hazardous", "High"])
        cond_score = ORDINAL_COND[condition]
        cont_score = ORDINAL_CONT[contamination]
        broken_pct = round(rng.uniform(0.0, 90.0), 1)
        has_cracks = 1.0 if rng.random() > 0.5 else 0.0
        struct_comp = 1.0 if rng.random() > 0.5 else 0.0
        has_rust = 1.0 if material == "Steel" else 0.0
        has_rot = 0.0; is_moist = 0.0
        has_hazardous_coating = 1.0; is_separable = 0.0

    unit = rng.choice(UNITS)
    quantity = round(rng.uniform(50.0, 8000.0), 1)

    return {
        "material": material,
        "condition": condition,
        "contamination": contamination,
        "unit": unit,
        "quantity": quantity,
        "broken_percentage": broken_pct,
        "condition_score": cond_score,
        "contamination_score": cont_score,
        "has_cracks": has_cracks,
        "structural_compromised": struct_comp,
        "has_rust": has_rust,
        "has_rot": has_rot,
        "is_moist": is_moist,
        "has_hazardous_coating": has_hazardous_coating,
        "is_separable": is_separable,
        "recommended_pathway": target_class
    }


def main():
    rng = random.Random(42)
    rows = []

    # Stratified generation: 600 samples per class (balanced = 3000 total)
    TARGET_CLASSES = ["REUSE", "REPAIR", "RECYCLE", "RECOVER", "DISPOSAL / SPECIALIZED HANDLING"]
    per_class = 600

    for target_cls in TARGET_CLASSES:
        for _ in range(per_class):
            rows.append(generate_targeted_row(target_cls, rng))

    # Shuffle to avoid order bias during training
    rng.shuffle(rows)

    fieldnames = list(rows[0].keys())
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated reference dataset with {len(rows)} samples.")
    print(f"Saved to: {OUTPUT_CSV}")

    # Print distribution
    from collections import Counter
    dist = Counter(r["recommended_pathway"] for r in rows)
    for cls, cnt in sorted(dist.items()):
        print(f"  {cls:<40}: {cnt:>4} ({cnt/len(rows)*100:.1f}%)")


if __name__ == "__main__":
    main()

