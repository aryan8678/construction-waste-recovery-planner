# Construction Waste Recovery Planner

## 1. Project Overview

The **Construction Waste Recovery Planner** is a full-stack
decision-support application for recommending sustainable recovery
pathways for construction and demolition waste.

The current implementation uses a **deterministic, rule-based decision
engine**. It evaluates material characteristics and returns an
explainable recommendation such as:

-   `REUSE`
-   `REPAIR`
-   `RECYCLE`
-   `RECOVER`
-   `DISPOSAL / SPECIALIZED HANDLING`

The application also stores assessment history and provides supporting
information about materials, rules, statistics, and the decision
process.

> **Current status:** The application has been upgraded to a **modular Machine Learning (ML) decision architecture** with hybrid civil engineering safety guardrails. The model slot (`backend/app/ml/saved_models/waste_recovery_model.joblib`) is modular and ready for the user to train and drop in. See [ML_MODEL_INTEGRATION_SPECIFICATION.md](./ML_MODEL_INTEGRATION_SPECIFICATION.md) for full details.

------------------------------------------------------------------------

## 2. Technology Stack

### Backend

-   Python
-   FastAPI
-   Pydantic
-   SQLAlchemy
-   SQLite
-   Pytest
-   Uvicorn-compatible FastAPI application structure

### Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS
-   Lucide React icons
-   CSS-based responsive interface

### Database

-   SQLite database
-   SQLAlchemy ORM models
-   Automatic table creation
-   Seed data for rules, materials, and example assessments

------------------------------------------------------------------------

## 3. High-Level Architecture

``` text
User
  |
  v
React + TypeScript Frontend
  |
  | HTTP requests
  v
FastAPI Backend
  |
  +--> Pydantic input validation
  |
  +--> Rule-Based Decision Engine
  |       |
  |       +--> Rule definitions
  |       +--> Material knowledge base
  |       +--> Decision explanation
  |
  +--> SQLite database through SQLAlchemy
  |
  v
Assessment Result
  |
  v
Frontend result, history, statistics, and explanation views
```

------------------------------------------------------------------------

## 4. Backend Structure

``` text
backend/
├── app/
│   ├── main.py
│   ├── database/
│   │   ├── session.py
│   │   └── seed_data.py
│   ├── models/
│   │   ├── assessment.py
│   │   ├── material.py
│   │   └── rule.py
│   ├── routes/
│   │   ├── assessments.py
│   │   ├── health.py
│   │   ├── materials.py
│   │   ├── rules.py
│   │   └── statistics.py
│   ├── rules/
│   │   ├── engine.py
│   │   ├── materials_data.py
│   │   └── rule_base.py
│   └── schemas/
│       ├── assessment.py
│       ├── material.py
│       ├── rule.py
│       └── statistics.py
├── tests/
│   └── test_rule_engine.py
└── requirements.txt
```

------------------------------------------------------------------------

## 5. Application Entry Point

### File

``` text
backend/app/main.py
```

The application:

1.  Creates database tables using SQLAlchemy metadata.
2.  Runs the database seeding function.
3.  Creates the FastAPI application.
4.  Enables CORS.
5.  Registers the API routers.
6.  Exposes a root endpoint describing the application.

The current root response identifies the engine as:

``` text
Deterministic Rule-Based (No AI/ML)
```

This description will need to be updated when the ML model becomes the
primary decision component.

------------------------------------------------------------------------

## 6. Input Data Model

### File

``` text
backend/app/schemas/assessment.py
```

The main input model is `WasteInput`.

  ------------------------------------------------------------------------------
  Field                          Type                    Description
  ------------------------------ ----------------------- -----------------------
  `material`                     string                  Material type, such as
                                                         Concrete, Brick, Steel,
                                                         or Wood

  `condition`                    string                  Material condition

  `contamination`                string                  Contamination level

  `quantity`                     float                   Quantity of the waste
                                                         material

  `unit`                         string                  Measurement unit, such
                                                         as kg or tonnes

  `additional_characteristics`   dictionary              Optional
                                                         material-specific
                                                         characteristics
  ------------------------------------------------------------------------------

### Current validation

