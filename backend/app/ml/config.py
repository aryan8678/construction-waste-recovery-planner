import os
from pathlib import Path
from typing import List, Dict

# Base directory for the backend app
ML_DIR = Path(__file__).resolve().parent
SAVED_MODELS_DIR = ML_DIR / "saved_models"
DATA_DIR = ML_DIR / "data"

# Ensure directories exist
SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Default model artifact path
DEFAULT_MODEL_FILE = SAVED_MODELS_DIR / "waste_recovery_model.joblib"
METADATA_FILE = SAVED_MODELS_DIR / "model_metadata.json"

# Target classes matching the 5 circular waste hierarchy pathways
TARGET_CLASSES: List[str] = [
    "REUSE",
    "REPAIR",
    "RECYCLE",
    "RECOVER",
    "DISPOSAL / SPECIALIZED HANDLING"
]

# Canonical material categories
MATERIAL_CATEGORIES: List[str] = [
    "Concrete",
    "Brick",
    "Steel",
    "Wood",
    "Glass",
    "Plastic",
    "Gypsum",
    "Asphalt",
    "Soil",
    "Ceramic / Tiles",
    "Mixed Construction Waste"
]

# Condition categories (Ordinal / Categorical)
CONDITION_CATEGORIES: List[str] = [
    "Excellent",
    "Good",
    "Moderate",
    "Damaged",
    "Severely Damaged"
]

# Contamination categories (Ordinal / Categorical)
CONTAMINATION_CATEGORIES: List[str] = [
    "None",
    "Low",
    "Moderate",
    "High",
    "Hazardous"
]

# Measurement units
UNIT_CATEGORIES: List[str] = [
    "kg",
    "tonnes",
    "units",
    "cubic metres"
]

# Standard Tabular Feature Names for the ML Model Matrix
CATEGORICAL_FEATURES: List[str] = [
    "material",
    "condition",
    "contamination",
    "unit"
]

NUMERICAL_FEATURES: List[str] = [
    "quantity",
    "broken_percentage",
    "condition_score",
    "contamination_score",
    "has_cracks",
    "structural_compromised",
    "has_rust",
    "has_rot",
    "is_moist",
    "has_hazardous_coating",
    "is_separable"
]

ALL_FEATURE_COLUMNS: List[str] = CATEGORICAL_FEATURES + NUMERICAL_FEATURES

# Ordinal score mappings for feature engineering
CONDITION_ORDINAL_MAP: Dict[str, float] = {
    "Excellent": 4.0,
    "Good": 3.0,
    "Moderate": 2.0,
    "Damaged": 1.0,
    "Severely Damaged": 0.0
}

CONTAMINATION_ORDINAL_MAP: Dict[str, float] = {
    "None": 0.0,
    "Low": 1.0,
    "Moderate": 2.0,
    "High": 3.0,
    "Hazardous": 4.0
}
