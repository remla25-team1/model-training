"""Tests for model monitoring and prediction on fresh inputs."""

import joblib
import numpy as np
import pandas as pd
from lib_ml.preprocessing import Preprocessor


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
