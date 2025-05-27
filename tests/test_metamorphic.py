"""Metamorphic testing for sentiment analysis model robustness."""

import os
import pickle
import random
import sys

import nltk
import pandas as pd
import pytest
from nltk.corpus import wordnet
from sklearn.metrics import accuracy_score

nltk.download("wordnet")
nltk.download("omw-1.4")

# Skip all tests in this module if the metamorphic data file is missing
METAMORPHIC_DATA_PATH = "data/raw/metamorphic_data.tsv"
if not os.path.exists(METAMORPHIC_DATA_PATH):
    pytest.skip(
        f"Metamorphic data not found: {METAMORPHIC_DATA_PATH}", allow_module_level=True
    )


# metamorphic transformation functions
def get_synonym(word):
    """
    Get a random synonym for a given word using WordNet.

    If no synonym is found, return the original word.
    """
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
    """
    Replace each word in the text with a random synonym.

    If no synonym is found, the original word is kept.
    """
    words = text.split()
    return " ".join(get_synonym(w) for w in words)


def invert_negation(text):
    """
    Invert the negation in the text.

    If "not" is present, remove it; otherwise, add "not" after the first word.
    """
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
    """
    Shuffle the order of words in the text.

    If there are more than 3 words, shuffle the middle words. If there are 3 or fewer
    words, shuffle all words.
    """
    tokens = text.split()
    if len(tokens) > 3:
        middle = tokens[1:-1]
        random.shuffle(middle)
        tokens = [tokens[0]] + middle + [tokens[-1]]
    else:
        random.shuffle(tokens)
    return " ".join(tokens)


def add_irrelevant_info(text):
    """
    Add a neutral phrase to the text that does not change its sentiment.

    The phrase is chosen randomly from a predefined list of neutral phrases.
    """
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
    """
    Invert the label from "0" to "1" or from "1" to "0".

    This is used for transformations where the sentiment is expected to change.
    """
    return "1" if label == "0" else "0"


def generate_metamorphic_dataset(input_path, output_path):
    """
    Generate a metamorphic dataset by applying various metamorphic transformations to
    the input data.

    Args:
        input_path (str): Path to the input .tsv file containing two columns: "text" and "label".
        output_path (str): Path to the output .tsv file to write the transformed data.

    The function reads the input data, splits it into four subsets, and applies
    a different transformation to each subset:
        - MR1: Synonym Replacement (label unchanged)
        - MR2: Negation Inversion (label inverted)
        - MR3: Word Order Shuffling (label unchanged)
        - MR4: Add Irrelevant Information (label unchanged)

    The output .tsv file will have four columns:
        - original_text: The original input text.
        - original_label: The original label.
        - transformed_text: The text after metamorphic transformation.
        - transformed_label: The expected label after transformation.
    """
    # read .tsv input file
    df = pd.read_csv(input_path, sep="\t", names=["text", "label"])

    # shuffle and split into four subsets
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    subsets = [df_shuffled.iloc[i::4].reset_index(drop=True) for i in range(4)]

    # Apply different transformation to each subset
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
                # handle unexpected cases
                raise ValueError(f"Unexpected subset index: {i}")

            all_transformed.append((text, label, transformed, new_label))

    # Write to output file with 4 columns
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
    print("Metamorphic dataset written to metamorphic_data.tsv")


def load_model(path="sentiment_model.pkl"):
    """
    Load a pre-trained sentiment analysis model from a pickle file.

    Args:
        path (str): Path to the model file. Default is "sentiment_model.pkl".
    Returns:
        model: The loaded sentiment analysis model.
    """
    with open(path, "rb") as file:
        return pickle.load(file)


def predict(trained_model, texts):
    """
    Predict sentiment labels for a list of texts using the provided model.

    Args:
        trained_model: The pre-trained sentiment analysis model.
        texts (list): A list of text strings to predict.
    Returns:
        list: Predicted sentiment labels for the input texts.
    """
    return trained_model.predict(texts)


# metrics
def evaluate_model(trained_model, df):
    """
    Evaluate the metamorphic robustness of a sentiment analysis model on a given DataFrame.
    Args:
        trained_model: The pre-trained sentiment analysis model.
        df (DataFrame): A DataFrame containing the original and transformed texts and labels.
            It should have the following columns:
            - original_text: The original text.
            - original_label: The original label.
            - transformed_text: The text after metamorphic transformation.
            - transformed_label: The expected label after transformation.
    Returns:
        DataFrame: The input DataFrame with additional columns
        for predictions and evaluation metrics.
    """
    pred_orig = predict(trained_model, df["original_text"])
    pred_trans = predict(trained_model, df["transformed_text"])

    df["pred_original"] = pred_orig
    df["pred_transformed"] = pred_trans

    # Consistency Rate
    consistency = (df["pred_original"] == df["pred_transformed"]).mean()

    # Label Preservation Rate (MRs where label shouldn't change)
    same_label_mask = df["original_label"] == df["transformed_label"]
    label_preservation = (
        (df["pred_transformed"] == df["original_label"])[same_label_mask].mean()
        if same_label_mask.any()
        else None
    )

    # Flipping Rate (MRs where label is expected to change)
    flipped_mask = df["original_label"] != df["transformed_label"]
    flipping_rate = (
        (df["pred_transformed"] != df["pred_original"])[flipped_mask].mean()
        if flipped_mask.any()
        else None
    )

    # Accuracy Drop
    acc_orig = accuracy_score(df["original_label"], df["pred_original"])
    acc_trans = accuracy_score(df["transformed_label"], df["pred_transformed"])
    delta_acc = acc_orig - acc_trans

    print("Metamorphic Robustness Evaluation:")
    print(f"Consistency Rate:       {consistency:.3f}")
    if label_preservation is not None:
        print(f"Label Preservation Rate: {label_preservation:.3f}")
    if flipping_rate is not None:
        print(f"Flipping Rate:           {flipping_rate:.3f}")
    print(f"Accuracy Drop (delta acc):    {delta_acc:.3f}")

    return df


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_metamorphic.py <input_data.tsv> <model.pkl>")
    else:
        data_path = sys.argv[1]
        model_path = sys.argv[2]

        data_base_dir = os.path.dirname(os.path.abspath(data_path)) or "."

        metamorphic_data_path = os.path.join(data_base_dir, "metamorphic_data.tsv")

        generate_metamorphic_dataset(data_path, metamorphic_data_path)

        metamorphic_df = pd.read_csv(metamorphic_data_path, sep="\t")

        loaded_model = load_model(model_path)

        results_df = evaluate_model(loaded_model, metamorphic_df)

        results_df.to_csv(
            os.path.join(data_base_dir, "metamorphic_predictions.tsv"),
            sep="\t",
            index=False,
        )
