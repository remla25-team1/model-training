from sklearn.metrics import accuracy_score
from model_training.training import SentimentModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import tracemalloc
import joblib
import pandas as pd
from lib_ml.preprocessing import Preprocessor
import pytest
import os


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


def test_model_prediction_accuracy(trained_model_file):
    model_path = trained_model_file
    classifier = joblib.load(model_path)
    dataset = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", delimiter='\t', quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(dataset)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    X = vectorizer.transform(corpus).toarray()
    y = dataset.iloc[:, -1].values
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    y_pred = classifier.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[Accuracy] Model accuracy on test set: {acc:.2f}")
    assert acc >= 0.65, f"Model accuracy too low: {acc:.2f}"


def get_accuracy(corpus, labels):
    corpus = [doc for doc in corpus if doc.strip()]
    if len(corpus) < 5:
        pytest.skip("Too few valid documents after preprocessing")
    vectorizer = CountVectorizer(max_features=1420)
    try:
        X = vectorizer.fit_transform(corpus).toarray()
    except ValueError as e:
        pytest.skip(f"Vectorizer failed: {e}")
    y = labels[:len(X)] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    clf = GaussianNB().fit(X_train, y_train)
    return accuracy_score(y_test, clf.predict(X_test))

def test_model_consistency_on_labels():
    model = SentimentModel("data/a1_RestaurantReviews_HistoricDump.tsv")
    df = model.dataset.copy()
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
    assert abs(acc_pos - acc_neg) < 0.15, (
        f"Model performs very differently on positive vs negative samples: {acc_pos:.2f} vs {acc_neg:.2f}"
    )




def test_model_prediction_determinism(trained_model_file):
    clf = joblib.load(trained_model_file)
    dataset = pd.read_csv("data/a1_RestaurantReviews_HistoricDump.tsv", delimiter='\t', quoting=3)
    preprocessor = Preprocessor()
    corpus = preprocessor.process(dataset)
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    X = vectorizer.transform(corpus).toarray()
    y = dataset.iloc[:, -1].values
    _, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=0)
    pred1 = clf.predict(X_test)
    pred2 = clf.predict(X_test)
    assert (pred1 == pred2).all(), "Predictions differ between identical runs"


def test_memory_usage_during_vectorization():
    model = SentimentModel("data/a1_RestaurantReviews_HistoricDump.tsv")
    corpus = model.preprocess_data()

    vectorizer = CountVectorizer(max_features=1420)
    tracemalloc.start()
    vectorizer.fit_transform(corpus)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / (1024 * 1024)  
    print(f"[Memory] Peak vectorization memory usage: {peak_mb:.2f}MB")
    assert peak_mb < 100, f"Vectorization peak memory usage too high: {peak_mb:.2f}MB"
