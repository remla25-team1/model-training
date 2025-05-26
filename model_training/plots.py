"""Plot generation utilities for the model training package."""

from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from model_training.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    _input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    _output_path: Path = FIGURES_DIR / "plot.png",
):
    """CLI entry point for generating plots from data."""
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")


if __name__ == "__main__":
    app()
