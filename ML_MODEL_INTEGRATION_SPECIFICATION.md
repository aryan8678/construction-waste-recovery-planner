# Machine Learning Model Integration Specification & Guide
**Construction Waste Recovery Planner**

---

## 1. Executive Summary: What Has Been Implemented

The Construction Waste Recovery Planner has been transitioned from a deterministic rule-based inference script into a **modular Machine Learning (ML) decision architecture**.

Per your instructions:
- **The ML model slot has been left modular and empty**: You can train your own model independently and drop it into the designated folder (`backend/app/ml/saved_models/waste_recovery_model.joblib`).
- **Zero downtime / Seamless operation**: When your trained model file is not yet present, a built-in probabilistic baseline adapter executes in place, calculating class probabilities, confidence scores, and circular hierarchy recommendations so that the entire frontend, API, database, and test suite work smoothly out of the box.
- **Input and output schemas are strictly defined**: All 15 tabular features, preprocessing steps, categorical mappings, and the 5 multi-class target pathways are standardized.
- **Frontend enhancements**: The UI now visualizes **ML Confidence Scores**, a **Multi-Class Probability Distribution Bar Chart** across all 5 circular pathways, dynamic model version badges, an **ML Model Architecture Status Card** on the Dashboard, and a modernized 5-stage ML inference pipeline.
- **Turnkey Training Template**: A ready-to-run training script (`backend/app/ml/train_template.py`) and reference dataset (`backend/app/ml/data/sample_waste_dataset.csv`) are provided for immediate training.

---

## 2. Defined Input Feature Schema

Every incoming assessment request (`WasteInput`) is extracted and converted into a **15-dimensional tabular feature vector** before being passed to the ML classifier.

### Feature Specification Table

| # | Feature Name | Data Type | Permissible / Example Values | Preprocessing / Encoding Method | Description |
|---|:---|:---:|:---|:---|:---|
| **1** | `material` | Categorical | `Concrete`, `Brick`, `Steel`, `Wood`, `Glass`, `Plastic`, `Gypsum`, `Asphalt`, `Soil`, `Ceramic / Tiles`, `Mixed Construction Waste` | One-Hot Encoded (`OneHotEncoder(handle_unknown='ignore')`) | Primary C&D waste material type |
| **2** | `condition` | Categorical | `Excellent`, `Good`, `Moderate`, `Damaged`, `Severely Damaged` | One-Hot Encoded | Reported physical condition |
| **3** | `contamination` | Categorical | `None`, `Low`, `Moderate`, `High`, `Hazardous` | One-Hot Encoded | Foreign substance / chemical contamination |
| **4** | `unit` | Categorical | `kg`, `tonnes`, `units`, `cubic metres` | One-Hot Encoded | Measurement unit |
| **5** | `quantity` | Numerical (float) | Any float $> 0.0$ (e.g. `500.0`, `12.5`) | Standard Scaled (`StandardScaler`) | Batch quantity |
| **6** | `broken_percentage` | Numerical (float) | Continuous from `0.0` to `100.0` | Standard Scaled (`StandardScaler`) | Percentage of fractured / fragmented pieces |
| **7** | `condition_score` | Numerical (float) | `4.0` (Excellent), `3.0` (Good), `2.0` (Moderate), `1.0` (Damaged), `0.0` (Severely Damaged) | Ordinal numerical mapping | Quantitative degradation index |
| **8** | `contamination_score` | Numerical (float) | `0.0` (None), `1.0` (Low), `2.0` (Moderate), `3.0` (High), `4.0` (Hazardous) | Ordinal numerical mapping | Quantitative toxicity / contamination index |
| **9** | `has_cracks` | Binary (float) | `1.0` (True) or `0.0` (False) | Pass-through binary flag | Extracted from `additional_characteristics['cracks']` |
| **10**| `structural_compromised`| Binary (float)| `1.0` (Compromised/Deformed) or `0.0` (Sound)| Pass-through binary flag | Extracted from `additional_characteristics['structural_integrity']` |
| **11**| `has_rust` | Binary (float) | `1.0` (Moderate/Heavy) or `0.0` (None/Low) | Pass-through binary flag | Extracted from `additional_characteristics['rust_level']` |
| **12**| `has_rot` | Binary (float) | `1.0` (Dry/Wet rot present) or `0.0` (None) | Pass-through binary flag | Extracted from `additional_characteristics['rot']` |
| **13**| `is_moist` | Binary (float) | `1.0` (High moisture/wet) or `0.0` (Dry) | Pass-through binary flag | Extracted from `additional_characteristics['moisture']` |
| **14**| `has_hazardous_coating`| Binary (float) | `1.0` (Lead paint/chemical/asbestos) or `0.0`| Pass-through binary flag | Extracted from `additional_characteristics['paint_coating']` |
| **15**| `is_separable` | Binary (float) | `1.0` (Can be sorted on-site/MRF) or `0.0` | Pass-through binary flag | Extracted from `additional_characteristics['separable_on_site']` |

