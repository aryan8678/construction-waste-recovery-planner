"""
Machine Learning Training Script Template for Construction Waste Recovery Planner.

This script trains a multi-class classification model using Scikit-Learn.
It preprocesses categorical and numerical features using a ColumnTransformer,
fits an ensemble classifier, evaluates performance metrics, and exports
the finalized model pipeline to `backend/app/ml/saved_models/waste_recovery_model.joblib`.

Usage:
    python backend/app/ml/train_template.py [--dataset path/to/your/dataset.csv]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to sys.path so app imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ml.config import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    ALL_FEATURE_COLUMNS,
    TARGET_CLASSES,
    SAVED_MODELS_DIR,
    DEFAULT_MODEL_FILE,
    METADATA_FILE,
    DATA_DIR
)

def train(dataset_path: Path):
    try:
        import pandas as pd
        import numpy as np
        import joblib
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements: pip install pandas scikit-learn joblib numpy")
        sys.exit(1)

    print("=" * 70)
    print(" CONSTRUCTION WASTE RECOVERY PLANNER - MODEL TRAINING")
    print("=" * 70)

    # 1. Load dataset
    if not dataset_path.exists():
        print(f"Dataset not found at: {dataset_path}")
        print("Generating sample dataset first...")
        from app.ml.generate_sample_dataset import main as gen_main
        gen_main()
        dataset_path = DATA_DIR / "sample_waste_dataset.csv"

    print(f"Loading training data from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    target_col = "recommended_pathway"
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset. Columns: {list(df.columns)}")

    # Check required feature columns
    missing_cols = [c for c in ALL_FEATURE_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required feature columns: {missing_cols}")

    X = df[ALL_FEATURE_COLUMNS]
    y = df[target_col]

    print("\nClass distribution in dataset:")
    for cls, count in y.value_counts().items():
        print(f"  - {cls:<35}: {count:>4} samples ({count/len(y)*100:5.1f}%)")

    # 2. Train-Test Split (Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\nSplit into: {len(X_train)} training samples, {len(X_test)} validation samples.")

    # 3. Construct Preprocessing & Modeling Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERICAL_FEATURES)
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    # 4. Fit Pipeline
    print("\nTraining Random Forest Classifier Pipeline...")
    pipeline.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy on Validation Set: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # 6. Save Model Artifact & Metadata
    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, DEFAULT_MODEL_FILE)
    print(f"\n[OK] Model successfully serialized to: {DEFAULT_MODEL_FILE}")

    metadata = {
        "model_name": "RandomForestClassifier Pipeline",
        "version": "1.0.0",
        "training_timestamp": datetime.now().isoformat(),
        "training_samples": len(X_train),
        "validation_samples": len(X_test),
        "accuracy": round(float(acc), 4),
        "features": ALL_FEATURE_COLUMNS,
        "classes": list(pipeline.classes_)
    }

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Metadata saved to: {METADATA_FILE}")

    print("\n" + "=" * 70)
    print(" TRAINING COMPLETE! Your model is now live in the application.")
    print(" Start backend (`run_backend.bat`) and reload the frontend to verify!")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Waste Recovery ML Model")
    parser.add_argument("--dataset", type=str, default=str(DATA_DIR / "sample_waste_dataset.csv"),
                        help="Path to CSV training dataset")
    args = parser.parse_args()
    train(Path(args.dataset))
