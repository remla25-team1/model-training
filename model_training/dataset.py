from pathlib import Path
from loguru import logger
import typer
import gdown

from model_training.config import RAW_DATA_DIR

app = typer.Typer()


def download_dataset(output_path):
    '''
    Download the sentiment analysis dataset from Google Drive.
    '''
    # Google Drive file ID
    file_id = "1_SHjQJVxZdr_LW2aIHAiOSBPWWGWd7Bs"

    url = f"https://drive.google.com/uc?id={file_id}"

    if not output_path.exists():
        logger.info(f"Downloading dataset to {output_path} from {url}...")
        gdown.download(url, str(output_path), quiet=False)
        logger.success(f"Download complete.")
    else:
        logger.info(f"File already exists at {output_path}, skipping download.")


@app.command()
def main(
    output_path: Path = RAW_DATA_DIR / "a1_RestaurantReviews_HistoricDump.tsv",
):
    download_dataset(output_path)


if __name__ == "__main__":
    app()
