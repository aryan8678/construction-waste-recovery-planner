"""
ML Model Diagnostic and Status API Router.
Provides real-time inspection of ML model artifact availability,
required feature schema, active model engine, and user training instructions.
"""

from fastapi import APIRouter
from app.ml.model_adapter import get_model_status

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

@router.get("/status")
def check_ml_status():
    """
    Returns diagnostic details about the currently loaded Machine Learning model,
    including file path, whether user-trained model artifact is active,
    required input features, and target classes.
    """
    return get_model_status()
