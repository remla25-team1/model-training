# Model Training

Repository for training a sentiment analysis model.

## Poetry for Dependency Management

This project uses **Poetry** to manage Python dependencies and virtual environments.

### Getting Started

#### 1. Install Poetry

If you don’t have Poetry installed yet, run the following command:

```bash
pipx install poetry
```

####  2. Install Dependencies

After installing Poetry, navigate to the project root directory (where the pyproject.toml file is located) and run:

```bash 
poetry install
```

This will create a virtual environment and install all required packages.

If you decide to add dependencies to ```pyproject.toml```, you need to update the ```poetry.lock``` file by running ```poetry lock```. Afterwards you can run ```poetry install``` again to install the updates packages.

#### 3. Activate the Virtual Environment (optional)

To activate the Poetry-managed virtual environment shell, run:
```bash 
eval $(poetry env activate)
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

To evaluate a model version named `v1.0.0`:

```bash 
poetry run python evaluate.py --version v1.0.0
```

#### 5. Exiting the Poetry Virtual Environment

To leave the Poetry virtual environment and return to your system’s default shell, simply run:
```bash
exit
```
or press `Ctrl+D`.

This will terminate the current virtual environment session and bring you back to your normal terminal environment.

## Running Model Training Pipeline

From the project root directory, execute the following scripts in order to run the full model training pipeline:

#### 1. Download and save the dataset

```bash 
python model_training/dataset.py
```

- This script downloads the raw dataset and stores it in the `data/raw/` folder.

#### 2. Preprocess the data

```bash 
python model_training/preprocessing.py
```

- Cleans the text data (e.g. lowercasing, removing punctuation, etc.) and saves the processed version to `data/processed/`.

#### 3. Extract features

```bash 
python model_training/features.py
```

- Converts the cleaned text into numerical features using Bag-of-Words, and prepares it for modeling.

#### 4. Train the model

```bash 
python model_training/modeling/train.py --version v0.0.3
```

- Trains the machine learning model, evaluates performance, and saves the trained model to the `models/` directory.
- The `--version` flag is used to tag the saved model with a specific version name (e.g., `v0.0.3`). This helps with tracking changes, reproducibility, and model deployment — especially when maintaining multiple versions over time.

#### 5. Evaluate the model

```bash 
python model_training/modeling/evaluate.py --version v0.0.3
```

- Evaluates the performance of a trained model corresponding to the specified version.
- The --version flag tells the script which model version to load from the `models/` directory for evaluation.
- The script outputs key metrics like accuracy and confusion matrix to help you understand how well the model performs on test data.

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
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
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
    │   └── train.py            <- Code to train models
    |models          
    │
    └── plots.py                <- Code to create visualizations
```

--------

