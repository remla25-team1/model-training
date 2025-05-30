"""Unit tests as check that a model exists and can be run."""

import os

import joblib
import numpy as np
import pytest
from sklearn.naive_bayes import GaussianNB

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR

# Define test model version (should match your training invocation)
MODEL_VERSION = "test_model_dev"


@pytest.fixture(scope="module")
def model_path():
    path = MODELS_DIR / MODEL_VERSION / f"{MODEL_VERSION}_Sentiment_Model.pkl"
    if not path.exists():
        pytest.skip(f"Trained model not found at: {path}")
    return path


def test_model_file_exists(model_path):
    """Check that the model file exists."""
    assert os.path.exists(model_path), f"Model file not found: {model_path}"


def test_model_can_be_loaded(model_path):
    """Check that the model file is loadable and of correct type."""
    model = joblib.load(model_path)
    assert isinstance(model, GaussianNB), "Loaded model is not a GaussianNB instance"


def test_model_can_predict(model_path):
    """Optional: Load test features and check model predicts without error."""
    x_test_path = PROCESSED_DATA_DIR / "features_test.npy"
    if not x_test_path.exists():
        pytest.skip(f"Test features not found: {x_test_path}")
    x_test = np.load(x_test_path)

    model = joblib.load(model_path)
    try:
        y_pred = model.predict(x_test)
    except Exception as e:
        pytest.fail(f"Model prediction failed: {e}")

    assert y_pred.shape[0] == x_test.shape[0], "Prediction output size mismatch"
