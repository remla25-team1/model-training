"""Fixture to ensure the model is trained before running tests."""

import os

import pytest

from model_training.training import SentimentModel


@pytest.fixture(scope="module", name="model_file")
def trained_model_file():
    """
    Fixture to ensure the model is trained before running tests.

    If the model file does not exist, it will train the model and return the path.
    """
    model_version = "test_model_dev"
    model_path = f"models/{model_version}/{model_version}_Sentiment_Model.pkl"
    if not os.path.exists(model_path):
        model = SentimentModel("data/raw/a1_RestaurantReviews_HistoricDump.tsv")
        corpus = model.preprocess_data()
        x, y = model.transform_data(corpus)
        x_train, x_test, y_train, y_test = model.divide_data(x, y)
        model.fitting(model_version, x_train, x_test, y_train, y_test)
    return model_path
