"""Train the sentiment analysis model using preprocessed .npy files."""

from pathlib import Path

import joblib
import numpy as np
import typer
from loguru import logger
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR
from model_training.ensure_versioning import Ensurance

app = typer.Typer()


@app.command()
def train(
    features_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    labels_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
    version: str = None,
    evaluate: bool = True,
):
    """
    Trains and saves a Gaussian Naive Bayes model.

    Optionally evaluates the model if evaluate=True.
    """
    version = version or Ensurance().return_version()
    logger.info(f"Using model version: {version}")

    logger.info("Loading training data...")
    x = np.load(features_path)
    y = np.load(labels_path)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )
    np.save(PROCESSED_DATA_DIR / "features_test.npy", x_test)
    np.save(PROCESSED_DATA_DIR / "labels_test.npy", y_test)

    model_dir = MODELS_DIR / version
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{version}_Sentiment_Model.pkl"

    logger.info("Training Gaussian Naive Bayes model...")
    classifier = GaussianNB()
    classifier.fit(x_train, y_train)
    joblib.dump(classifier, model_path)
    logger.info(f"Model saved to {model_path}")

    if evaluate:
        logger.info("Evaluating model...")
        y_pred = classifier.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"Accuracy: {acc}")
        logger.info(f"Confusion Matrix:\n{cm}")


if __name__ == "__main__":
    app()
