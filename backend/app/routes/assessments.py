import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.session import get_db
from app.models.assessment import Assessment
from app.schemas.assessment import (
    WasteInput,
    AssessmentResult,
    AssessmentRecord
)
from app.rules.engine import evaluate_waste
from app.ml.model_adapter import evaluate_waste_ml

router = APIRouter(prefix="/api", tags=["Assessments"])

@router.post("/analyze", response_model=AssessmentResult)
def analyze_waste(waste_input: WasteInput, db: Session = Depends(get_db)):
    """
    Executes the Machine Learning decision support engine on waste characteristics,
    evaluates environmental safety constraints, persists the assessment in SQLite,
    and returns comprehensive explainable results with prediction probabilities.
    """
    result = evaluate_waste_ml(waste_input)

    db_assessment = Assessment(
        material=waste_input.material,
        condition=waste_input.condition,
        contamination=waste_input.contamination,
        quantity=waste_input.quantity,
        unit=waste_input.unit,
        additional_characteristics=json.dumps(waste_input.additional_characteristics or {}),
        recommended_pathway=result.recommended_pathway,
        reason=result.reason,
        matched_rule=result.matched_rule,
        rule_match_strength=result.rule_match_strength,
        applications=json.dumps(result.potential_applications),
        alternatives=json.dumps(result.alternative_options),
        decision_path=json.dumps([s.model_dump() for s in result.decision_steps]),
        sustainability=json.dumps(result.sustainability.model_dump()),
        confidence_score=result.confidence_score,
        model_version=result.model_version,
        prediction_probabilities=json.dumps(result.prediction_probabilities or {}),
        decision_source=result.inference_source or "ML Model"
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)

    result.id = db_assessment.id
    return result

@router.get("/assessments", response_model=List[AssessmentRecord])
def list_assessments(
    material: Optional[str] = None,
    pathway: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Assessment).order_by(desc(Assessment.timestamp))

    if material:
        query = query.filter(Assessment.material.ilike(f"%{material}%"))
    if pathway:
        query = query.filter(Assessment.recommended_pathway.ilike(f"%{pathway}%"))

    records = query.all()
    results = []
    for r in records:
        try:
            apps = json.loads(r.applications or "[]")
        except Exception:
            apps = []
        try:
            alts = json.loads(r.alternatives or "[]")
        except Exception:
            alts = []

        if search:
            s_lower = search.lower()
            if not (s_lower in r.material.lower() or s_lower in r.recommended_pathway.lower() or s_lower in (r.matched_rule or "").lower() or s_lower in r.reason.lower()):
                continue

        results.append(AssessmentRecord(
            id=r.id,
            timestamp=r.timestamp,
            material=r.material,
            condition=r.condition,
            contamination=r.contamination,
            quantity=r.quantity,
            unit=r.unit,
            recommended_pathway=r.recommended_pathway,
            matched_rule=r.matched_rule or "ML Model",
            reason=r.reason,
            applications=apps,
            alternatives=alts,
            confidence_score=r.confidence_score,
            model_version=r.model_version
        ))

    return results

@router.get("/assessments/{assessment_id}", response_model=AssessmentResult)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    rec = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Assessment not found")

    try:
        chars = json.loads(rec.additional_characteristics or "{}")
    except Exception:
        chars = {}

    input_obj = WasteInput(
        material=rec.material,
        condition=rec.condition,
        contamination=rec.contamination,
        quantity=rec.quantity,
        unit=rec.unit,
        additional_characteristics=chars
    )

    result = evaluate_waste_ml(input_obj)
    result.id = rec.id
    result.timestamp = rec.timestamp
    if rec.confidence_score is not None:
        result.confidence_score = rec.confidence_score
    if rec.model_version:
        result.model_version = rec.model_version
    if rec.prediction_probabilities:
        try:
            result.prediction_probabilities = json.loads(rec.prediction_probabilities)
        except Exception:
            pass
    return result

@router.delete("/assessments/{assessment_id}")
def delete_assessment(assessment_id: int, db: Session = Depends(get_db)):
    rec = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Assessment not found")

    db.delete(rec)
    db.commit()
    return {"status": "success", "message": f"Assessment {assessment_id} deleted successfully"}
