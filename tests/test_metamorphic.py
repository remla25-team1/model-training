import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
import os
import numpy as np
import sys
import pickle
from sklearn.metrics import accuracy_score

nltk.download("wordnet")
nltk.download("omw-1.4")

# metamorphic transformation functions
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


def generate_metamorphic_dataset(input_path, output_path):
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

            all_transformed.append((text, label, transformed, new_label))

    # Write to output file with 4 columns
    transformed_df = pd.DataFrame(
        all_transformed,
        columns=["original_text", "original_label", "transformed_text", "transformed_label"]
    )

    transformed_df.to_csv(output_path, sep="\t", index=False)
    print("Metamorphic dataset written to metamorphic_data.tsv")


def load_model(path="sentiment_model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def predict(model, texts):
    return model.predict(texts)

# metrics
def evaluate_model(model, df):
    pred_orig = predict(model, df["original_text"])
    pred_trans = predict(model, df["transformed_text"])

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

        model = load_model(model_path)

        results_df = evaluate_model(model, metamorphic_df)

        results_df.to_csv(os.path.join(data_base_dir, "metamorphic_predictions.tsv"), sep="\t", index=False)
