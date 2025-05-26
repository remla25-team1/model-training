"""Feature extraction and data splitting utilities for model training."""

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from loguru import logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from model_training.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def transform_data(dataset, bow_output_path):
    """
    Transforms the dataset into a bag-of-words representation using CountVectorizer.

    input:
    - dataset: DataFrame, the preprocessed dataset containing the text data and labels
    - bow_output_path: str, where to store the CountVectorizer model
    output:
    - x: array-like, the transformed feature set
    - y: array-like, the target variable
    """
    corpus = dataset["Review"].tolist()
    y = dataset["Liked"].values
    cv = CountVectorizer(max_features=1420)
    x = cv.fit_transform(corpus).toarray()

    # Save CountVectorizer model
    with open(bow_output_path, "wb") as f:
        pickle.dump(cv, f)
    logger.info(f"Saved CountVectorizer model to {bow_output_path}")

    return x, y


def split_data(x, y, test_size, random_state):
    """
    Splits the dataset into training and testing sets.

    input:
    - x: array-like, feature set
    - y: array-like, target variable
    - test_size: int, size of test set
    - random_state: int, seed used when splitting
    output:
    - x_train: array-like, training feature set
    - x_test: array-like, testing feature set
    - y_train: array-like, training target variable
    - y_test: array-like, testing target variable
    """
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )
    logger.info(f"Split data into train and test sets with test size {test_size}")

    return x_train, x_test, y_train, y_test


# pylint: disable=too-many-arguments, too-many-positional-arguments
@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
    features_train_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    features_test_path: Path = PROCESSED_DATA_DIR / "features_test.npy",
    labels_train_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
    labels_test_path: Path = PROCESSED_DATA_DIR / "labels_test.npy",
    bow_output_path: Path = MODELS_DIR / "c1_BoW_Sentiment_Model.pkl",
    test_size: float = 0.2,
    random_state: int = 1,
):
    """
    Main CLI entry point for feature extraction and data splitting.

    Loads the dataset, transforms it into features, splits into train/test, and saves
    the resulting arrays and vectorizer.
    """
    logger.info(f"Loading dataset from: {input_path}")
    dataset = pd.read_csv(input_path, delimiter="\t", quoting=3)

    # Transform data
    x, y = transform_data(dataset, bow_output_path)

    # Split data
    x_train, x_test, y_train, y_test = split_data(x, y, test_size, random_state)

    # Save splits
    np.save(features_train_path, x_train)
    np.save(features_test_path, x_test)
    np.save(labels_train_path, y_train)
    np.save(labels_test_path, y_test)
    logger.info(f"Saved train and test features and labels to {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    app()
