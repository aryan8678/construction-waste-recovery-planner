import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.assessment import WasteInput
from app.ml.preprocessor import extract_features_from_input
from app.ml.model_adapter import evaluate_waste_ml, get_model_status
from app.ml.config import ALL_FEATURE_COLUMNS, TARGET_CLASSES

client = TestClient(app)

def test_feature_extraction():
    inp = WasteInput(
        material="Concrete",
        condition="Damaged",
        contamination="None",
        quantity=500.0,
        unit="kg",
        additional_characteristics={"cracks": "Moderate", "structural_integrity": "Compromised"}
    )
    features = extract_features_from_input(inp)

    assert features["material"] == "Concrete"
    assert features["condition"] == "Damaged"
    assert features["quantity"] == 500.0
    assert features["has_cracks"] == 1.0
    assert features["structural_compromised"] == 1.0
    assert features["condition_score"] == 1.0
    assert features["contamination_score"] == 0.0

    # Check all required feature columns exist in extracted dict
    for col in ALL_FEATURE_COLUMNS:
        assert col in features

def test_ml_adapter_fallback_probabilities():
    """
    Ensures that even before user places a trained .joblib model,
    the adapter yields a valid AssessmentResult with ML probabilities summing to ~1.0
    """
    inp = WasteInput(
        material="Concrete",
        condition="Damaged",
        contamination="None",
        quantity=500.0,
        unit="kg",
        additional_characteristics={"cracks": "Moderate"}
    )
    result = evaluate_waste_ml(inp)

    assert result.recommended_pathway in TARGET_CLASSES
    assert result.confidence_score is not None
    assert 0.0 <= result.confidence_score <= 1.0
    assert result.prediction_probabilities is not None

    # Check probability sum is approximately 1.0
    prob_sum = sum(result.prediction_probabilities.values())
    assert abs(prob_sum - 1.0) < 0.05
    assert "RECYCLE" in result.prediction_probabilities

def test_ml_adapter_safety_override_hazardous():
    """
    Hazardous contamination must trigger safety override to specialized handling.
    """
    inp = WasteInput(
        material="Wood",
        condition="Good",
        contamination="Hazardous",
        quantity=200.0,
        unit="kg"
    )
    result = evaluate_waste_ml(inp)
    assert "DISPOSAL" in result.recommended_pathway
    assert result.professional_assessment_required is True

def test_ml_status_endpoint():
    res = client.get("/api/ml/status")
    assert res.status_code == 200
    data = res.json()
    assert "model_file_exists" in data
    assert "target_classes" in data
    assert "required_feature_columns" in data
    assert len(data["target_classes"]) == 5

def test_api_analyze_with_ml():
    payload = {
        "material": "Brick",
        "condition": "Good",
        "contamination": "None",
        "quantity": 350,
        "unit": "kg",
        "additional_characteristics": {
            "broken_percentage": 5
        }
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "confidence_score" in data
    assert "prediction_probabilities" in data
    assert data["confidence_score"] > 0
    assert data["recommended_pathway"] in TARGET_CLASSES
