"""Tests for model monitoring and prediction on fresh inputs."""

import os

import joblib
import numpy as np
import pandas as pd
import pytest
from lib_ml.preprocessing import Preprocessor
from utils.log_metrics import log_metric

category = "MONITORING_TESTING"

def test_model_on_simulated_fresh_inputs(model_file):
    """
    Test the model's prediction on simulated fresh inputs.

    This test checks if the model can handle new data and provides a reasonable
    prediction ratio.
    """
    data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(data_path):
        pytest.skip(f"Test data not found: {data_path}")

    fresh_df = pd.read_csv(data_path, sep="\t")
    model = joblib.load(model_file)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    pre = Preprocessor()
    processed = [pre.process_item(text) for text in fresh_df["Review"]]
    x = vectorizer.transform(processed).toarray()
    preds = model.predict(x)
    # Validate output shape
    correct_shape = preds.shape == (len(fresh_df),)
    log_metric("FRESH_PREDICTION_SHAPE_OK", correct_shape, message="Prediction output shape matches input size", category=category)
    assert correct_shape, "Unexpected prediction output shape"
    # Analyze prediction distribution
    positive_ratio = np.mean(preds)
    negative_ratio = 1 - positive_ratio
    log_metric(
        "FRESH_POSITIVE_RATIO",
        positive_ratio,
        message= "Prediction distribution is suspicious if not between 0.2 and 0.8",
        category=category,
        precision=2
    )
    assert (
        0.2 < positive_ratio < 0.8
    ), f"Prediction distribution suspicious: {positive_ratio:.2f}"
