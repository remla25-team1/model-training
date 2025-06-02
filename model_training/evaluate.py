"""Evaluation utilities and CLI for the sentiment analysis model."""

from pathlib import Path

import joblib
import numpy as np
import typer
import json
import os

from loguru import logger
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR

app = typer.Typer()


def save_confusion_matrix(y_true, y_pred, output_path):
    """
    Save confusion matrix of classifier on test data.

    input:
    - y_true: array-like, true labels
    - y_pred: array-like, predicted labels
    - output_path: str, where to store the confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)
    np.save(output_path, cm)
    logger.info(f"Confusion matrix saved to {output_path}")


def save_classification_report(y_true, y_pred, output_path):
    """
    Save classification report to file.

    input:
    - y_true: array-like, true labels
    - y_pred: array-like, predicted labels
    - output_path: str, where to store the classification report
    """
    report = classification_report(y_true, y_pred)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info(f"Classification report saved to {output_path}")


def evaluate_model(version, classifier, x_test, y_test):
    """
    Evaluate the trained model on test data.

    input:
    - version: str, model version name
    - classifier: trained model
    - x_test: array-like, test features
    - y_test: array-like, true test labels
    """
    # Predict
    y_pred = classifier.predict(x_test)

    # Save confusion matrix and classification report
    cm_path = REPORTS_DIR / f"{version}_confusion_matrix.npy"
    report_path = REPORTS_DIR / f"{version}_classification_report.txt"
    save_confusion_matrix(y_test, y_pred, cm_path)
    save_classification_report(y_test, y_pred, report_path)

    # Log accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy:.4f}")

    # Store accuracy in JSON
    metrics = {"Accuracy": accuracy}
    # Make sure the directory exists
    os.makedirs("experiments", exist_ok=True)
    with open("experiments/metrics.json", "w") as f:
        json.dump(metrics, f)


@app.command()
def main(
    version: str = typer.Option(..., help="Model version name (e.g., v1.0.0)"),
    features_path: Path = PROCESSED_DATA_DIR / "features_test.npy",
    labels_path: Path = PROCESSED_DATA_DIR / "labels_test.npy",
):
    """
    CLI entry point for evaluating the sentiment analysis model.

    Loads test data and model, evaluates, and saves reports.
    """
    # Load test data
    logger.info(f"Loading test data from {features_path} and {labels_path}")
    x_test = np.load(features_path)
    y_test = np.load(labels_path)

    # Load model
    model_path = MODELS_DIR / version / f"{version}_Sentiment_Model.pkl"
    logger.info(f"Loading model from {model_path}")
    classifier = joblib.load(model_path)

    # Evaluate
    evaluate_model(version, classifier, x_test, y_test)


if __name__ == "__main__":
    app()
