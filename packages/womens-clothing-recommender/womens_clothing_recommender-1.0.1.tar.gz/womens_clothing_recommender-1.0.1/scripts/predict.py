# scripts/predict.py
"""
Interactive prediction tool for the trained recommendation model.
Allows users to input review details and get instant prediction.
"""

import os
import sys
import joblib
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import MODEL_FILE


def load_model(model_path) -> joblib:
    """Load the trained model from disk."""
    return joblib.load(model_path)


def check_model_exists(model_path) -> None:
    """Check if model file exists. Exit if not."""
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        print("Please train the model first using: python main.py train")
        raise SystemExit(1)


def get_user_input() -> pd.DataFrame:
    """Collect review information from user via console."""
    print("\n" + "="*60)
    print(" CUSTOMER RECOMMENDATION PREDICTION TOOL ")
    print("="*60)
    print("Leave blank and press Enter to use default value.\n")

    data = {
        'Clothing ID': input("Clothing ID (e.g. 1077) [1077]: ") or "1077",
        'Age': int(input("Age [35]: ") or "35"),
        'Title': input("Review Title [Great dress!] [Great dress!]: ") or "Great dress!",
        'Review Text': input("Review Text [Loved it, perfect fit] [Loved it, perfect fit]: ") or "Loved it, perfect fit",
        'Rating': int(input("Rating (1-5) [5]: ") or "5"),
        'Positive Feedback Count': int(input("Positive Feedback Count [3]: ") or "3"),
        'Division Name': input("Division (General/General Petite/Initmates) [General]: ") or "General",
        'Department Name': input("Department (Dresses/Tops/Bottoms etc.) [Dresses]: ") or "Dresses",
        'Class Name': input("Class Name (Dresses/Knits etc.) [Dresses]: ") or "Dresses"
    }
    return pd.DataFrame([data])


def main() -> None:
    """Main interactive prediction loop."""
    try:
        check_model_exists(MODEL_FILE)
        model = load_model(MODEL_FILE)

        print("\nModel loaded successfully!\n")

        while True:
            try:
                df_input = get_user_input()
                prediction = model.predict(df_input)[0]
                probability = model.predict_proba(df_input)[0]

                print("\n" + "="*60)
                print(" PREDICTION RESULT ")
                print("="*60)
                status = "RECOMMENDED" if prediction == 1 else "NOT RECOMMENDED"
                print(f" Prediction: {status}")
                print(f" Confidence → Recommend: {probability[1]:.1%} | Not Recommend: {probability[0]:.1%}")
                print("="*60)

                if input("\nMake another prediction? (y/n): ").strip().lower() != 'y':
                    print("Goodbye!\n")
                    break

            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.\n")
            except Exception as e:
                print(f"Error during prediction: {e}\n")

    except KeyboardInterrupt:
        print("\n\nPrediction interrupted. Goodbye!")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()