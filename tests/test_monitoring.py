from sklearn.metrics import accuracy_score
from model_training.training import SentimentModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import joblib
from lib_ml.preprocessing import Preprocessor
import pytest
import os
import numpy as np
import pandas as pd

@pytest.fixture(scope="module")
def trained_model_file():
    model_version = "test_model_dev"
    model_path = f"models/{model_version}/{model_version}_Sentiment_Model.pkl"
    if not os.path.exists(model_path):
        model = SentimentModel("data/a1_RestaurantReviews_HistoricDump.tsv")
        corpus = model.preprocess_data()
        X, y = model.transform_data(corpus)
        X_train, X_test, y_train, y_test = model.divide_data(X, y)
        model.fitting(model_version, X_train, X_test, y_train, y_test)
    return model_path

def test_model_on_simulated_fresh_inputs(trained_model_file):
    fresh_df = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", sep="\t")
    model = joblib.load(trained_model_file)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl") 
    pre = Preprocessor()
    processed = [pre.process_item(text) for text in fresh_df["Review"]]
    X = vectorizer.transform(processed).toarray()
    preds = model.predict(X)
    assert preds.shape == (len(fresh_df),), "Unexpected prediction output shape"
    positive_ratio = np.mean(preds)
    print(f"[Fresh Inputs] Total samples: {len(fresh_df)}")
    print(f"[Prediction Ratio] Positive: {positive_ratio:.2f}, Negative: {1 - positive_ratio:.2f}")
    assert 0.2 < positive_ratio < 0.8, f"Prediction distribution suspicious: {positive_ratio:.2f}"
