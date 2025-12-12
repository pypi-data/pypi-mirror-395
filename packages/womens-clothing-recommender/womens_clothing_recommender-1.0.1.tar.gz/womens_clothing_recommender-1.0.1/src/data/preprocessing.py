# src/data/preprocessing.py
"""
Data preprocessing utilities.
Handles cleaning and pipeline construction for the recommendation model.
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from ..features.review_features import ReviewFeatures
from config import (
    NUMERIC_FEATURES, CATEGORICAL_FEATURES,
    TFIDF_MAX_FEATURES, SVD_N_COMPONENTS, ONEHOT_MAX_CATEGORIES
)


def preprocess_ecommerce_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize raw dataset.

    Args:
        df (pd.DataFrame): Raw dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    # Remove unnamed index column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)

    # Standardize column names
    df.columns = [col.replace('.', ' ').strip() for col in df.columns]

    # Handle missing text values
    df['Title'] = df['Title'].fillna('').astype(str)
    df['Review Text'] = df['Review Text'].fillna('').astype(str)

    # Handle missing categorical values
    categorical_cols = ['Division Name', 'Department Name', 'Class Name']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str)

    return df


def create_preprocessing_pipeline() -> ColumnTransformer:
    """
    Create the full preprocessing pipeline using ColumnTransformer.

    Returns:
        ColumnTransformer: Combined preprocessing steps
    """
    # Numeric features pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical features pipeline
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
        ('onehot', OneHotEncoder(
            handle_unknown='ignore',
            max_categories=ONEHOT_MAX_CATEGORIES
        ))
    ])

    # Text features pipeline with TF-IDF + SVD
    text_transformer = Pipeline(steps=[
        ('tfidf', TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES,
            ngram_range=(1, 2),
            stop_words='english'
        )),
        ('svd', TruncatedSVD(n_components=SVD_N_COMPONENTS, random_state=42))
    ])

    # Custom engineered features from review text
    review_features_transformer = Pipeline(steps=[
        ('features', ReviewFeatures()),
        ('scaler', StandardScaler())
    ])

    # Combine all transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES),
            ('title_tfidf', text_transformer, 'Title'),
            ('review_tfidf', text_transformer, 'Review Text'),
            ('review_features', review_features_transformer, ['Title', 'Review Text'])
        ],
        remainder='drop'
    )

    return preprocessor