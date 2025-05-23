from pathlib import Path
from loguru import logger
import typer
import joblib
import numpy as np

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def predict(classifier, X):
    '''
    Generate predictions from the classifier on the input features X.
    input:
    - classifier: trained model
    - X: array-like, features to predict on
    output:
    - y_pred: array-like, predictions
    '''
    y_pred = classifier.predict(X)
    logger.info(f"Generated predictions for {len(y_pred)} samples.")

    return y_pred


@app.command()
def main(
    version: str = typer.Option(..., help="Model version name (e.g., v1.0.0)"),
    features_path: Path = PROCESSED_DATA_DIR / "features_test.npy",
):
    # Load test data
    logger.info(f"Loading features from {features_path}")
    X_test = np.load(features_path)

    # Load model
    model_path = MODELS_DIR / version / f"{version}_Sentiment_Model.pkl"
    logger.info(f"Loading model from {model_path}")
    classifier = joblib.load(model_path)

    # Predict
    predictions = predict(classifier, X_test)

    # Save output predictions to a file
    np.save(PROCESSED_DATA_DIR / f"predictions_{version}.npy", predictions)
    logger.info(f"Saved predictions to {PROCESSED_DATA_DIR / f'predictions_{version}.npy'}")


if __name__ == "__main__":
    app()