---

## 3. Defined Target Output Classes & Response Schema

### 3.1 The 5 Canonical Target Classes
The ML model solves a **Multi-Class Classification Problem** with exactly 5 target pathways aligned to the European Waste Framework Directive & Circular Waste Hierarchy:

```python
TARGET_CLASSES = [
    "REUSE",                            # Class 0: Direct salvage & whole-component reuse (Tier 1)
    "REPAIR",                           # Class 1: Refurbishment, minor reconditioning, recutting (Tier 2)
    "RECYCLE",                          # Class 2: Reprocessing into aggregates / secondary feedstock (Tier 3)
    "RECOVER",                          # Class 3: Thermal energy recovery / MRF fiber recovery (Tier 4)
    "DISPOSAL / SPECIALIZED HANDLING"   # Class 4: Regulated hazardous containment or landfill (Tier 5)
]
```

### 3.2 Expected Model Methods
Your trained model object must implement the standard Scikit-Learn estimator API:
1. `model.predict(X)` $\rightarrow$ Returns an array of predicted class strings (e.g. `["RECYCLE"]`).
2. `model.predict_proba(X)` $\rightarrow$ Returns a 2D array of class probabilities of shape `(n_samples, 5)` summing to $1.0$.

### 3.3 API Response Output (`AssessmentResult`)
When `/api/analyze` is called, the ML adapter returns:
```json
{
  "id": 1,
  "timestamp": "2026-09-18T18:05:00Z",
  "input_summary": {
    "material": "Concrete",
    "condition": "Damaged",
    "contamination": "None",
    "quantity": 500.0,
    "unit": "kg",
    "additional_characteristics": {
      "cracks": "Moderate",
      "structural_integrity": "Compromised"
    }
  },
  "recommended_pathway": "RECYCLE",
  "confidence_score": 0.942,
  "prediction_probabilities": {
    "REUSE": 0.035,
    "REPAIR": 0.012,
    "RECYCLE": 0.942,
    "RECOVER": 0.009,
    "DISPOSAL / SPECIALIZED HANDLING": 0.002
  },
  "model_name": "RandomForestClassifier Pipeline",
  "model_version": "1.0.0",
  "inference_source": "USER_TRAINED_ML_MODEL",
  "rule_match_strength": "ML Confidence: 94.2%",
  "matched_rule": "ML-RandomForestClassifier Pipeline",
  "reason": "Direct reuse is unsuitable due to material condition, while clean concrete remains suitable for processing into recycled aggregate and secondary feedstock.",
  "conditions_satisfied": [
    "Material = Concrete",
    "Condition = Damaged (Score: 1.0/4)",
    "Contamination = None (Score: 0.0/4)",
    "ML Model Confidence = 94.2%",
    "Inference Engine = RandomForestClassifier Pipeline (USER_TRAINED_ML_MODEL)"
  ],
  "potential_applications": [
    "Crushed recycled aggregate (RCA)",
    "Road base sub-base course",
    "Engineered fill"
  ],
  "alternative_options": [
    "Controlled reuse for suitable non-structural applications",
    "Controlled sub-base backfill"
  ],
  "decision_steps": [...],
  "hierarchy_evaluation": [...],
  "sustainability": {
    "landfill_avoidance": "HIGH (85%+ Diverted)",
    "material_recovery": "HIGH (Processed Aggregate / Secondary Feedstock)",
    "resource_conservation": "HIGH (Offsets Virgin Quarrying and Smelting)",
    "circularity_potential": "HIGH (Secondary Loop Reprocessing)",
    "assessment_type": "Machine Learning Qualitative Sustainability Index",
    "note": "Conserves landfill space and displaces virgin raw material extraction."
  },
  "safety_disclaimer": "This decision-support recommendation is generated by a Machine Learning model operating under civil and environmental engineering safety constraints...",
  "professional_assessment_required": false
}
```

