from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, ConfigDict

class WasteInput(BaseModel):
    material: str = Field(..., description="Material type (e.g. Concrete, Brick, Steel, etc.)")
    condition: str = Field(..., description="Condition: Excellent, Good, Moderate, Damaged, Severely Damaged")
    contamination: str = Field(..., description="Contamination: None, Low, Moderate, High, Hazardous")
    quantity: float = Field(..., gt=0, description="Quantity must be greater than zero")
    unit: str = Field(..., description="Unit: kg, tonnes, units, cubic metres")
    additional_characteristics: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @field_validator("material")
    def validate_material(cls, v):
        if not v or not v.strip():
            raise ValueError("Material type cannot be empty")
        return v.strip()

    @field_validator("quantity")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

class DecisionStep(BaseModel):
    stage: str
    title: str
    description: str
    status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class HierarchyEvaluation(BaseModel):
    tier: str
    name: str
    selected: bool
    status: str
    reason: str

class SustainabilityAssessment(BaseModel):
    landfill_avoidance: str
    material_recovery: str
    resource_conservation: str
    circularity_potential: str
    assessment_type: str = "Qualitative sustainability assessment"
    note: str = "Indicative assessment for prototype demonstration."

class AssessmentResult(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    input_summary: WasteInput
    recommended_pathway: str
    rule_match_strength: str = "Strong Rule Match"
    matched_rule: str
    reason: str
    conditions_satisfied: List[str]
    potential_applications: List[str]
    alternative_options: List[str]
    decision_steps: List[DecisionStep]
    hierarchy_evaluation: List[HierarchyEvaluation]
    sustainability: SustainabilityAssessment
    safety_disclaimer: str
    professional_assessment_required: bool = False
    confidence_score: Optional[float] = None
    prediction_probabilities: Optional[Dict[str, float]] = None
    model_name: Optional[str] = "ML Classifier"
    model_version: Optional[str] = "v1.0"
    inference_source: Optional[str] = "ML Model"

class AssessmentRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    material: str
    condition: str
    contamination: str
    quantity: float
    unit: str
    recommended_pathway: str
    matched_rule: str
    reason: str
    applications: List[str]
    alternatives: List[str]
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None
