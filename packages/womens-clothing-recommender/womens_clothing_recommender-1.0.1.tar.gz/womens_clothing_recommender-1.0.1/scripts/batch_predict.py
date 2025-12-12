# scripts/batch_predict.py
"""
Batch prediction script.
Reads a CSV file with reviews and adds prediction columns.
"""

import os
import sys
import joblib
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import MODEL_FILE


def load_model(model_path):
    """Load the trained model."""
    return joblib.load(model_path)


def check_model_exists(model_path) -> None:
    """Exit if model is not trained."""
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        print("Run 'python main.py train' first.")
        raise SystemExit(1)


def main(csv_path: str) -> None:
    """Process entire CSV file and save predictions."""
    try:
        check_model_exists(MODEL_FILE)
        model = load_model(MODEL_FILE)

        print(f"\nLoading data from: {csv_path}")
        df = pd.read_csv(csv_path)

        required_cols = [
            'Clothing ID', 'Age', 'Title', 'Review Text', 'Rating',
            'Positive Feedback Count', 'Division Name', 'Department Name', 'Class Name'
        ]

        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Missing required columns: {missing_cols}")
            print("Required columns:", required_cols)
            return

        print("Making predictions...")
        predictions = model.predict(df[required_cols])
        probabilities = model.predict_proba(df[required_cols])[:, 1]

        df['Predicted_Recommendation'] = ['Recommended' if p == 1 else 'Not Recommended' for p in predictions]
        df['Recommendation_Probability'] = probabilities

        output_file = "batch_predictions_output.csv"
        df.to_csv(output_file, index=False)
        print(f"Success! Predictions saved to: {output_file}")
        print(f"Total reviews processed: {len(df)}")

    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
    except Exception as e:
        print(f"Error during batch prediction: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/batch_predict.py <path_to_csv_file>")
        sys.exit(1)
    main(sys.argv[1])