-   `material` cannot be empty.
-   `quantity` must be greater than zero.
-   `additional_characteristics` defaults to an empty dictionary.
-   Pydantic validates the request body before the decision engine is
    called.

### Example input

``` json
{
  "material": "Concrete",
  "condition": "Damaged",
  "contamination": "None",
  "quantity": 500,
  "unit": "kg",
  "additional_characteristics": {
    "cracks": "Moderate",
    "structural_integrity": "Compromised"
  }
}
```

------------------------------------------------------------------------

## 7. Rule-Based Decision Engine

### Files

``` text
backend/app/rules/engine.py
backend/app/rules/rule_base.py
```

The function used by the backend is:

``` python
evaluate_waste(waste_input)
```

The engine is deterministic. It uses the supplied input characteristics
to evaluate predefined rules and produce an explainable result.

The returned result includes:

-   Recommended pathway
-   Rule match strength
-   Matched rule identifier
-   Reason for the recommendation
-   Conditions satisfied
-   Potential applications
-   Alternative recovery options
-   Decision steps
-   Waste hierarchy evaluation
-   Sustainability assessment
-   Safety disclaimer
-   Whether professional assessment is required

### Rule characteristics

Rules are defined for different materials and conditions. Examples
covered by the test suite include:

-   Concrete
-   Brick
-   Steel
-   Wood
-   Soil

The rule system considers factors such as:

-   Material condition
-   Contamination
-   Structural integrity
-   Cracks
-   Rust
-   Rot
-   Paint coating
-   Other material-specific characteristics

### Important behavior

Hazardous contamination can lead to a disposal or specialized-handling
recommendation and can set:

``` text
professional_assessment_required = true
```

------------------------------------------------------------------------

## 8. API Endpoints

All primary application endpoints are under the `/api` prefix unless
otherwise stated.

### Health

``` http
GET /health
```

Used to check whether the backend is running.

### Root

``` http
GET /
```

Returns a welcome message, documentation location, online status, and
engine description.

### Analyze waste

``` http
POST /api/analyze
```

Flow:

1.  Receives a `WasteInput` object.
2.  Validates the input with Pydantic.
3.  Calls `evaluate_waste`.
4.  Saves the assessment in SQLite.
5.  Returns the complete `AssessmentResult`.

### List assessments

``` http
GET /api/assessments
```

Supports optional filtering parameters:

-   `material`
-   `pathway`
-   `search`

Results are ordered by timestamp in descending order.

### Get one assessment

``` http
GET /api/assessments/{assessment_id}
```

Retrieves a previously stored assessment and reconstructs the result
using the decision engine.

### Delete an assessment

``` http
DELETE /api/assessments/{assessment_id}
```

Deletes an assessment from the database.

### Materials

``` http
GET /api/materials
GET /api/materials/{name}
```

Returns material information from the material knowledge base.

### Rules

``` http
GET /api/rules
GET /api/rules/{rule_id}
```

Returns rule information and individual rule details.

### Statistics

``` http
GET /api/statistics
```

Returns application statistics, including assessment counts and pathway
counts.

------------------------------------------------------------------------

## 9. Database Design

### Database

The project uses SQLite:

``` text
backend/app/database/waste_planner.db
```

### Assessment table

The `Assessment` SQLAlchemy model stores:

  Column                         Purpose
  ------------------------------ -------------------------------------------------
  `id`                           Primary key
  `timestamp`                    Assessment creation time
  `material`                     Material name
  `condition`                    Material condition
  `contamination`                Contamination level
  `quantity`                     Quantity
  `unit`                         Measurement unit
  `additional_characteristics`   JSON text containing extra inputs
  `recommended_pathway`          Selected recovery pathway
  `reason`                       Explanation
  `matched_rule`                 Rule identifier
  `rule_match_strength`          Match strength
  `applications`                 JSON text containing possible applications
  `alternatives`                 JSON text containing alternative options
  `decision_path`                JSON text containing decision steps
  `sustainability`               JSON text containing sustainability information

Lists and dictionaries are serialized into JSON text before being stored
in SQLite.

------------------------------------------------------------------------

## 10. Database Seeding

### File

``` text
backend/app/database/seed_data.py
```

