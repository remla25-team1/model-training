from pathlib import Path
from loguru import logger
import typer
import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def train_and_save_model(version, X_train, y_train):
    ''' 
    Trains the Gaussian Naive Bayes model and creates a directory for the model version and saves the trained model in that directory.
    input:
    - version: str, model version name
    - X_train: array-like, training data features
    - y_train: array-like, training data labels
    '''
    # Create directory for output model
    model_dir = MODELS_DIR / version
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{version}_Sentiment_Model.pkl"
    
    # Fit a Gaussian Naive Bayes classifier to the training data
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    
    # Save model
    joblib.dump(classifier, model_path)
    logger.info(f"Model trained and saved to: {model_path}")


@app.command()
def main(
    version: str = typer.Option(..., help="Model version name (e.g., v1.0.0)"),
    features_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    labels_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
):
    # Priority: CLI arg > dynamic_version.txt > VERSION.txt
    if version is None:
        version_file = Path("dynamic_version.txt")
        if version_file.exists():
            with open(version_file) as f:
                version = f.read().strip()
        else:
            with open("VERSION.txt") as f:
                version = f.read().strip()  # Fallback to base version
                
    # Load training data
    logger.info(f"Loading training data from {features_path} and {labels_path}")
    X_train = np.load(features_path)
    y_train = np.load(labels_path)

    # Train and save model
    logger.info(f"Training model version: {version}")
    train_and_save_model(version, X_train, y_train)


if __name__ == "__main__":
    app()
