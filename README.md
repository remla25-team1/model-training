# REMLA-25, Team 1, Model Training
![coverage](https://img.shields.io/badge/coverage-44%25-red) ![pylint](https://img.shields.io/badge/pylint-0.0%2F10-red)
9.91%2F10-red)
9%2E91%2F10-red)

Repository for training a sentiment analysis model.

## Table of Contents
- [Project Organization](#project-organization)
- [Getting Started](#getting-started)
- [Set up dvc remote](#set-up-dvc-remote)
- [Running Model Training Pipeline](#running-model-training-pipeline)
- [1. Download and save the dataset](#1-download-and-save-the-dataset)
- [2. Preprocess the data](#2-preprocess-the-data)
- [3. Extract features](#3-extract-features)
- [4. Train the model](#4-train-the-model)
- [5. Evaluate the model](#5-evaluate-the-model)
- [Automatic Versioning](#automatic-versioning)
- [To trigger the automated version release](#to-trigger-the-automated-version-release)
- [ML auto testing](#ml-auto-testing)
    - [Coverage](#coverage)
    - [Test Metrics Summary](#test-metrics-summary)

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
    ├── evaluate.py             <- Code to evaluate trained model
    │
    ├── train.py                <- Code to train models        
    │
    └── plots.py                <- Code to create visualizations
```

--------

## Getting Started

This project uses **Poetry** to manage Python dependencies and virtual environments.

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

## Set up dvc remote
**1) Activate the Virtual Environment**

To activate the venv you can execute the command from the Poetry setup (step 3).

**2) Get Credentials** 

Log into the gdrive of remla25.team1@gmail.com to see the credential json file (remla-dvc-remote-g1-2591d1204b80) of the service account. 

**3) Move credentials** 

Move it into .dvc/tmp of this repository, if the tmp map doesn't exist yet create it. This will not be saved into github, because it is part of the .gitignore.

**4) Pull DVC** 

Run 
```bash
dvc pull -r myremote
```
This should pull all the files stored in the gdrive for DVC.

**5) Troubleshooting** 

If it didn't pull because the remote was not included in the dvc/config file, make the remote again
```bash
dvc remote add myremote gdrive://1R5ndxon7Ej5SDUo0pt9xJ_qCEGc5pE6u
dvc remote default myremote
```
Again, this should have been done already so it shouldn't be necessary to create it again.

**6) Push to DVC** 

To push the changes you made, run 
```
dvc repro
git commit -am "Your message"
git push
dvc push -r myremote
```


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
python model_training/train.py --version=v0.0.1
```

- Trains the machine learning model, evaluates performance, and saves the trained model to the `models/` directory.
- version is the version you want to train. In release.yml this is automated to latest tag.

#### 5. Evaluate the model

```bash 
python model_training/evaluate.py --version v0.0.3
```

- Evaluates the performance of a trained model corresponding to the specified version.
- The --version flag tells the script which model version to load from the `models/` directory for evaluation.
- The script outputs key metrics like accuracy and confusion matrix to help you understand how well the model performs on test data.

## Automatic Versioning
We have two types of tags: vX.X.X or vX.X.X-pre-DATE-XXX. The first version is used for production. These will always be versions that work. The latter tag is an experimental model for developing purposes, this doesn't always have to be a working version. The version bump is now done automatically, so if v0.0.1 already exists, it will automatically bump the VERSION.txt up one count. Same story for the experimental tags, they will be based on the VERSION.txt as a base and increment based on date and based on last three digits if there are multiple models on the same day.

### To trigger the automated version release:
1) Go to repo model-training on GitHub.
2) Click on the "Actions" tab.
3) Select "Versioning Workflow (SemVer + Dated Pre-Releases) " from the list on the left.
4) Click the “Run workflow” button.
5) When this workflow has finished, go to Release model-training from the list on the left
6) You will now see that this workflow has been triggered automatically by the previous workflow.

## ML auto testing
### Test Metrics Summary
#### Summary of Coverage 
<!-- COVERAGE_SUMMARY_START -->

| File | Statements | Miss | Coverage | Missing Lines |
|------|------------|------|----------|----------------|
| model_training/config.py | 18 | 2 | 89% |              18      2    89%   31-32 |
| model_training/ensure_versioning.py | 25 | 19 | 24% |   25     19    24%   13-28, 32-42, 46-47 |
| model_training/train.py | 38 | 24 | 37% |               38     24    37%   31-60, 64 |
| ------------------------------------------------------------------- |  |  |  | ------------------------------------------------------------------- |
<!-- COVERAGE_SUMMARY_END -->
<!-- METRICS START -->

#### DATA_AND_FEATURES

| Metric | Value | Notes |
|--------|-------|---------|
| DATA_QUALITY | pass | Checked: NULL_CHECKS, EMPTY_STRING_CHECK, BINARY_LABEL_CHECK |
| FEATURE_SPARSITY | 0.9962 | Zero ratio: 0.9962 |
| PREPROCESSING_LATENCY | 0.0 | Avg. time per review (on 100 samples) |

#### MODEL_DEVELOPMENT

| Metric | Value | Notes |
|--------|-------|---------|
| MODEL_ACCURACY | 0.672 | Accuracy on test set |
| ACCURACY_POSITIVE | 1.0 | Accuracy on positive samples |
| ACCURACY_NEGATIVE | 1.0 | Accuracy on negative samples |
| PREDICTION_DETERMINISTIC | True | Predictions are consistent across repeated inference |
| VECTORIZATION_MEMORY_USAGE | 0.441 | Peak memory usage during vectorization (MB) |

#### INFRASTRUCTURE_TESTING

| Metric | Value | Notes |
|--------|-------|---------|
| MODEL_FILE_EXISTS | True | Model file found |
| MODEL_LOADABLE | True | Model loaded and is GaussianNB |

#### MONITORING_TESTING

| Metric | Value | Notes |
|--------|-------|---------|
| FRESH_PREDICTION_SHAPE_OK | True | Prediction output shape matches input size |
| FRESH_POSITIVE_RATIO | 0.42 | Prediction distribution is suspicious if not between 0.2 and 0.8 |

<!-- METRICS END -->