The seed process creates initial rule and material data and inserts
demonstration assessments.

The demonstration data includes materials such as:

-   Concrete
-   Brick
-   Steel
-   Wood
-   Glass
-   Soil
-   Ceramic / Tiles
-   Gypsum
-   Asphalt

The seeded assessments contain different combinations of:

-   Condition
-   Contamination
-   Quantity
-   Material-specific characteristics

The seed function uses the current rule engine to generate the
recommendation and related explanation fields.

> When ML is introduced, seed behavior must be reviewed carefully so
> that repeated application startup does not create unwanted duplicate
> records or overwrite expected behavior.

------------------------------------------------------------------------

## 11. Result Schema

The main result model is `AssessmentResult`.

It contains:

-   `id`
-   `timestamp`
-   `input_summary`
-   `recommended_pathway`
-   `rule_match_strength`
-   `matched_rule`
-   `reason`
-   `conditions_satisfied`
-   `potential_applications`
-   `alternative_options`
-   `decision_steps`
-   `hierarchy_evaluation`
-   `sustainability`
-   `safety_disclaimer`
-   `professional_assessment_required`

The frontend currently depends on this structured response rather than
receiving only a single predicted label.

Therefore, an ML integration should preserve this response contract
wherever possible.

------------------------------------------------------------------------

## 12. Frontend Structure

``` text
frontend/src/
├── App.tsx
├── App.css
├── index.css
├── components/
│   ├── DecisionFlow.tsx
│   ├── Footer.tsx
│   ├── HierarchyBadge.tsx
│   ├── Navbar.tsx
│   ├── RuleModal.tsx
│   └── SustainabilityPanel.tsx
├── pages/
│   ├── AssessmentResultPage.tsx
│   ├── DashboardPage.tsx
│   ├── HistoryPage.tsx
│   ├── MaterialsPage.tsx
│   ├── MethodologyPage.tsx
│   ├── NewAssessmentPage.tsx
│   └── RuleExplorerPage.tsx
├── services/
│   └── api.ts
└── types/
    └── index.ts
```

### Main frontend responsibilities

-   Collect waste assessment inputs.
-   Send requests to the backend API.
-   Display recommendation results.
-   Show decision flow and explanation.
-   Display potential applications and alternatives.
-   Show sustainability information.
-   Display assessment history.
-   Display materials and rule information.
-   Display statistics and methodology information.

------------------------------------------------------------------------

## 13. Frontend Pages

### New Assessment

The `NewAssessmentPage` collects the waste information needed by the
backend.

The page is responsible for submitting the assessment request through
the API service.

### Assessment Result

The `AssessmentResultPage` displays:

-   Recommended pathway
-   Reason
-   Conditions satisfied
-   Decision flow
-   Potential applications
-   Alternative recovery options
-   Sustainability assessment
-   Safety and professional-assessment information

### Dashboard

Displays a general overview of the application and assessment-related
information.

### History

Displays previously created assessments and supports retrieving or
managing historical records.

### Materials

Displays material information from the backend material endpoints.

### Methodology

Explains the application's current decision-support methodology.

### Rule Explorer

Allows users to inspect the available rules.

------------------------------------------------------------------------

## 14. Testing

### File

``` text
backend/tests/test_rule_engine.py
```

The test suite checks both individual rule behavior and API-level
behavior.

Covered examples include:

-   Concrete reuse
-   Concrete recycling
-   Concrete hazardous disposal
-   Brick reuse and recycling
-   Steel reuse and recycling
-   Wood reuse, recovery, and hazardous disposal
-   Soil reuse and hazardous disposal
-   API analysis flow
-   Assessment history retrieval
-   Statistics endpoint
-   Rules endpoint
-   Materials endpoint

The API flow test verifies that:

1.  `/api/analyze` returns HTTP 200.
2.  A recommendation is returned.
3.  The assessment receives a database ID.
4.  Assessment history contains records.
5.  Statistics are available.
6.  Rules and materials endpoints return data.

### Important testing requirement for ML integration

The existing rule-based tests should be preserved initially as a
baseline. New ML tests should be added separately instead of immediately
deleting the existing tests.

------------------------------------------------------------------------

