"""Unit tests as check that a model exists and can be run."""

import os

import joblib
import numpy as np
import pytest
from sklearn.naive_bayes import GaussianNB

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR
from utils.log_metrics import log_metric

# Define test model version (should match your training invocation)
MODEL_VERSION = "test_model_dev"

category = "INFRASTRUCTURE_TESTING"

@pytest.fixture(scope="module")
def model_path():
    path = MODELS_DIR / MODEL_VERSION / f"{MODEL_VERSION}_Sentiment_Model.pkl"
    if not path.exists():
        pytest.skip(f"Trained model not found at: {path}")
    return path


def test_model_file_exists(model_path):
    """Check that the model file exists."""
    exists = os.path.exists(model_path)
    log_metric("MODEL_FILE_EXISTS", exists, message="Model file found" if exists else "Model file missing", category=category)
    assert exists, f"Model file not found: {model_path}"


def test_model_can_be_loaded(model_path):
    """Check that the model file is loadable and of correct type."""
    model = joblib.load(model_path)
    correct_type = isinstance(model, GaussianNB)
    assert correct_type, "Loaded model is not a GaussianNB instance"
    log_metric("MODEL_LOADABLE", correct_type, message="Model loaded and is GaussianNB", category=category)


def test_model_can_predict(model_path):
    """Optional: Load test features and check model predicts without error."""
    x_test_path = PROCESSED_DATA_DIR / "features_test.npy"
    if not x_test_path.exists():
        pytest.skip(f"Test features not found: {x_test_path}")
    x_test = np.load(x_test_path)

    model = joblib.load(model_path)
    try:
        y_pred = model.predict(x_test)
        success = y_pred.shape[0] == x_test.shape[0]
        log_metric("MODEL_PREDICT_SHAPE_OK", success, message=f"Predicted {y_pred.shape[0]} samples", category=category)
        assert success, "Prediction output size mismatch"
    except Exception as e:
        log_metric("MODEL_PREDICT_ERROR", False, message=str(e), category=category)
        pytest.fail(f"Model prediction failed: {e}")
