import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.material import Material
from app.schemas.material import MaterialResponse

router = APIRouter(prefix="/api", tags=["Materials"])

@router.get("/materials", response_model=List[MaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    mats = db.query(Material).order_by(Material.name).all()
    results = []
    for m in mats:
        try:
            apps = json.loads(m.common_applications or "[]")
        except Exception:
            apps = []
        results.append(MaterialResponse(
            id=m.id,
            name=m.name,
            category=m.category,
            description=m.description,
            typical_waste_source=m.typical_waste_source,
            reuse_potential=m.reuse_potential,
            recycling_potential=m.recycling_potential,
            common_applications=apps,
            important_considerations=m.important_considerations
        ))
    return results

@router.get("/materials/{name}", response_model=MaterialResponse)
def get_material(name: str, db: Session = Depends(get_db)):
    m = db.query(Material).filter(Material.name.ilike(name)).first()
    if not m:
        raise HTTPException(status_code=404, detail="Material not found")
    try:
        apps = json.loads(m.common_applications or "[]")
    except Exception:
        apps = []
    return MaterialResponse(
        id=m.id,
        name=m.name,
        category=m.category,
        description=m.description,
        typical_waste_source=m.typical_waste_source,
        reuse_potential=m.reuse_potential,
        recycling_potential=m.recycling_potential,
        common_applications=apps,
        important_considerations=m.important_considerations
    )
