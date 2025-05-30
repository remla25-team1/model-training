"""Preprocessing utilities for the sentiment analysis model training pipeline."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import typer
from lib_ml.preprocessing import Preprocessor
from loguru import logger
from sklearn.feature_extraction.text import CountVectorizer

from model_training.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


def preprocess_data(dataset):
    """
    Preprocesses the dataset using the Preprocessor class.

    input:
    - dataset: DataFrame, the raw dataset containing the text data and labels
    output:
    - corpus: list, the preprocessed text data
    """
    preprocessor = Preprocessor()
    logger.info("Starting preprocessing...")
    corpus = preprocessor.process(dataset)
    logger.info("Preprocessing completed.")

    return corpus


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
    output_path: Path = PROCESSED_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
    save_npy: bool = True,
):
    """CLI entry point for preprocessing the dataset."""
    # Load raw data from file
    logger.info(f"Loading dataset from: {input_path}")
    dataset = pd.read_csv(input_path, delimiter="\t", quoting=3)

    # Preprocess data
    corpus = preprocess_data(dataset)
    processed_df = pd.DataFrame({"Review": corpus, "Liked": dataset["Liked"]})

    # Remove any rows with missing or empty reviews
    processed_df.dropna(subset=["Review"], inplace=True)
    processed_df = processed_df[processed_df["Review"].str.strip() != ""]

    # Save cleaned data
    processed_df.to_csv(output_path, sep="\t", index=False)
    logger.info(f"Saved preprocessed data to {output_path}")

    if save_npy:
        logger.info("Converting text to BoW features...")
        vectorizer = CountVectorizer(max_features=1420)
        x = vectorizer.fit_transform(processed_df["Review"]).toarray()
        y = processed_df["Liked"].values

        joblib.dump(vectorizer, PROCESSED_DATA_DIR / "c1_BoW_Sentiment_Model.pkl")
        np.save(PROCESSED_DATA_DIR / "features_train.npy", x)
        np.save(PROCESSED_DATA_DIR / "labels_train.npy", y)
        logger.info("Saved features and labels as .npy files.")


if __name__ == "__main__":
    app()
