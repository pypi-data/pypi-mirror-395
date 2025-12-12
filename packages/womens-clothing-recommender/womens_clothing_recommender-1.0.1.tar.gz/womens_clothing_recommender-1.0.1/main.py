# main.py
import sys
import subprocess

def print_help():
    print("""
Usage:
    python main.py train                    → Trains the model (downloads dataset if missing)
    python main.py predict                  → Interactive prediction mode (console input)
    python main.py predict-batch <csv>      → Predicts all comments in the CSV file
    python main.py --help                   → Shows this help message
    """)

def run_train():
    print("Starting model training...")
    subprocess.run([sys.executable, "./scripts/train.py"], check=True)
    print("Training completed!")

def interactive_predict():
    subprocess.run([sys.executable, "./scripts/predict.py"], check=True)

def batch_predict(csv_path):
    subprocess.run([sys.executable, "./scripts/batch_predict.py",csv_path], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print_help()
    elif sys.argv[1] == "train":
        run_train()
    elif sys.argv[1] == "predict":
        interactive_predict()
    elif sys.argv[1] == "predict-batch" and len(sys.argv) == 3:
        batch_predict(sys.argv[2])
    else:
        print("Invalid command!")
        print_help()