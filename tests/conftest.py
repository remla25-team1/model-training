"""Fixture to ensure the model is trained before running tests."""

import os

import numpy as np
import pytest

from model_training.train import train


@pytest.fixture(scope="module", name="model_file")
def trained_model_file(tmp_path_factory):
    """
    Fixture to ensure the model is trained before running tests.

    If the model file does not exist, it will call the train function and return the
    path.
    """
    model_version = "test_model_dev"
    model_path = f"models/{model_version}/{model_version}_Sentiment_Model.pkl"

    # Skip if raw data isn't available
    raw_data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(raw_data_path):
        pytest.skip(f"Test data not found: {raw_data_path}")

    # Trigger training if model doesn't exist
    if not os.path.exists(model_path):
        # Generate dummy features and labels if not already present
        x = np.random.rand(100, 10)
        y = np.random.randint(0, 2, 100)
        np.save("data/processed/features_train.npy", x)
        np.save("data/processed/labels_train.npy", y)
        # Call train function
        train(
            features_path="data/processed/features_train.npy",
            labels_path="data/processed/labels_train.npy",
            version=model_version,
            evaluate=False,
        )

    return model_path
