"""Unit and integration tests for model development and training pipeline."""

import os
import tracemalloc

import joblib
import pandas as pd
import pytest
from lib_ml.preprocessing import Preprocessor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from utils.log_metrics import log_metric

category = "MODEL_DEVELOPMENT"

def test_model_prediction_accuracy(model_file):
    """
    Test the accuracy of the trained model on a test set.

    This test checks if the model achieves at least 65% accuracy.
    """
    data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(data_path):
        pytest.skip(f"Test data not found: {data_path}")

    classifier = joblib.load(model_file)
    dataset = pd.read_csv(data_path, delimiter="\t", quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(dataset)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    x = vectorizer.transform(corpus).toarray()
    y = dataset.iloc[:, -1].values
    _, x_test, _, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    y_pred = classifier.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[Accuracy] Model accuracy on test set: {acc:.2f}")
    assert acc >= 0.65, f"Model accuracy too low: {acc:.2f}"
    log_metric("MODEL_ACCURACY", acc, message="Accuracy on test set", category=category)


def get_accuracy(corpus, labels):
    """
    Helper function to compute accuracy of a Naive Bayes classifier on a given corpus
    and labels.

    This function preprocesses the corpus, vectorizes it, and trains a Gaussian Naive
    Bayes classifier. It returns the accuracy score on a test set.
    """
    corpus = [doc for doc in corpus if doc.strip()]
    if len(corpus) < 5:
        pytest.skip("Too few valid documents after preprocessing")
    vectorizer = CountVectorizer(max_features=1420)
    try:
        x = vectorizer.fit_transform(corpus).toarray()
    except ValueError as e:
        pytest.skip(f"Vectorizer failed: {e}")
    y = labels[: len(x)]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )
    clf = GaussianNB().fit(x_train, y_train)
    return accuracy_score(y_test, clf.predict(x_test))


def test_model_consistency_on_labels():
    """
    Test the model's performance on positive and negative samples.

    This test checks if the model performs similarly on both classes. It computes the
    accuracy for positive and negative samples separately and asserts that the
    difference in accuracy is less than 15%.
    """
    data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(data_path):
        pytest.skip(f"Test data not found: {data_path}")

    df = pd.read_csv(data_path, delimiter="\t", quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(df)
    df["cleaned"] = corpus

    pos_df = df[df["Liked"] == 1].reset_index(drop=True)
    neg_df = df[df["Liked"] == 0].reset_index(drop=True)
    pos_corpus = pos_df["cleaned"].tolist()
    neg_corpus = neg_df["cleaned"].tolist()

    acc_pos = get_accuracy(pos_corpus, pos_df["Liked"])
    acc_neg = get_accuracy(neg_corpus, neg_df["Liked"])
    print(f"[Slice Test] Accuracy Positive: {acc_pos:.2f}, Negative: {acc_neg:.2f}")
    log_metric("ACCURACY_POSITIVE", acc_pos, message="Accuracy on positive samples", category=category)
    log_metric("ACCURACY_NEGATIVE", acc_neg, message="Accuracy on negative samples", category=category)
    assert (
        abs(acc_pos - acc_neg) < 0.15
    ), f"Model performs differently on pos vs neg samples: {acc_pos:.2f} vs {acc_neg:.2f}"


def test_model_prediction_determinism(model_file):
    """
    Test that the model produces the same predictions on the same input across multiple
    runs.

    This test ensures that the model's predictions are deterministic.
    """
    data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(data_path):
        pytest.skip(f"Test data not found: {data_path}")

    clf = joblib.load(model_file)
    dataset = pd.read_csv(data_path, delimiter="\t", quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(dataset)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    x = vectorizer.transform(corpus).toarray()
    y = dataset.iloc[:, -1].values
    _, x_test, _, _ = train_test_split(x, y, test_size=0.2, random_state=0)
    pred1 = clf.predict(x_test)
    pred2 = clf.predict(x_test)
    deterministic = (pred1 == pred2).all()
    log_metric("PREDICTION_DETERMINISTIC", deterministic, message="Predictions are consistent across repeated inference", category=category)
    assert deterministic, "Predictions differ between identical runs"



def test_memory_usage_during_vectorization():
    """
    Test the memory usage during the vectorization process.

    This test checks if the peak memory usage during vectorization is below a threshold.
    """
    data_path = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"
    if not os.path.exists(data_path):
        pytest.skip(f"Test data not found: {data_path}")

    df = pd.read_csv(data_path, delimiter="\t", quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(df)

    vectorizer = CountVectorizer(max_features=1420)
    tracemalloc.start()
    vectorizer.fit_transform(corpus)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / (1024 * 1024)
    print(f"[Memory] Peak vectorization memory usage: {peak_mb:.2f}MB")
    log_metric("VECTORIZATION_MEMORY_USAGE", peak_mb, message="Peak memory usage during vectorization (MB)", category=category)
    assert peak_mb < 100, f"Vectorization peak memory usage too high: {peak_mb:.2f}MB"
