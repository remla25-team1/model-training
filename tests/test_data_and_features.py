import time

import numpy as np
import pandas as pd
from lib_ml.preprocessing import Preprocessor
from sklearn.feature_extraction.text import CountVectorizer


def test_data_quality():
    dataset = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", sep="\t")
    # check null values
    assert dataset['Review'].notnull().all(), "Data contains null reviews"
    assert dataset['Liked'].notnull().all(), "Data contains null labels"
    # test if there are empty strings
    assert not (dataset['Review'].str.strip() == '').any(), "There exists empty reviews"
    # test label values
    labels = set(dataset['Liked'].unique())
    assert set(dataset['Liked'].unique()).issubset({0, 1}), "Labels are not binary (0 or 1)"
    print(f"[Data Quality] {len(dataset)} samples checked. Labels: {labels}")


def test_feature_distribution():
    dataset = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", sep="\t")
    reviews = dataset["Review"].dropna().tolist()
    preprocessor = Preprocessor() 
    processed_reviews = [preprocessor.process_item(r) for r in reviews]
    vectorizer = CountVectorizer(max_features=1420)
    X = vectorizer.fit_transform(processed_reviews)
    # check structure
    print(f"[Feature Distribution] Sample size: {X.shape[0]}, Features: {X.shape[1]}")
    assert X.shape[0] == len(processed_reviews), "Number of rows in feature matrix doesn't match input"
    assert X.shape[1] == 1420, "Unexpected number of feature columns"
    #check for NaN / Inf
    dense = X.toarray()
    assert np.isfinite(dense).all(), "Feature matrix contains NaN or Inf"
    # check sparsity 
    sparsity = (dense == 0).mean()
    print(f"[Sparsity] Zero ratio: {sparsity:.4f}")
    assert sparsity < 0.999, f"Feature matrix too sparse: {sparsity:.5f} zeros"


def test_feature_preprocessing_latency():
    dataset = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", sep="\t")
    sample = dataset['Review'].dropna().sample(min(100, len(dataset)))
    start = time.time()
    for review in sample:
        _ = review.lower().strip()
    latency = (time.time() - start) / len(sample)
    print(f"[Latency] Avg preprocessing time per review: {latency:.5f}s (on {len(sample)} samples)")
    assert latency < 0.01, f"Feature processing latency too high: {latency:.5f}s"
