import sys, json, warnings
sys.path.insert(0, 'backend')
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('backend/app/ml/data/sample_waste_dataset.csv')
CAT = ['material','condition','contamination','unit']
NUM = ['quantity','broken_percentage','condition_score','contamination_score','has_cracks','structural_compromised','has_rust','has_rot','is_moist','has_hazardous_coating','is_separable']
X = df[CAT + NUM]
y = df['recommended_pathway']

preprocessor = ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CAT), ('num', StandardScaler(), NUM)])
classifiers = {'RandomForest(n=150)': RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, class_weight='balanced'), 'GradientBoosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42), 'DecisionTree': DecisionTreeClassifier(max_depth=10, random_state=42, class_weight='balanced'), 'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print('5-FOLD CV RESULTS:')
print('-'*70)
for name, clf in classifiers.items():
    pipe = Pipeline([('pre', preprocessor), ('clf', clf)])
    key_test = 'test_score'
    key_train = 'train_score'
    res = cross_validate(pipe, X, y, cv=cv, scoring='accuracy', return_train_score=True)
    val_mean = np.mean(res[key_test])*100
    val_std = np.std(res[key_test])*100
    train_mean = np.mean(res[key_train])*100
    fold_scores = [round(s*100,1) for s in res[key_test]]
    print(name + ': Val ' + str(round(val_mean,2)) + '% +/- ' + str(round(val_std,2)) + '%  Train: ' + str(round(train_mean,2)) + '%  Folds: ' + str(fold_scores))
