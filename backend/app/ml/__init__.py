"""
Machine Learning Module for Construction Waste Recovery Planner.
Provides feature preprocessing, model loading, probabilistic inference,
fallback decision engine, and training templates.
"""

from app.ml.config import TARGET_CLASSES, ALL_FEATURE_COLUMNS, DEFAULT_MODEL_FILE
from app.ml.model_adapter import evaluate_waste_ml, get_model_status

__all__ = [
    "TARGET_CLASSES",
    "ALL_FEATURE_COLUMNS",
    "DEFAULT_MODEL_FILE",
    "evaluate_waste_ml",
    "get_model_status"
]