## 15. Current Strengths

The existing implementation already provides:

-   A functioning full-stack architecture
-   Input validation
-   A modular backend
-   A reusable decision engine
-   Explainable recommendations
-   Database persistence
-   Assessment history
-   Material information
-   Rule exploration
-   Statistics
-   Frontend result visualizations
-   Automated tests
-   A safety disclaimer and professional-assessment flag

These components can be retained while the prediction component is
upgraded.

------------------------------------------------------------------------

## 16. Current Limitations

Based on the current implementation:

1.  The recommendation engine is rule-based, not ML-based.
2.  No trained ML model is currently integrated.
3.  The current rule engine depends on predefined material-specific
    logic.
4.  The result schema contains rule-oriented fields such as
    `matched_rule`.
5.  The current database schema does not explicitly store ML model
    version, prediction probability, or model confidence.
6.  The project needs a suitable labelled dataset before an ML model can
    be trained reliably.
7.  If the dataset labels are generated directly from the existing
    rules, the model will primarily learn to imitate the rule engine
    rather than learn independently from real-world expert decisions.
8.  ML predictions must be validated carefully for hazardous materials
    and safety-sensitive cases.

------------------------------------------------------------------------

## 17. Planned ML Integration

The safest integration approach is incremental.

### Proposed architecture

``` text
Frontend input
     |
     v
FastAPI validation
     |
     v
Feature preprocessing
     |
     v
ML prediction model
     |
     +--> Prediction and confidence
     |
     +--> Rule engine safety checks / fallback
     |
     v
Existing result format
     |
     v
Database + frontend
```

### Recommended implementation approach

1.  Inspect the dataset.
2.  Identify input features and target labels.
3.  Compare dataset columns with the existing `WasteInput` model.
4.  Clean and encode the dataset.
5.  Split the data into training and testing sets.
6.  Train baseline models.
7.  Evaluate classification performance.
8.  Save the trained model and preprocessing objects.
9.  Add a prediction module to the backend.
10. Keep the existing API input format initially.
11. Convert the ML prediction into the existing `AssessmentResult`
    structure.
12. Add fallback behavior for unknown or unsafe inputs.
13. Add ML-specific tests.
14. Update the frontend only where the dataset or model requires
    additional fields.
15. Update the methodology page and API description to reflect the
    hybrid or ML-based system.

### Suggested future files

``` text
backend/app/ml/
├── preprocessing.py
├── train.py
├── predict.py
├── model.joblib
├── encoder.joblib
└── metadata.json
```

The exact file structure should be finalized after inspecting the
dataset.

------------------------------------------------------------------------

## 18. Compatibility Requirements for ML Integration

The following should remain stable unless there is a specific reason to
change them:

-   `POST /api/analyze`
-   Existing input field names
-   Database persistence
-   Assessment history
-   Frontend result rendering
-   Existing result fields
-   Safety-related behavior
-   Existing tests and rule engine

The ML system can initially be added behind the existing API so that the
frontend does not need to be rewritten immediately.

------------------------------------------------------------------------

## 19. Development and Execution

The project includes batch files at the project root:

``` text
run_all.bat
run_backend.bat
run_frontend.bat
```

The backend dependencies are listed in:

``` text
backend/requirements.txt
```

The frontend dependencies and scripts are listed in:

``` text
frontend/package.json
```

The frontend build script runs TypeScript compilation followed by the
Vite build:

``` bash
npm run build
```

The frontend development script is:

``` bash
npm run dev
```

The backend should be run from the backend environment with the project
package structure available.

------------------------------------------------------------------------

## 20. Summary

The current project is a working construction-waste decision-support
application built around a deterministic rule engine.

Its major implemented components are:

-   React frontend
-   FastAPI backend
-   Pydantic validation
-   SQLAlchemy and SQLite persistence
-   Material knowledge base
-   Rule database and rule explorer
-   Explainable decision results
-   Sustainability information
-   Assessment history
-   Statistics
-   Automated tests

The next major development phase is to integrate a suitable dataset and
train an ML model while preserving the existing API, database, frontend
flow, and safety checks.

The ML integration should be performed incrementally and tested after
each change.
