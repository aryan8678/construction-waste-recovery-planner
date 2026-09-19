from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class MaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    category: str
    description: str
    typical_waste_source: str
    reuse_potential: str
    recycling_potential: str
    common_applications: List[str]
    important_considerations: str
