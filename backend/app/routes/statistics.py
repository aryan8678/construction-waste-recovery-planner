import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.session import get_db
from app.models.assessment import Assessment
from app.schemas.statistics import StatisticsResponse

router = APIRouter(prefix="/api", tags=["Statistics"])

@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    all_assessments = db.query(Assessment).order_by(desc(Assessment.timestamp)).all()
    total = len(all_assessments)

    # Initialize pathway counts with all 5 tiers
    pathways = {
        "REUSE": 0,
        "REPAIR": 0,
        "RECYCLE": 0,
        "RECOVER": 0,
        "DISPOSE": 0
    }
    materials: dict = {}
    conditions: dict = {}

    for a in all_assessments:
        # Normalize pathway key for chart consistency
        p = a.recommended_pathway.upper()
        if "REUSE" in p:
            pathways["REUSE"] += 1
        elif "REPAIR" in p:
            pathways["REPAIR"] += 1
        elif "RECYCLE" in p:
            pathways["RECYCLE"] += 1
        elif "RECOVER" in p:
            pathways["RECOVER"] += 1
        else:
            pathways["DISPOSE"] += 1

        materials[a.material] = materials.get(a.material, 0) + 1
        conditions[a.condition] = conditions.get(a.condition, 0) + 1

    recent = []
    for a in all_assessments[:5]:
        recent.append({
            "id": a.id,
            "timestamp": a.timestamp.isoformat(),
            "material": a.material,
            "quantity": a.quantity,
            "unit": a.unit,
            "condition": a.condition,
            "contamination": a.contamination,
            "pathway": a.recommended_pathway,
            "matched_rule": a.matched_rule
        })

    return StatisticsResponse(
        total_assessments=total,
        pathway_counts=pathways,
        material_counts=materials,
        condition_counts=conditions,
        recent_assessments=recent
    )
