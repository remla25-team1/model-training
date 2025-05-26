import os

import joblib
import numpy as np
import pandas as pd
import pytest
from lib_ml.preprocessing import Preprocessor

from model_training.training import SentimentModel


@pytest.fixture(scope="module")
def trained_model_file():
    """
    Fixture to ensure the model is trained before running tests.

    If the model file does not exist, it will train the model and return the path.
    """
    model_version = "test_model_dev"
    model_path = f"models/{model_version}/{model_version}_Sentiment_Model.pkl"
    if not os.path.exists(model_path):
        model = SentimentModel("data/a1_RestaurantReviews_HistoricDump.tsv")
        corpus = model.preprocess_data()
        x, y = model.transform_data(corpus)
        X_train, X_test, y_train, y_test = model.divide_data(x, y)
        model.fitting(model_version, X_train, X_test, y_train, y_test)
    return model_path


def test_model_on_simulated_fresh_inputs(trained_model_file):
    """
    Test the model's prediction on simulated fresh inputs.

    This test checks if the model can handle new data and provides a reasonable
    prediction ratio.
    """
    fresh_df = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", sep="\t")
    model = joblib.load(trained_model_file)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    pre = Preprocessor()
    processed = [pre.process_item(text) for text in fresh_df["Review"]]
    x = vectorizer.transform(processed).toarray()
    preds = model.predict(x)
    assert preds.shape == (len(fresh_df),), "Unexpected prediction output shape"
    positive_ratio = np.mean(preds)
    print(f"[Fresh Inputs] Total samples: {len(fresh_df)}")
    print(
        f"[Prediction Ratio] Positive: {positive_ratio:.2f}, Negative: {1 - positive_ratio:.2f}"
    )
    assert (
        0.2 < positive_ratio < 0.8
    ), f"Prediction distribution suspicious: {positive_ratio:.2f}"