---

## 4. How the "Empty" ML Model Slot Works

The model file location is:
```
backend/app/ml/saved_models/waste_recovery_model.joblib
```

### Dynamic Detection in `backend/app/ml/model_adapter.py`
1. When the backend starts or an assessment request arrives, `get_loaded_model()` checks if `waste_recovery_model.joblib` exists in `saved_models/`.
2. **If the file is absent (Empty Slot)**:
   - The adapter loads `BaselineProbabilisticModel()`.
   - It computes domain-calibrated class probabilities and recommendations.
   - It sets `inference_source = "BASELINE_PROBABILISTIC_ENGINE"`.
   - The entire frontend displays valid confidence bars, probability breakdowns, and recovery advice without throwing errors.
3. **If the file is present (Your Trained Model)**:
   - The adapter loads your pipeline via `joblib.load()`.
   - It executes `model.predict_proba(df_features)` directly.
   - It sets `inference_source = "USER_TRAINED_ML_MODEL"`.
   - The UI automatically displays your model's real predictions and confidence metrics!

### Built-In Environmental Safety Guardrail
Even with an ML model, environmental regulations mandate zero-tolerance for toxic or hazardous substances. If:
- `contamination in ["High", "Hazardous"]`, or
- `has_hazardous_coating == 1.0`

The adapter automatically overrides the recommendation to `DISPOSAL / SPECIALIZED HANDLING`, triggers `professional_assessment_required = true`, and appends `"(Safety Override Enforced)"` to the inference source. This guarantees safety compliance during site inspections.

---

## 5. Step-by-Step Instructions: What You Need To Do Next

### Step 1: Open Your Terminal in the Project Directory
Navigate to the project root:
```bash
cd "c:\VIT Chennai\Third Year\Fifth Semester\BCLE215L - Waste Management\Project\F2 project\construction-waste-recovery-planner"
```

### Step 2: (Optional) Inspect or Add Your Training Data
A reference dataset with 1,200 stratified observations has already been generated for you at:
```
backend/app/ml/data/sample_waste_dataset.csv
```
You can inspect it, replace it with your real-world site dataset, or append additional rows. Just ensure the columns match the 15 feature names plus `recommended_pathway`.

### Step 3: Run the Training Script
Run the turnkey training script:
```bash
backend\venv\Scripts\python backend/app/ml/train_template.py
```
*(Or if you use global python: `python backend/app/ml/train_template.py`)*

**What this script does automatically:**
1. Loads the dataset into Pandas.
2. Applies `OneHotEncoder` to categorical features and `StandardScaler` to numerical features via Scikit-Learn's `ColumnTransformer`.
3. Trains a `RandomForestClassifier` ensemble pipeline.
4. Evaluates test set Accuracy, Precision, Recall, and Confusion Matrix.
5. Serializes the fitted model pipeline directly to:
   `backend/app/ml/saved_models/waste_recovery_model.joblib`
6. Writes training diagnostics to:
   `backend/app/ml/saved_models/model_metadata.json`

### Step 4: (Alternative) Train Your Own Custom Model in a Jupyter Notebook / Python Script
If you prefer to train your own custom model (e.g. XGBoost, LightGBM, CatBoost, or an MLP), use this code snippet:

```python
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

# 1. Load data
df = pd.read_csv("backend/app/ml/data/sample_waste_dataset.csv")

categorical_cols = ["material", "condition", "contamination", "unit"]
numerical_cols = [
    "quantity", "broken_percentage", "condition_score", "contamination_score",
    "has_cracks", "structural_compromised", "has_rust", "has_rot",
    "is_moist", "has_hazardous_coating", "is_separable"
]
all_features = categorical_cols + numerical_cols

X = df[all_features]
y = df["recommended_pathway"]

# 2. Build Pipeline
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
    ("num", StandardScaler(), numerical_cols)
])

clf = GradientBoostingClassifier(n_estimators=200, learning_rate=0.08, max_depth=6)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", clf)
])

# 3. Train
pipeline.fit(X, y)

# 4. Save to the empty ML model slot
joblib.dump(pipeline, "backend/app/ml/saved_models/waste_recovery_model.joblib")
print("Trained model saved successfully!")
```

### Step 5: Start the Full-Stack Application
In two separate terminals:

