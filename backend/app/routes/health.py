from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Construction Waste Recovery Planner API",
        "version": "1.0.0-academic",
        "mode": "deterministic-rule-engine",
        "ai_ml_enabled": False,
        "timestamp": datetime.utcnow().isoformat()
    }
