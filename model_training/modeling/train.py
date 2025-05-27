"""Training entry point and utilities for the sentiment analysis model."""

from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import typer
from loguru import logger
from sklearn.naive_bayes import GaussianNB

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR

from model_training.modeling.ensure_versioning import Ensurance

app = typer.Typer()


def train_and_save_model(version, x_train, y_train):
    """
    Trains the Gaussian Naive Bayes model and creates a directory for the model version
    and saves the trained model in that directory.

    input:
    - version: str, model version name
    - x_train: array-like, training data features
    - y_train: array-like, training data labels
    """
    # Create directory for output model
    model_dir = MODELS_DIR / version
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{version}_Sentiment_Model.pkl"

    # Fit a Gaussian Naive Bayes classifier to the training data
    classifier = GaussianNB()
    classifier.fit(x_train, y_train)

    # Save model
    joblib.dump(classifier, model_path)
    logger.info(f"Model trained and saved to: {model_path}")


@app.command()
def main(
    features_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    labels_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
    version: Optional[str] = None,  # Allow override
):
    """
    CLI entry point for training and saving the sentiment analysis model.

    Loads features and labels, trains the model, and saves it with the specified
    version.
    """
    version = version or Ensurance().return_version()
    logger.info(
        f"Using model version: {version} (from {'CLI' if version else 'Ensurance'})"
    )

    # Load training data
    logger.info(f"Loading training data from {features_path} and {labels_path}")
    x_train = np.load(features_path)
    y_train = np.load(labels_path)

    # Train and save model
    logger.info(f"Training model version: {version}")
    train_and_save_model(version, x_train, y_train)


if __name__ == "__main__":
    app()
