"""Unit tests for data quality and feature extraction in the sentiment analysis
pipeline."""

import os
import time

import numpy as np
import pandas as pd
import pytest
from lib_ml.preprocessing import Preprocessor
from sklearn.feature_extraction.text import CountVectorizer

# Adjust this path if DVC moves the file or if renamed in preprocessing stage
DATA_PATH = "data/raw/a1_RestaurantReviews_HistoricDump.tsv"


def test_data_quality():
    """Check for null values, empty reviews, and label correctness."""
    if not os.path.exists(DATA_PATH):
        pytest.skip(f"Test data not found: {DATA_PATH}")

    dataset = pd.read_csv(DATA_PATH, sep="\t")

    # Null checks
    assert dataset["Review"].notnull().all(), "Data contains null reviews"
    assert dataset["Liked"].notnull().all(), "Data contains null labels"

    # Empty string check
    assert not (dataset["Review"].str.strip() == "").any(), "There exists empty reviews"

    # Binary label check
    labels = set(dataset["Liked"].unique())
    assert labels.issubset({0, 1}), f"Labels are not binary: {labels}"
    print(f"[Data Quality] {len(dataset)} samples checked. Labels: {labels}")


def test_feature_distribution():
    """Ensure feature matrix is structurally valid and not overly sparse."""
    if not os.path.exists(DATA_PATH):
        pytest.skip(f"Test data not found: {DATA_PATH}")

    dataset = pd.read_csv(DATA_PATH, sep="\t")
    reviews = dataset["Review"].dropna().tolist()

    preprocessor = Preprocessor()
    processed_reviews = [preprocessor.process_item(r) for r in reviews]

    vectorizer = CountVectorizer(max_features=1420)
    x = vectorizer.fit_transform(processed_reviews)

    assert x.shape[0] == len(
        processed_reviews
    ), "Mismatch in review count and feature rows"
    assert x.shape[1] == 1420, "Unexpected number of feature columns"

    dense = x.toarray()
    assert np.isfinite(dense).all(), "Feature matrix contains NaN or Inf"

    sparsity = (dense == 0).mean()
    print(f"[Sparsity] Zero ratio: {sparsity:.4f}")
    assert sparsity < 0.999, f"Feature matrix too sparse: {sparsity:.5f} zeros"


def test_feature_preprocessing_latency():
    """Test average latency for basic text cleaning."""
    if not os.path.exists(DATA_PATH):
        pytest.skip(f"Test data not found: {DATA_PATH}")

    dataset = pd.read_csv(DATA_PATH, sep="\t")
    sample = dataset["Review"].dropna().sample(min(100, len(dataset)))

    start = time.time()
    for review in sample:
        _ = review.lower().strip()
    latency = (time.time() - start) / len(sample)

    print(
        f"[Latency] Avg preprocessing time per review: {latency:.5f}s (on {len(sample)} samples)"
    )
    assert latency < 0.01, f"Feature processing latency too high: {latency:.5f}s"
