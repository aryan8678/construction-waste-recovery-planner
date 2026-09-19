import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.rule import Rule
from app.schemas.rule import RuleResponse

router = APIRouter(prefix="/api", tags=["Rules"])

@router.get("/rules", response_model=List[RuleResponse])
def list_rules(
    material: Optional[str] = None,
    pathway: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Rule)
    if material:
        query = query.filter(Rule.material.ilike(f"%{material}%"))
    if pathway:
        query = query.filter(Rule.pathway.ilike(f"%{pathway}%"))

    rules = query.order_by(Rule.material, Rule.priority).all()
    results = []
    for r in rules:
        try:
            apps = json.loads(r.applications or "[]")
        except Exception:
            apps = []
        try:
            alts = json.loads(r.alternatives or "[]")
        except Exception:
            alts = []

        results.append(RuleResponse(
            id=r.id,
            rule_id=r.rule_id,
            material=r.material,
            pathway=r.pathway,
            priority=r.priority,
            conditions_description=r.conditions_description,
            reason=r.reason,
            applications=apps,
            alternatives=alts
        ))
    return results

@router.get("/rules/{rule_id}", response_model=RuleResponse)
def get_rule(rule_id: str, db: Session = Depends(get_db)):
    r = db.query(Rule).filter(Rule.rule_id.ilike(rule_id)).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rule not found")

    try:
        apps = json.loads(r.applications or "[]")
    except Exception:
        apps = []
    try:
        alts = json.loads(r.alternatives or "[]")
    except Exception:
        alts = []

    return RuleResponse(
        id=r.id,
        rule_id=r.rule_id,
        material=r.material,
        pathway=r.pathway,
        priority=r.priority,
        conditions_description=r.conditions_description,
        reason=r.reason,
        applications=apps,
        alternatives=alts
    )
