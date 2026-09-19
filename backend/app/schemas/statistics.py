from typing import Dict, List, Any
from pydantic import BaseModel

class StatisticsResponse(BaseModel):
    total_assessments: int
    pathway_counts: Dict[str, int]
    material_counts: Dict[str, int]
    condition_counts: Dict[str, int]
    recent_assessments: List[Dict[str, Any]]
