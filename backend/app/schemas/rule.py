from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class RuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    rule_id: str
    material: str
    pathway: str
    priority: int
    conditions_description: str
    reason: str
    applications: List[str]
    alternatives: List[str]
