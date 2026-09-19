"""
Feature Engineering and Preprocessing Pipeline.
Transforms WasteInput into structured feature dictionaries and matrices
ready for Machine Learning model inference or dataset construction.
"""

from typing import Dict, Any, List
import math
from app.schemas.assessment import WasteInput
from app.ml.config import (
    CONDITION_ORDINAL_MAP,
    CONTAMINATION_ORDINAL_MAP,
    ALL_FEATURE_COLUMNS,
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES
)

def extract_features_from_input(waste_input: WasteInput) -> Dict[str, Any]:
    """
    Extracts numerical and categorical features from a WasteInput instance.
    Includes feature engineering from additional_characteristics.
    """
    material = str(waste_input.material or "Mixed Construction Waste").strip()
    condition = str(waste_input.condition or "Moderate").strip()
    contamination = str(waste_input.contamination or "None").strip()
    unit = str(waste_input.unit or "kg").strip()
    quantity = float(waste_input.quantity if waste_input.quantity and waste_input.quantity > 0 else 1.0)
    chars = waste_input.additional_characteristics or {}

    # Ordinal scores
    condition_score = CONDITION_ORDINAL_MAP.get(condition, 2.0)
    contamination_score = CONTAMINATION_ORDINAL_MAP.get(contamination, 0.0)

    # Domain flags extracted from characteristics
    # Cracks
    has_cracks = 0.0
    crack_val = str(chars.get("cracks", "")).lower()
    if crack_val in ["moderate", "severe", "compromised", "yes", "extensive"]:
        has_cracks = 1.0

    # Structural Integrity
    struct_val = str(chars.get("structural_integrity", "")).lower()
    structural_compromised = 1.0 if struct_val in ["compromised", "deformed", "failed", "unsafe"] else 0.0

    # Broken percentage
    broken_pct = 0.0
    try:
        if "broken_percentage" in chars:
            broken_pct = float(chars["broken_percentage"])
        elif "intact_percentage" in chars:
            broken_pct = max(0.0, 100.0 - float(chars["intact_percentage"]))
    except (ValueError, TypeError):
        broken_pct = 0.0

    # Rust
    rust_val = str(chars.get("rust_level", "")).lower()
    has_rust = 1.0 if rust_val in ["moderate", "heavy", "severe", "pitted", "yes"] else 0.0

    # Rot
    rot_val = str(chars.get("rot", "")).lower()
    has_rot = 1.0 if rot_val in ["yes", "moderate", "severe", "dry rot", "wet rot"] else 0.0

    # Moisture
    moist_val = str(chars.get("moisture", "")).lower() + " " + str(chars.get("wet", "")).lower()
    is_moist = 1.0 if any(term in moist_val for term in ["wet", "moist", "high", "yes", "saturated"]) else 0.0

    # Hazardous Coating
    paint_val = str(chars.get("paint_coating", "")).lower() + " " + str(chars.get("foreign_contaminants", "")).lower()
    has_hazardous_coating = 1.0 if any(term in paint_val for term in ["lead", "creosote", "chemical", "asbestos", "toxic"]) else 0.0

    # Separability
    sep_val = str(chars.get("separable_on_site", "yes")).lower()
    is_separable = 1.0 if sep_val not in ["no", "false", "inseparable"] else 0.0

    features: Dict[str, Any] = {
        "material": material,
        "condition": condition,
        "contamination": contamination,
        "unit": unit,
        "quantity": quantity,
        "broken_percentage": float(broken_pct),
        "condition_score": float(condition_score),
        "contamination_score": float(contamination_score),
        "has_cracks": float(has_cracks),
        "structural_compromised": float(structural_compromised),
        "has_rust": float(has_rust),
        "has_rot": float(has_rot),
        "is_moist": float(is_moist),
        "has_hazardous_coating": float(has_hazardous_coating),
        "is_separable": float(is_separable)
    }

    return features

def features_to_input_dataframe(features_dict: Dict[str, Any]):
    """
    Converts features dictionary into a Pandas DataFrame matching the training schema.
    If pandas is available, returns a DataFrame; otherwise returns list of dicts.
    """
    try:
        import pandas as pd
        df = pd.DataFrame([features_dict], columns=ALL_FEATURE_COLUMNS)
        return df
    except ImportError:
        return [features_dict]
