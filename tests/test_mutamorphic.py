"""Mutamorphic testing for sentiment analysis model robustness."""

import argparse
import os
import random
import sys

import joblib
import nltk
import pandas as pd
from lib_ml.preprocessing import Preprocessor
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score

from model_training.config import MODELS_DIR
from utils.log_metrics import log_metric

# Download required NLTK data
nltk.download("wordnet")
nltk.download("omw-1.4")

# Mutamorphic data file path (will be generated)
MUTAMORPHIC_DATA_FILENAME = "mutamorphic_data.tsv"

# Preprocessor and vectorizer globals (will initialize later)
preprocessor = Preprocessor()
vectorizer = CountVectorizer(max_features=1420)

category = "MUTAMORPHIC_TESTING"

# ---------------- Mutamorphic Transformations ----------------


def get_synonym(word):
    synsets = wordnet.synsets(word)
    if synsets:
        lemmas = synsets[0].lemmas()
        synonyms = [
            lemma.name().replace("_", " ")
            for lemma in lemmas
            if lemma.name().lower() != word.lower()
        ]
        if synonyms:
            return random.choice(synonyms)
    return word


def replace_synonyms(text):
    words = text.split()
    return " ".join(get_synonym(w) for w in words)


def invert_negation(text):
    tokens = text.split()
    if "not" in tokens:
        tokens = [t for t in tokens if t.lower() != "not"]
    else:
        if len(tokens) > 1:
            tokens.insert(1, "not")
        else:
            tokens.insert(0, "not")
    return " ".join(tokens)


def shuffle_word_order(text):
    tokens = text.split()
    if len(tokens) > 3:
        middle = tokens[1:-1]
        random.shuffle(middle)
        tokens = [tokens[0]] + middle + [tokens[-1]]
    else:
        random.shuffle(tokens)
    return " ".join(tokens)


def add_irrelevant_info(text):
    random.seed(42)
    neutral_phrases = [
        "I had cereal today.",
        "It's a sunny day.",
        "The sky is blue.",
        "I walked my dog this morning.",
        "I like coffee.",
        "Water boils at 100 degrees Celsius.",
        "The train arrived on time.",
        "I charged my phone last night.",
        "She went to the grocery store.",
        "It's currently Tuesday.",
        "He wore a blue shirt.",
        "There are 24 hours in a day.",
        "My laptop is on the desk.",
        "Birds can fly.",
        "The light turned green.",
        "They are watching a documentary.",
        "The book is on the shelf.",
        "I took the bus to work.",
        "It rained last night.",
        "The meeting starts at 10 a.m.",
    ]
    return f"{text} {random.choice(neutral_phrases)}"


def invert_label(label):
    return "1" if label == "0" else "0"


def generate_mutamorphic_dataset(input_path, output_path):
    df = pd.read_csv(input_path, sep="\t", names=["text", "label"])

    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    subsets = [df_shuffled.iloc[i::4].reset_index(drop=True) for i in range(4)]

    all_transformed = []

    for i, subset in enumerate(subsets):
        for _, row in subset.iterrows():
            text, label = row["text"], row["label"]

            if i == 0:  # MR1: Synonym Replacement
                transformed = replace_synonyms(text)
                new_label = label
            elif i == 1:  # MR2: Negation Inversion
                transformed = invert_negation(text)
                new_label = invert_label(label)
            elif i == 2:  # MR3: Word Order Shuffling
                transformed = shuffle_word_order(text)
                new_label = label
            elif i == 3:  # MR4: Add Irrelevant Information
                transformed = add_irrelevant_info(text)
                new_label = label
            else:
                raise ValueError(f"Unexpected subset index: {i}")

            all_transformed.append((text, label, transformed, new_label))

    transformed_df = pd.DataFrame(
        all_transformed,
        columns=[
            "original_text",
            "original_label",
            "transformed_text",
            "transformed_label",
        ],
    )

    transformed_df.to_csv(output_path, sep="\t", index=False)
    print(f"Mutamorphic dataset written to {output_path}")


