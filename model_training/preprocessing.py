from pathlib import Path
from loguru import logger
import typer
import pandas as pd
from lib_ml.preprocessing import Preprocessor

from model_training.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


def preprocess_data(dataset):
    '''
    Preprocesses the dataset using the Preprocessor class.
    input:
    - dataset: DataFrame, the raw dataset containing the text data and labels
    output:
    - corpus: list, the preprocessed text data
    '''
    preprocessor = Preprocessor()
    logger.info("Starting preprocessing...")
    corpus = preprocessor.process(dataset)
    logger.info("Preprocessing completed.")

    return corpus
    

@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
    output_path: Path = PROCESSED_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
):
    # Load raw data from file
    logger.info(f"Loading dataset from: {input_path}")
    dataset = pd.read_csv(input_path, delimiter="\t", quoting=3)

    # Preprocess data
    corpus = preprocess_data(dataset)
    processed_df = pd.DataFrame({
        "Review": corpus,
        "Liked": dataset["Liked"]
    })

    # Remove any rows with missing or empty reviews
    processed_df.dropna(subset=["Review"], inplace=True)
    processed_df = processed_df[processed_df["Review"].str.strip() != ""]

    # Save cleaned data
    processed_df.to_csv(output_path, sep="\t", index=False)
    logger.info(f"Saved preprocessed data to {output_path}")


if __name__ == "__main__":
    app()
