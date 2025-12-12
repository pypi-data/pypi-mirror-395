# src/features/review_features.py
"""
Custom feature extractor for review text.
Extracts length and exclamation count as sentiment proxies.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ReviewFeatures(BaseEstimator, TransformerMixin):
    """
    Extract hand-crafted features from review title and text.
    Features:
        - Title length
        - Review text length
        - Number of exclamation marks (sentiment indicator)
    """

    def fit(self, X, y=None):
        """No fitting required."""
        return self

    def transform(self, X):
        """
        Transform input into numeric features.

        Args:
            X: DataFrame or array with columns ['Title', 'Review Text']

        Returns:
            np.array: Stacked feature matrix
        """
        X = pd.DataFrame(X, columns=['Title', 'Review Text'])

        title_length = X['Title'].str.len().fillna(0).values.reshape(-1, 1)
        review_length = X['Review Text'].str.len().fillna(0).values.reshape(-1, 1)
        exclamation_count = X['Review Text'].str.count('!').fillna(0).values.reshape(-1, 1)

        return np.hstack([title_length, review_length, exclamation_count])