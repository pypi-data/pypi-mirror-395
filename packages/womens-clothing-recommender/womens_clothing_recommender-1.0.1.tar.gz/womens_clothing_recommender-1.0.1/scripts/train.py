# scripts/train.py
"""
Customer Recommendation Prediction Model Training Script
Trains an ensemble model on Women's E-Commerce Clothing Reviews dataset.
Saves model, generates performance plots and saves them to images/ folder.
"""

import os
import sys
import shutil
import logging
from pathlib import Path

import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, classification_report, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay, roc_curve,
    precision_recall_fscore_support
)

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import (
    DATASET_FILE, MODEL_FILE, TEST_SIZE, RANDOM_STATE, PARAM_GRID, CV_FOLDS
)
from src.data.preprocessing import preprocess_ecommerce_data, create_preprocessing_pipeline
from src.models.ensemble import create_ensemble_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Create directory for saving plots
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)


def download_dataset() -> None:
    """Download the dataset from Kaggle if not already present."""
    try:
        import kagglehub
        logger.info("Downloading dataset from Kaggle...")
        download_path = kagglehub.dataset_download("mexwell/womens-e-commerce-clothing-reviews")

        csv_file = next(
            (os.path.join(download_path, f) for f in os.listdir(download_path)
             if f.lower().endswith(".csv")),
            None
        )
        if csv_file is None:
            raise FileNotFoundError("CSV file not found in downloaded dataset.")

        shutil.copy2(csv_file, DATASET_FILE)
        logger.info(f"Dataset successfully downloaded to: {DATASET_FILE}")

    except ImportError:
        logger.error("kagglehub is not installed. Run: pip install kagglehub")
        raise
    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        raise


def load_and_prepare_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load dataset and prepare features and target."""
    if not DATASET_FILE.exists():
        logger.info("Dataset not found. Downloading...")
        download_dataset()

    logger.info(f"Loading dataset from: {DATASET_FILE}")
    df = pd.read_csv(
        DATASET_FILE,
        sep=';',
        quotechar='"',
        on_bad_lines='warn',
        encoding='utf-8'
    )

    df = preprocess_ecommerce_data(df)
    logger.info(f"Data loaded and preprocessed. Shape: {df.shape}")

    feature_cols = [
        'Clothing ID', 'Age', 'Title', 'Review Text', 'Rating',
        'Positive Feedback Count', 'Division Name', 'Department Name', 'Class Name'
    ]
    X = df[feature_cols]
    y = df['Recommended IND']

    return X, y


def train_model(X: pd.DataFrame, y: pd.Series):
    """Train the model using GridSearchCV with stratified split."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
    logger.info(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

    preprocessor = create_preprocessing_pipeline()
    ensemble = create_ensemble_model()

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', ensemble)
    ])

    logger.info("Starting GridSearchCV for hyperparameter tuning...")
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=PARAM_GRID,
        cv=CV_FOLDS,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    logger.info(f"Best parameters found: {grid_search.best_params_}")

    return best_model, X_test, y_test


def evaluate_and_save_metrics(model, X_test, y_test):
    """Evaluate model and save performance metrics visualization."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')

    metrics = {
        "Accuracy": accuracy,
        "ROC AUC": roc_auc,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1
    }

    # Print metrics
    print("\n" + "="*60)
    print(" MODEL PERFORMANCE SUMMARY ")
    print("="*60)
    for metric, value in metrics.items():
        print(f"{metric:12}: {value:.4f}")
    print("="*60)

    # Plot and save metrics bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(metrics.keys(), metrics.values(),
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    plt.ylim(0, 1)
    plt.title("Model Performance Metrics", fontsize=16, fontweight='bold')
    plt.ylabel("Score")
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.01,
                 f'{height:.4f}', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "performance_metrics.png", dpi=300, bbox_inches='tight')
    plt.show()

    return y_pred, y_proba


def plot_and_save_results(y_test, y_pred, y_proba):
    """Generate and save all evaluation plots."""
    cm = confusion_matrix(y_test, y_pred)

    # --- Confusion Matrix ---
    plt.figure(figsize=(8, 6))
    ConfusionMatrixDisplay(cm, display_labels=['Not Recommended', 'Recommended']).plot(
        cmap='Blues', ax=plt.gca()
    )
    plt.title("Confusion Matrix", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.show()

    # --- ROC Curve ---
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC AUC = {roc_auc_score(y_test, y_proba):.4f}',
             linewidth=3, color='#1f77b4')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.7)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "roc_curve.png", dpi=300, bbox_inches='tight')
    plt.show()

    # --- Full Presentation Report (Best for slides) ---
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Customer Recommendation Model - Final Performance Report",
                 fontsize=20, fontweight='bold')

    # Confusion Matrix
    ConfusionMatrixDisplay(cm, display_labels=['Not Recommended', 'Recommended']).plot(
        ax=axes[0,0], cmap='Blues')
    axes[0,0].set_title("Confusion Matrix")

    # ROC Curve
    axes[0,1].plot(fpr, tpr, label=f'ROC AUC = {roc_auc_score(y_test, y_proba):.4f}', linewidth=3)
    axes[0,1].plot([0, 1], [0, 1], 'k--')
    axes[0,1].set_title("ROC Curve")
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)

    # Performance Metrics
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC AUC']
    values = [
        accuracy_score(y_test, y_pred),
        *precision_recall_fscore_support(y_test, y_pred, average='weighted')[:3],
        roc_auc_score(y_test, y_proba)
    ]
    bars = axes[1,0].bar(metrics, values,
                         color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    axes[1,0].set_ylim(0, 1)
    axes[1,0].set_title("Performance Metrics")
    for bar in bars:
        h = bar.get_height()
        axes[1,0].text(bar.get_x() + bar.get_width()/2, h + 0.01,
                       f'{h:.4f}', ha='center', fontweight='bold')

    # Summary box
    axes[1,1].axis('off')
    summary_text = f"Test Samples: {len(y_test)}\nCorrect Predictions: {accuracy_score(y_test, y_pred)*len(y_test):.0f}"
    axes[1,1].text(0.5, 0.5, summary_text, transform=axes[1,1].transAxes,
                   ha='center', va='center', fontsize=14,
                   bbox=dict(boxstyle="round", facecolor="lightgray"))

    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "full_presentation_report.png", dpi=300, bbox_inches='tight')
    plt.show()


def save_model(model, filepath: Path) -> None:
    """Save the trained model to disk."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)
    logger.info(f"Model saved successfully: {filepath}")


def main() -> None:
    """Main training pipeline execution."""
    try:
        X, y = load_and_prepare_data()
        best_model, X_test, y_test = train_model(X, y)
        y_pred, y_proba = evaluate_and_save_metrics(best_model, X_test, y_test)
        plot_and_save_results(y_test, y_pred, y_proba)
        save_model(best_model, MODEL_FILE)

        logger.info("Training completed successfully!")
        print(f"\nAll evaluation images saved to: {IMAGES_DIR.resolve()}")
        print("Ready for presentation!")

    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


if __name__ == "__main__":
    main()