# config.py
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
DATASET_FILE = DATA_DIR / "dataset.csv"
MODEL_FILE = MODELS_DIR / "best_recommendation_model.pkl"

# Model Parameters
NUMERIC_FEATURES = ['Age', 'Rating', 'Positive Feedback Count']
CATEGORICAL_FEATURES = ['Clothing ID', 'Division Name', 'Department Name', 'Class Name']
TEXT_FEATURES = ['Title', 'Review Text']

# Pipeline Parameters
TFIDF_MAX_FEATURES = 5000
SVD_N_COMPONENTS = 100
ONEHOT_MAX_CATEGORIES = 100

# GridSearch Parameters
PARAM_GRID = {
    'classifier__lr__C': [0.1, 1.0],
    'classifier__rf__n_estimators': [100, 200],
    'classifier__svc__C': [1, 10]
}
CV_FOLDS = 3
TEST_SIZE = 0.2
RANDOM_STATE = 42