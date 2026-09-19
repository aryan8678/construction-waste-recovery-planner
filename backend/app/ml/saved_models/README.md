# Saved Models Directory

This directory is the designated storage location for your trained Machine Learning model.

## Target Model Artifact:
- **Filename**: `waste_recovery_model.joblib`
- **Path**: `backend/app/ml/saved_models/waste_recovery_model.joblib`

## Expected Model Interface:
The model should be a serialized Python object (typically a Scikit-Learn `Pipeline`, `RandomForestClassifier`, `XGBClassifier`, or `GradientBoostingClassifier`) that implements:
1. `predict(X)`: returns the predicted pathway string (one of the 5 canonical classes).
2. `predict_proba(X)`: returns class probabilities summing to 1.0.

## 5 Target Canonical Classes:
1. `REUSE`
2. `REPAIR`
3. `RECYCLE`
4. `RECOVER`
5. `DISPOSAL / SPECIALIZED HANDLING`

## Optional Metadata File:
You can also place a `model_metadata.json` file in this directory to display custom info in the UI:
```json
{
  "model_name": "RandomForestClassifier",
  "version": "1.0.0",
  "accuracy": 0.942,
  "trained_on": "2026-09-18",
  "features_count": 15
}
```

## How to train:
Run the provided training script template from the project root:
```bash
python backend/app/ml/train_template.py
```
This script will train on your CSV dataset, evaluate metrics, and automatically export `waste_recovery_model.joblib` and `model_metadata.json` directly into this folder!
