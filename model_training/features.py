from pathlib import Path
from loguru import logger
import typer
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

from model_training.config import PROCESSED_DATA_DIR, MODELS_DIR

app = typer.Typer()


def transform_data(dataset, bow_output_path):
    '''
    Transforms the dataset into a bag-of-words representation using CountVectorizer.
    input:
    - dataset: DataFrame, the preprocessed dataset containing the text data and labels
    - bow_output_path: str, where to store the CountVectorizer model
    output:
    - X: array-like, the transformed feature set
    - y: array-like, the target variable
    '''
    corpus = dataset["Review"].tolist()
    y = dataset["Label"].values 
    cv = CountVectorizer(max_features=1420)
    X = cv.fit_transform(corpus).toarray()

    # Save CountVectorizer model
    with open(bow_output_path, "wb") as f:
        pickle.dump(cv, f)
    logger.info(f"Saved CountVectorizer model to {bow_output_path}")

    return X, y


def split_data(X, y, test_size, random_state):
    '''
    Splits the dataset into training and testing sets.
    input:
    - X: array-like, feature set
    - y: array-like, target variable
    - test_size: int, size of test set
    - random_state: int, seed used when splitting 
    output:
    - X_train: array-like, training feature set
    - X_test: array-like, testing feature set
    - y_train: array-like, training target variable
    - y_test: array-like, testing target variable
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    logger.info(f"Split data into train and test sets with test size {test_size}")

    return X_train, X_test, y_train, y_test


@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
    features_train_path: Path = PROCESSED_DATA_DIR / "features_train.npy",
    features_test_path: Path = PROCESSED_DATA_DIR / "features_test.npy",
    labels_train_path: Path = PROCESSED_DATA_DIR / "labels_train.npy",
    labels_test_path: Path = PROCESSED_DATA_DIR / "labels_test.npy",
    bow_output_path: Path = MODELS_DIR / "c1_BoW_Sentiment_Model.pkl",
    test_size: float = 0.2,
    random_state: int = 1
):
    # Load preprocessed data from file
    logger.info(f"Loading dataset from: {input_path}")
    dataset = pd.read_csv(input_path, delimiter="\t", quoting=3)

    # Transform data
    X, y = transform_data(dataset, bow_output_path)

    # Split data 
    X_train, X_test, y_train, y_test = split_data(X, y, test_size, random_state)

    # Save splits
    np.save(features_train_path, X_train)
    np.save(features_test_path, X_test)
    np.save(labels_train_path, y_train)
    np.save(labels_test_path, y_test)
    logger.info(f"Saved train and test features and labels to {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    app()
