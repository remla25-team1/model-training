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
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Only log info and above from code

class SentimentModel:
    def __init__(self, dataset_path):
        '''
        Initializes the SentimentModel class with the dataset path.
        input:
        - dataset_path: str, path to the dataset file
        '''
        
        # Load the dataset
        self.dataset = pd.read_csv(dataset_path, delimiter = '\t', quoting = 3)
        logger.info(f"Dataset loaded from {dataset_path}")
        
    def preprocess_data(self):
        '''
        Preprocesses the dataset using the Preprocessor class.
        output:
        - corpus: list, the preprocessed text data
        '''
        
        # Initialize the Preprocessing class
        preprocessor = Preprocessor()
        logger.info("Starting preprocessing...")
        # Do some preprocessing on the dataset
        corpus = preprocessor.process(self.dataset)
        logger.info("Preprocessing completed.")
        
        return corpus
    
    def transform_data(self, corpus):
        '''
        Transforms the dataset into a bag-of-words representation using CountVectorizer.
        input:
        - dataset: DataFrame, the dataset containing the text data and labels
        - corpus: list, the text data to be transformed
        output:
        - X: array-like, the transformed feature set
        - y: array-like, the target variable
        '''
        
        cv = CountVectorizer(max_features=1420)
        X = cv.fit_transform(corpus).toarray()
        y = self.dataset.iloc[:, -1].values
        
        # Saving BoW dictionary to later use in prediction
        os.makedirs('bow', exist_ok=True)
        bow_path = 'bow/c1_BoW_Sentiment_Model.pkl'
        pickle.dump(cv, open(bow_path, "wb"))
        
        return X, y

    def divide_data(self, X, y):
        '''
        Splits the dataset into training and testing sets.
        input:
        - X: array-like, feature set
        - y: array-like, target variable
        output:
        - X_train: array-like, training feature set
        - X_test: array-like, testing feature set
        - y_train: array-like, training target variable
        - y_test: array-like, testing target variable
        '''
        
        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        
        return X_train, X_test, y_train, y_test

    def fitting(self, version, X_train, X_test, y_train, y_test):
        ''' 
        Trains the Gaussian Naive Bayes model and creates a directory for the model version and saves the trained model in that directory.
        input:
        - version: str, the version of the model to be saved
        - X_train: array-like, training data features
        - y_train: array-like, training data labels
        output:
        - None, the model is saved to a file    
        '''
        
        # Create a directory for the specific version of the model
        model_dir = os.path.join('models', version)
        # Create the directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        # Define the path for the model file    
        model_path = os.path.join(model_dir, f"{version}_Sentiment_Model.pkl")
        
        # Set up the Gaussian Naive Bayes classifier
        classifier = GaussianNB()
        # Fit the classifier to the training data
        classifier.fit(X_train, y_train)
        # Save the trained model to a file
        joblib.dump(classifier, model_path)
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Model version: {version}")
        
        y_pred = classifier.predict(X_test)
        logger.info(f"Predictions: {y_pred}")

        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"Confusion Matrix: {cm}")

        accuracy_score(y_test, y_pred)
        logger.info(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        return classifier
if __name__ == "__main__":
    # Example usage
    dataset_path = 'data/a1_RestaurantReviews_HistoricDump.tsv'  # Path to your dataset
    model_version = sys.argv[1]  # Version of the model, read from the tag of the git release
    
    # Initialize the SentimentModel class
    sentiment_model = SentimentModel(dataset_path)
    
    # Preprocess the data
    corpus = sentiment_model.preprocess_data()
    
    # Transform the data into a bag-of-words representation
    X, y = sentiment_model.transform_data(corpus)
    
    # Divide the data into training and testing sets
    X_train, X_test, y_train, y_test = sentiment_model.divide_data(X, y)
    
    # Fit the model and save it
    sentiment_model.fitting(model_version, X_train, X_test, y_train, y_test)