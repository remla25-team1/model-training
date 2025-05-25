import typer
import joblib
import numpy as np
import dvc.api
import yaml

from pathlib import Path
from loguru import logger
from pathlib import Path
from sklearn.naive_bayes import GaussianNB
from ensure_versioning import Ensurance

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
    features_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    labels_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
):
    # Make an instance of the ensurance we need
    ensurance = Ensurance()
    version = ensurance.return_version()

    # Load training data
    logger.info(f"Loading training data from {features_path} and {labels_path}")
    X_train = np.load(features_path)
    y_train = np.load(labels_path)

    # Train and save model
    logger.info(f"Training model version: {version}")
    train_and_save_model(version, X_train, y_train)


if __name__ == "__main__":
    app()