# ---------------- Model Loading & Prediction ----------------


def load_model(version):
    path = MODELS_DIR / version / f"{version}_Sentiment_Model.pkl"
    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}")
    print(f"Loading model from {path}")
    return joblib.load(path)


def fit_vectorizer_on_training_data(train_texts):
    processed = [preprocessor.process_item(t) for t in train_texts]
    vectorizer.fit(processed)
    print(f"Fitted vectorizer on {len(train_texts)} training samples")


def predict(model, texts):
    processed = [preprocessor.process_item(t) for t in texts]
    x = vectorizer.transform(processed)
    return model.predict(x.toarray())


# ---------------- Evaluation ----------------


def evaluate_model(trained_model, df):
    pred_orig = predict(trained_model, df["original_text"])
    pred_trans = predict(trained_model, df["transformed_text"])

    df["pred_original"] = pred_orig
    df["pred_transformed"] = pred_trans

    consistency = (df["pred_original"] == df["pred_transformed"]).mean()

    same_label_mask = df["original_label"] == df["transformed_label"]
    label_preservation = (
        (df["pred_transformed"] == df["original_label"])[same_label_mask].mean()
        if same_label_mask.any()
        else None
    )

    flipped_mask = df["original_label"] != df["transformed_label"]
    flipping_rate = (
        (df["pred_transformed"] != df["pred_original"])[flipped_mask].mean()
        if flipped_mask.any()
        else None
    )

    acc_orig = accuracy_score(df["original_label"], df["pred_original"])
    acc_trans = accuracy_score(df["transformed_label"], df["pred_transformed"])
    delta_acc = acc_orig - acc_trans

    log_metric("CONSISTENCY_RATE", consistency, message="Same predictions before and after transformation", category=category)
    if label_preservation is not None:
        print(f"Consistency Rate:       {consistency:.3f}")
        log_metric("LABEL_PRESERVATION_RATE", label_preservation, message="Labels preserved where they should be", category=category)
    if label_preservation is not None:
        print(f"Label Preservation Rate: {label_preservation:.3f}")
    if flipping_rate is not None:
        print(f"Flipping Rate:           {flipping_rate:.3f}")
        log_metric("FLIPPING_RATE", flipping_rate, message="Predictions flipped where they should flip", category=category)
    print(f"Accuracy Drop (delta acc):    {delta_acc:.3f}")
    log_metric("ACCURACY_DROP", delta_acc, message="Accuracy drop after mutamorphic transformation", category=category)


    return df


# ---------------- Main ----------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mutamorphic Testing for Sentiment Analysis"
    )
    parser.add_argument(
        "--input", required=True, help="Input .tsv data file with text and label"
    )
    parser.add_argument(
        "--model-version", default="test_model_dev", help="Model version to load"
    )
    args = parser.parse_args()

    input_path = args.input
    base_dir = os.path.dirname(os.path.abspath(input_path)) or "."
    mutamorphic_path = os.path.join(base_dir, MUTAMORPHIC_DATA_FILENAME)

    if not os.path.exists(input_path):
        print(f"Input data file not found: {input_path}")
        sys.exit(1)

    # Generate mutamorphic dataset
    generate_mutamorphic_dataset(input_path, mutamorphic_path)

    # Load mutamorphic data
    mutamorphic_df = pd.read_csv(mutamorphic_path, sep="\t")

    # Load model
    model = load_model(args.model_version)

    # Fit vectorizer on original training texts (assumes input file is training data)
    train_df = pd.read_csv(input_path, sep="\t", names=["text", "label"])
    fit_vectorizer_on_training_data(train_df["text"])

    # Evaluate mutamorphic robustness
    results_df = evaluate_model(model, mutamorphic_df)

    # Save predictions
    output_dir = os.path.join("tests", "results")
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists, otherwise create it
    output_predictions_path = os.path.join(output_dir, "mutamorphic_predictions.tsv")
    results_df.to_csv(output_predictions_path, sep="\t", index=False)
    print(f"Predictions saved to {output_predictions_path}")
