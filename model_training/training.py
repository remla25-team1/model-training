# pylint: disable=redefined-outer-name
"""Training utilities and CLI for the sentiment analysis model."""

import logging
import os
import pickle
import sys

import joblib
import pandas as pd
from lib_ml.preprocessing import Preprocessor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# Global logging config (silences 3rd-party libraries)
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Only log info and above from code


class SentimentModel:
    """Class for training and evaluating a sentiment analysis model."""

    def __init__(self, dataset_path):
        """
        Initializes the SentimentModel class with the dataset path.

        input:
        - dataset_path: str, path to the dataset file
        """
        self.dataset = pd.read_csv(dataset_path, delimiter="\t", quoting=3)
        logger.info("Dataset loaded from %s", dataset_path)

    def preprocess_data(self):
        """
        Preprocesses the dataset using the Preprocessor class.

        output:
        - corpus: list, the preprocessed text data
        """
        preprocessor = Preprocessor()
        logger.info("Starting preprocessing...")
        corpus = preprocessor.process(self.dataset)
        logger.info("Preprocessing completed.")
        return corpus

    def transform_data(self, corpus):
        """
        Transforms the dataset into a bag-of-words representation using CountVectorizer.

        input:
        - corpus: list, the text data to be transformed
        output:
        - x: array-like, the transformed feature set
        - y: array-like, the target variable
        """
        cv = CountVectorizer(max_features=1420)
        x = cv.fit_transform(corpus).toarray()
        y = self.dataset.iloc[:, -1].values

        # Saving BoW dictionary to later use in prediction
        os.makedirs("bow", exist_ok=True)
        bow_path = "bow/c1_BoW_Sentiment_Model.pkl"
        with open(bow_path, "wb") as f:
            pickle.dump(cv, f)

        return x, y

    def divide_data(self, x, y):
        """
        Splits the dataset into training and testing sets.

        input:
        - x: array-like, feature set
        - y: array-like, target variable
        output:
        - x_train: array-like, training feature set
        - x_test: array-like, testing feature set
        - y_train: array-like, training target variable
        - y_test: array-like, testing target variable
        """
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=0
        )
        return x_train, x_test, y_train, y_test

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def fit_and_save(self, version, x_train, y_train):
        """
        Trains the Gaussian Naive Bayes model and creates a directory for the model
        version and saves the trained model in that directory.

        input:
        - version: str, the version of the model to be saved
        - x_train: array-like, training data features
        - y_train: array-like, training data labels
        output:
        - None, the model is saved to a file
        """
        model_dir = os.path.join("models", version)
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"{version}_Sentiment_Model.pkl")

        classifier = GaussianNB()
        classifier.fit(x_train, y_train)
        joblib.dump(classifier, model_path)
        logger.info("Model saved to %s", model_path)
        logger.info("Model version: %s", version)
        return classifier

    def predict(self, classifier, x_test, y_test):
        """Makes predictions and logs metrics."""
        y_pred = classifier.predict(x_test)
        logger.info("Predictions: %s", y_pred)

        cm = confusion_matrix(y_test, y_pred)
        logger.info("Confusion Matrix: %s", cm)

        acc = accuracy_score(y_test, y_pred)
        logger.info("Accuracy: %s", acc)
        return y_pred, cm, acc


if __name__ == "__main__":
    # Example usage
    DATASET_PATH = "data/a1_RestaurantReviews_HistoricDump.tsv"  # Path to your dataset
    if len(sys.argv) < 2:
        logger.error("Usage: python training.py <model_version>")
        sys.exit(1)
    model_version = sys.argv[
        1
    ]  # Version of the model, read from the tag of the git release

    # Initialize the SentimentModel class
    sentiment_model = SentimentModel(DATASET_PATH)

    # Preprocess the data
    corpus_main = sentiment_model.preprocess_data()

    # Transform the data into a bag-of-words representation
    x_main, y_main = sentiment_model.transform_data(corpus_main)

    # Divide the data into training and testing sets
    x_train_main, x_test_main, y_train_main, y_test_main = sentiment_model.divide_data(
        x_main, y_main
    )

    # Fit the model and save it
    classifier = sentiment_model.fit_and_save(model_version, x_train_main, y_train_main)

    # Make predictions and evaluate the model
    y_pred, cm, acc = sentiment_model.predict(classifier, x_test_main, y_test_main)
