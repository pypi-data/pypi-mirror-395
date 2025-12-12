# src/models/ensemble.py
"""
Ensemble model definition.
Creates a soft-voting ensemble of Logistic Regression, Random Forest, and SVC.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from config import RANDOM_STATE


def create_ensemble_model() -> VotingClassifier:
    """
    Create a soft-voting ensemble classifier.

    Returns:
        VotingClassifier: Ensemble of three strong base models
    """
    # Base estimators
    log_clf = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    rf_clf = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)
    svc_clf = SVC(probability=True, random_state=RANDOM_STATE)

    # Soft voting ensemble (uses predicted probabilities)
    ensemble = VotingClassifier(
        estimators=[
            ('lr', log_clf),
            ('rf', rf_clf),
            ('svc', svc_clf)
        ],
        voting='soft',
        n_jobs=-1
    )

    return ensemble