**Terminal 1 (Backend):**
```bash
run_backend.bat
```
*(Runs FastAPI at `http://127.0.0.1:8000`)*

**Terminal 2 (Frontend):**
```bash
run_frontend.bat
```
*(Runs Vite React at `http://localhost:5173`)*

---

## 6. How to Verify Your Model Integration

1. **Check ML Status Endpoint**:
   Open in browser or curl:
   ```
   http://127.0.0.1:8000/api/ml/status
   ```
   You will see:
   ```json
   {
     "model_file_exists": true,
     "model_file_path": ".../saved_models/waste_recovery_model.joblib",
     "is_user_trained_model_loaded": true,
     "model_engine": "Trained Scikit-Learn Model",
     "model_version": "1.0.0"
   }
   ```
2. **Dashboard UI Verification**:
   - Open `http://localhost:5173`.
   - Look at the new **Machine Learning Decision Engine Status Card** on the Dashboard.
   - It will display a green checkmark badge: **"Trained Model Active"**.
3. **Assessment Result Page Verification**:
   - Click **"New Assessment"** or select any quick demo.
   - Submit the assessment.
   - On the Result Page, observe:
     - **ML Model Confidence**: percentage score with colored badge (e.g. `95.4% Confidence`).
     - **ML Multi-Class Probability Distribution**: horizontal progress meters showing posterior probabilities for `REUSE`, `REPAIR`, `RECYCLE`, `RECOVER`, and `DISPOSAL`.
     - **Decision Pipeline**: 5-stage ML vectorization and inference flow.

---

## 7. Summary of Codebase Changes

| Component | File Path | Nature of Change |
|:---|:---|:---|
| **ML Config** | `backend/app/ml/config.py` | [NEW] Feature lists, target classes, path constants |
| **Preprocessor** | `backend/app/ml/preprocessor.py` | [NEW] 15-feature extraction & engineering from `WasteInput` |
| **Model Adapter** | `backend/app/ml/model_adapter.py` | [NEW] Model loader, probabilistic inference, fallback heuristic, guardrails |
| **Training Template** | `backend/app/ml/train_template.py` | [NEW] Complete Scikit-Learn Pipeline training & export script |
| **Sample Dataset** | `backend/app/ml/data/sample_waste_dataset.csv` | [NEW] Stratified 1,200 observation reference dataset |
| **Model Storage** | `backend/app/ml/saved_models/` | [NEW] Designated folder for user's `waste_recovery_model.joblib` |
| **ML Status Route** | `backend/app/routes/ml_status.py` | [NEW] `GET /api/ml/status` diagnostic endpoint |
| **ML Test Suite** | `backend/tests/test_ml_pipeline.py` | [NEW] Automated tests for feature vectorization and probability estimation |
| **Assessment Schema** | `backend/app/schemas/assessment.py` | [MODIFIED] Added `confidence_score`, `prediction_probabilities`, `model_name` |
| **Assessment Model** | `backend/app/models/assessment.py` | [MODIFIED] Added SQLite persistence columns for ML outputs |
| **Assessment Route** | `backend/app/routes/assessments.py` | [MODIFIED] Switched `POST /api/analyze` to call `evaluate_waste_ml()` |
| **FastAPI Entry** | `backend/app/main.py` | [MODIFIED] Registered `ml_status` router, updated docs & metadata |
| **Frontend Types** | `frontend/src/types/index.ts` | [MODIFIED] Added ML fields to `AssessmentResult`, `AssessmentRecord`, `MLModelStatus` |
| **API Client** | `frontend/src/services/api.ts` | [MODIFIED] Added `getMLStatus()` method |
| **Navbar** | `frontend/src/components/Navbar.tsx` | [MODIFIED] Updated subtitle & engine pill to ML Decision Engine |
| **Result Page** | `frontend/src/pages/AssessmentResultPage.tsx` | [MODIFIED] Added ML confidence display & multi-class probability breakdown bars |
| **Decision Flow** | `frontend/src/components/DecisionFlow.tsx` | [MODIFIED] Re-architected into 5-stage ML pipeline flowchart |
| **Dashboard** | `frontend/src/pages/DashboardPage.tsx` | [MODIFIED] Added ML Model Integration Status Card widget |
| **Methodology** | `frontend/src/pages/MethodologyPage.tsx` | [MODIFIED] Documented ML formulation, features, and safety guardrails |
