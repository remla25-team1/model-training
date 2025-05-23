# Model Training

Sentiment analysis model.

## Poetry for Dependency Management

This project uses **Poetry** to manage Python dependencies and virtual environments. Poetry simplifies package management and ensures consistent environments across different machines.

### Getting Started

#### 1. Install Poetry

If you don’t have Poetry installed yet, run the following command:

```bash
pip install poetry
```

####  2. Install Dependencies

After installing Poetry, navigate to the project root directory (where the pyproject.toml file is located) and run:

```bash 
poetry install
```

This will create a virtual environment and install all required packages.

#### 3. Activate the Virtual Environment (optional)

To activate the Poetry-managed virtual environment shell, run:
```bash 
poetry shell
```

Any Python commands you run inside this shell will use the installed dependencies.

#### 4. Running the Code

You can run your Python scripts in two ways:

- **Inside the Poetry shell:**

```bash 
python path/to/your_script.py [options]
```

- **Directly, without activating the shell, by prefixing with poetry run:**

```bash 
poetry run python path/to/your_script.py [options]
```

**Example:**

To evaluate a model version named v1.0.0:

```bash 
poetry run python evaluate.py --version v1.0.0
```

## Automatic Versioning

### To trigger the automated version release:
1) Go to repo model-training on GitHub.
2) Click on the "Actions" tab.
3) Select "Automated Pre-Release Versioning" from the list on the left (the name from name: Automated Pre-Release Versioning).
4) Click the “Run workflow” button.

### To do version bump:
1) Update VERSION.txt to new base version.
2) Commit and push it.
3) Run above steps to trigger automated version release.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         model-training and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── model_training   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes model_training a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   └── evaluate.py         <- Code to evaluate trained model
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

