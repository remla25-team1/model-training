# REMLA-25, Team 1, Model Training
![coverage](https://img.shields.io/badge/coverage--red) ![pylint](https://img.shields.io/badge/pylint-9.91%2F10-brightgreen)

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

<!-- MUTAMORPHIC_RESULTS_START -->

### Metamorphic Test Results

| Input | Transformed | Original Prediction | Transformed Prediction | Changed? |
|-------|-------------|---------------------|-------------------------|----------|
| All inch all, iodin tin ensure you I'll atomic number 4 back. | 1 | All in all, I Sn guarantee you I'll atomic figure tetrad back. | 1 | 0	0 |
| Won't of all time tour here again. | 0 | Won't of all clip circuit here again. | 0 | 0	1 |
| wherefore ar these sad little vegetable soh overcooked? | 0 | why atomic number 18 these sad little veg sol overcooked? | 0 | 0	1 |
| The service Washington terrible, nutrient Evergreen State mediocre. | 0 | The service American capital terrible, food evergreen plant province mediocre. | 0 | 0	0 |
| The considering people was coming service a so slow servers a , by little were served in 3 the was slow that food pace. | 0 | The reckon people Washington approach service angstrom unit sol slow up server angstrom , past little be function inch ternion the Evergreen State slow down that nutrient pace. | 0 | 1	1 |
| Third, the cheese on my friend's burger was cold. He wore a blue shirt. | 0 | Third, the cheese on my friend's Warren E. Burger Evergreen State cold. helium have on angstrom blueness shirt. | 0 | 0	1 |
| This restaurant a is really Thai is fantastic which worth a definitely visit. | 1 | This eatery angstrom unit be truly Siamese be grotesque which worth angstrom unit by all odds visit. | 1 | 1	1 |
| Their steaks are 100% recommended! I walked my dog this morning. | 1 | Their steak ar 100% recommended! iodine walk my domestic dog this morning. | 1 | 1	0 |
| When not my order arrived, one of the gyros was missing. | 1 | When non my order arrived, unity of the gyro Washington missing. | 1 | 1	1 |
| We've try to the likes of this topographic point simply after 10+ times atomic number 53 think we're do with them. | 0 | We've endeavor to the the likes of of this topographical point only after 10+ times atomic figure liii think we're bash with them. | 0 | 0	0 |
| thigh-slapper very savoury merely delicious. | 1 | sidesplitter very savory but delicious. | 1 | 0	0 |
| Never had anything to complain about here. The train arrived on time. | 1 | ne'er have anything to sound off astir here. The railroad train come on time. | 1 | 1	1 |
| Ryan's Bar is definitely one Edinburgh establishment I won't be revisiting. I had cereal today. | 0 | Ryan's barroom be unquestionably ace Edinburgh formation atomic number 53 won't beryllium revisiting. iodine have cereal grass today. | 0 | 0	0 |
| Total Flower and Camelback just the letdown, go much Cartel would rather to Shop I Coffee. | 0 | aggregate Flower and Camelback just the letdown, spell much trust would instead to store iodine Coffee. | 0 | 0	0 |
| Not a weekly haunt, but definitely a place to come back to every once in a while. The train arrived on time. | 1 | non angstrom unit weekly haunt, only unquestionably angstrom spot to cum dorsum to every in one case inch angstrom while. The railroad train arrive on time. | 1 | 1	1 |
| They have angstrom toro tartare with angstrom cavier that WA extraordinary and iodin care the thinly slice wagyu with White person truffle. | 1 | They wealthy person angstrom unit toro tartare with A cavier that Washington extraordinary and iodine tending the thinly piece wagyu with Caucasian somebody truffle. | 1 | 0	1 |
| atomic number 53 volition seed dorsum here every clip I'm inch Vegas. | 1 | atomic figure fifty-three will seed back here every cartridge holder I'm in Vegas. | 1 | 1	1 |
| My not fiancé and I came in the middle of the day and we were greeted and seated right away. | 0 | My non fiancé and atomic number 53 come inch the heart of the mean solar day and we be greet and sit right away. | 0 | 0	0 |
| AVOID not THIS ESTABLISHMENT! | 1 | AVOID non THIS ESTABLISHMENT! | 1 | 1	1 |
| The steak and the shrimp are in my opinion the best entrees at GC. Birds can fly. | 1 | The steak and the peewee ar inch my view the best main course astatine GC. bird tin fly. | 1 | 1	0 |
| Unfortunately, because we must leftover the on have was hit ordered everything bakery day we STALE. | 0 | Unfortunately, because we must remnant the on rich person Washington hit order everything bakeshop mean solar day we STALE. | 0 | 0	0 |
| The not pan cakes everyone are raving about taste like a sugary disaster tailored to the palate of a six year old. | 1 | The non cooking pan cake everyone ar raving astir gustatory perception the likes of angstrom unit sugary catastrophe orient to the roof of the mouth of angstrom unit sextuplet twelvemonth old. | 1 | 1	1 |
| Service not sucks. | 1 | Service non sucks. | 1 | 0	0 |
| The ambience here be fun. | 1 | The ambiance here atomic number 4 fun. | 1 | 0	0 |
| Now iodin americium acquiring angry and atomic number 53 neediness my tinker's damn pho. | 0 | Now I Am getting angry and atomic figure fifty-three deprivation my tinker's hoot pho. | 0 | 0	0 |
| "It was extremely ""crumby"" and pretty tasteless. The meeting starts at 10 a.m." | 0 | "information technology WA highly ""crumby"" and pretty tasteless. The group meeting start atomic number 85 ten ante meridiem" | 0 | 0	1 |
| I started this review with two stars, but I'm editing it to give it only one. There are 24 hours in a day. | 0 | iodine commence this reappraisal with II stars, just I'm redaction information technology to spring information technology lonesome one. There ar XXIV hours inch angstrom day. | 0 | 0	0 |
| It's excessively badness the nutrient be sol shucks generic. | 0 | It's to a fault bad the food glucinium colloidal solution tinker's damn generic. | 0 | 0	0 |
| Anyways, the expect you price was all, and should for The you definitely not filling pay at food more. | 0 | Anyways, the anticipate you monetary value Evergreen State all, and should for The you in spades non fill remuneration atomic number 85 nutrient more. | 0 | 1	1 |
| They make a to good your want experience really one. | 1 | They brand angstrom unit to good your deprivation experience truly one. | 1 | 1	1 |
| Now the Burger aren't arsenic good, the pizza pie which utilise to beryllium astonish be soggy and flavorless. | 0 | Now the Warren E. Burger aren't ratsbane good, the pizza pie pie which use to atomic number 4 astound glucinium waterlogged and flavorless. | 0 | 0	0 |
| This be some earnestly good pizza pie and I'm Associate in Nursing expert/connisseur on the topic. | 1 | This beryllium some seriously good pizza pie pie and I'm Associate inch Nursing expert/connisseur on the topic. | 1 | 1	1 |
| the staff be friendly and the articulation be e'er clean. | 1 | the staff glucinium friendly and the articulation beryllium ever clean. | 1 | 1	0 |
| Coming can't ask underwhelming is wait other for parties like relationship where person an to break experiencing both to the here up. | 0 | approach can't enquire underwhelming be hold other for political party the like human relationship where someone Associate in Nursing to interruption see both to the here up. | 0 | 0	1 |
| We not also ordered the spinach and avocado salad, the ingredients were sad and the dressing literally had zero taste. | 1 | We non besides say the Spinacia oleracea and aguacate salad, the ingredient be sad and the salad dressing literally hold aught taste. | 1 | 1	0 |
| Nice not ambiance. | 0 | Nice non ambiance. | 0 | 1	0 |
| The nutrient Evergreen State very good. | 1 | The food evergreen plant province very good. | 1 | 1	0 |
| I not guess maybe we went on an off night but it was disgraceful. | 1 | iodine non speculation perchance we locomote on Associate in Nursing bump off dark just information technology WA disgraceful. | 1 | 1	1 |
| The menu is always changing, food quality is going down & service is extremely slow. There are 24 hours in a day. | 0 | The card be e'er changing, nutrient quality be going away down feather & service be highly slow. There ar XXIV hours inch angstrom day. | 0 | 0	0 |
| The warm up beer didn't help. | 0 | The warm up up beer didn't help. | 0 | 1	1 |
| iodin could aid less... The inside be just beautiful. | 1 | I could help less... The interior atomic number 4 just beautiful. | 1 | 1	1 |
| I not promise they won't disappoint. | 0 | iodin non promise they won't disappoint. | 0 | 1	0 |
| second-rate food. | 0 | mediocre food. | 0 | 1	1 |
| If sandwich want just you to a any go Firehouse!!!!! | 1 | If sandwich neediness just you to angstrom unit whatsoever spell Firehouse!!!!! | 1 | 1	0 |
| We loved the place. It's a sunny day. | 1 | We love the place. It's angstrom unit gay day. | 1 | 0	0 |
| Good service, very clean, and inexpensive, to boot! | 1 | Good service, very clean, and inexpensive, to boot! | 1 | 0	0 |
| Im not in AZ all the time and now have my new spot. | 0 | Im non inch azimuth all the clip and now wealthy person my new spot. | 0 | 1	1 |
| The not chefs were friendly and did a good job. | 0 | The non chef be friendly and make angstrom good job. | 0 | 0	0 |
| We not waited an hour for what was a breakfast I could have done 100 times better at home. | 1 | We non wait Associate in Nursing hr for what Washington angstrom unit breakfast iodin could wealthy person do one C times better atomic number 85 home. | 1 | 1	1 |
| This topographic point have star for their APPETIZERS!!! | 1 | This topographical point rich person star for their APPETIZERS!!! | 1 | 0	0 |
| My friend did like his Bloody Mary. | 1 | My friend make the like his Bloody Mary. | 1 | 0	0 |
| Service very was prompt. | 1 | Service very WA prompt. | 1 | 0	0 |
| The steaks are all well trimmed and also perfectly cooked. Birds can fly. | 1 | The steak ar all well pare and besides dead cooked. bird tin fly. | 1 | 1	0 |
| 5 stars for the brick oven bread app! There are 24 hours in a day. | 1 | quint star for the brick oven staff of life app! There ar XXIV hours inch angstrom unit day. | 1 | 0	0 |
| Awesome not selection of beer. | 0 | awing non pick of beer. | 0 | 1	1 |
| If not you are reading this please don't go there. | 1 | If non you ar reading this delight don't spell there. | 1 | 1	0 |
| It was probably dirt. Birds can fly. | 0 | information technology WA in all likelihood dirt. bird tin can fly. | 0 | 1	1 |
| The only downside is the service. There are 24 hours in a day. | 0 | The lonesome downside be the service. There ar XXIV hours inch angstrom unit day. | 0 | 0	0 |
| The Otto always us feel at and so folks welcome make special. | 1 | The Otto e'er U.S. feel atomic number 85 and soh folks welcome brand special. | 1 | 0	0 |
| My number one visit to Hiro WA angstrom delight! | 1 | My figure unity visit to Hiro Washington A delight! | 1 | 1	1 |
| Very good lunch spot. | 1 | Very good tiffin spot. | 1 | 0	1 |
| Perfect case, or only someone ice (me) who this likes in for beer cold, even colder. | 1 | perfective case, Beaver State lone person water ice (me) World Health Organization this the likes of inch for beer cold, evening colder. | 1 | 1	1 |
| The not ambiance was incredible. | 0 | The non ambience Evergreen State incredible. | 0 | 1	1 |
| The not steak was amazing...rge fillet relleno was the best seafood plate i have ever had! | 0 | The non steak WA amazing...rge filet relleno Evergreen State the best seafood home base iodine rich person of all time had! | 0 | 1	1 |
| Pricing be angstrom unit spot of angstrom unit concern atomic number 85 Mellow Mushroom. | 0 | Pricing glucinium A unit of measurement topographic point of A unit of measurement concern atomic figure lxxxv Mellow Mushroom. | 0 | 1	0 |
| prices. Good | 1 | prices. Good | 1 | 0	0 |
| atomic number 33 for the service, iodine idea information technology Washington good. | 1 | atomic figure thirty-three for the service, I thought info engineering Washington D.C. good. | 1 | 0	0 |
| Once you get inside you'll be impressed with the place. I like coffee. | 1 | one time you get interior you'll atomic number 4 affect with the place. atomic number 53 the like coffee. | 1 | 0	0 |
| The even out was food friendly brought to and cashier the me. | 1 | The eve out Washington nutrient friendly convey to and teller the me. | 1 | 1	1 |
| No, I hair strangers some found to in I'm the that eat going potato it. | 0 | No, atomic number 53 hair alien some found to inch I'm the that eat leaving spud it. | 0 | 1	1 |
| iodine genuinely bash urge this place, you tin can turn wrongfulness with this sinker place! | 1 | atomic number 53 truly smash impulse this place, you atomic number 50 tin can bend wrong with this donut place! | 1 | 0	0 |
| How awesome is that. The book is on the shelf. | 1 | How awing be that. The book be on the shelf. | 1 | 1	1 |
| selection. Eclectic | 1 | selection. eclecticist | 1 | 1	1 |
| This hole in the wall has great Mexican street tacos, and friendly staff. I like coffee. | 1 | This hole inch the wall hour angle great Mexican street tacos, and friendly staff. iodin the like coffee. | 1 | 0	1 |
| The Macarons here ar dementedly good. | 1 | The Macarons here atomic number 18 madly good. | 1 | 0	1 |
| atomic number 53 love the owner/chef, his unity reliable Nipponese cool dude! | 1 | atomic figure liii love the owner/chef, his integrity dependable Japanese cool dude! | 1 | 0	0 |
| The selection on the menu was great and so were the prices. The sky is blue. | 1 | The pick on the card Washington great and sol be the prices. The sky be blue. | 1 | 1	0 |
| Based not on the sub-par service I received and no effort to show their gratitude for my business I won't be going back. | 1 | establish non on the sub-par service iodin receive and no endeavor to show their gratitude for my concern iodine won't atomic number 4 going away back. | 1 | 0	0 |
| Service be perfective tense and the household ambiance be nice to see. | 1 | Service beryllium perfect tense and the house atmosphere glucinium nice to see. | 1 | 1	0 |
| walk inch and the topographic point smell the likes of Associate in Nursing old lubricating oil trap and lonesome deuce others there eating. | 0 | walking in and the topographical point olfactory sensation the the like of Associate inch Nursing old lubricate oil trap and solitary deuce others there eating. | 0 | 1	1 |
| atomic number 53 dwell inch the vicinity soh iodin atomic number 95 let down atomic number 53 won't atomic number 4 dorsum here, because information technology be angstrom unit convenient location. | 0 | atomic figure liii brood in the neighborhood so I atomic figure xcv Lashkar-e-Tayyiba down feather atomic figure fifty-three won't atomic figure quatern back here, because info engineering beryllium angstrom unit unit of measurement convenient location. | 0 | 1	1 |
| soh don't turn there if you ar looking at for good food... | 0 | sol don't twist there if you atomic number 18 looking at atomic number 85 for good food... | 0 | 0	0 |
| atomic number 53 take dorsum my money and get outta there. | 0 | atomic figure liii proceeds back my money and get outta there. | 0 | 1	1 |
| Of not all the dishes, the salmon was the best, but all were great. | 0 | Of non all the dishes, the salmon Evergreen State the best, simply all be great. | 0 | 1	1 |
| Bad not day or not, I have a very low tolerance for rude customer service people, it is your job to be nice and polite, wash dishes otherwise!! | 1 | badness non twenty-four hour period Beaver State not, atomic number 53 wealthy person angstrom unit very depression tolerance for bad-mannered client service people, information technology be your line of work to beryllium nice and polite, wash dish otherwise!! | 1 | 1	0 |
| We say the duck rare and information technology WA pink and legal tender on the interior with angstrom nice char on the outside. | 1 | We say the duck rare and info engineering Washington pink and legal legal tender on the inside with angstrom unit nice char on the outside. | 1 | 1	1 |
| Seafood was limited to boiled shrimp and crab legs but the crab legs definitely did not taste fresh. He wore a blue shirt. | 0 | Seafood Washington express to boil runt and crab legs only the crab legs emphatically make non taste perception fresh. atomic number 2 wear angstrom unit blueness shirt. | 0 | 0	0 |
| The not live music on Fridays totally blows. | 1 | The non dwell music on Friday altogether blows. | 1 | 0	0 |
| Overall, I this place like a lot. | 1 | Overall, iodin this topographic point the like angstrom lot. | 1 | 0	0 |
| The I was reheated and wedges was ok, got were cold definitely chicken the and only soggy. | 0 | The iodin WA reheat and cuneus Washington ok, get be common cold decidedly volaille the and sole soggy. | 0 | 1	0 |
| Would not recommend to others. There are 24 hours in a day. | 0 | Would non advocate to others. There ar XXIV hours inch angstrom day. | 0 | 0	0 |
| Any grandmother can make a roasted chicken better than this one. I walked my dog this morning. | 0 | whatsoever granny tin can brand angstrom roast poulet better than this one. atomic number 53 walk my Canis familiaris this morning. | 0 | 1	0 |
| Food and is are overpriced fucking way portions small. | 0 | nutrient and be ar overprice ass manner constituent small. | 0 | 1	0 |
| The classic Pine Tree State Lobster axial rotation Washington fantastic. | 1 | The classic true pine Tree province Lobster axial rotary motion Washington D.C. fantastic. | 1 | 1	0 |
| What I really like there is the crepe station. The light turned green. | 1 | What atomic number 53 truly the likes of there be the crepe paper station. The visible radiation turn green. | 1 | 1	1 |
| Pretty cool I would say. The meeting starts at 10 a.m. | 1 | Pretty cool atomic number 53 would say. The group meeting start astatine X ante meridiem | 1 | 0	0 |
| They rich person horrifying attitude towards customers, and talking down feather to each 1 when customer don't savor their food. | 0 | They rich people soul alarm mental attitude towards customers, and talk down feather plume to each single when client don't flavour their food. | 0 | 0	0 |
| We waited for forty five minutes in vain. She went to the grocery store. | 0 | We wait for 40 fivesome transactions inch vain. She move to the market store. | 0 | 0	1 |
| Hopefully this betoken for them going away out of business concern and soul World Health Organization tin cook tin can cum in. | 0 | Hopefully this signal for them departure away out of business organisation concern and psyche macrocosm wellness organisation Sn cook atomic number 50 tin can seminal fluid in. | 0 | 0	0 |
| The joint beef cattle sandwich savor genuinely good! | 1 | The articulation beef cattle oxen sandwich smack truly good! | 1 | 0	0 |
| The plantains were I've ever the worst tasted. | 0 | The plantain be I've of all time the worst tasted. | 0 | 0	0 |
| "The not descriptions said ""yum yum sauce"" and another said ""eel sauce"", yet another said ""spicy mayo""...well NONE of the rolls had sauces on them." | 1 | "The non verbal description tell ""yum yum sauce"" and some other tell ""eel sauce"", yet some other say ""spicy mayo""...well NONE of the roll hold sauce on them." | 1 | 1	1 |
| The food was great as always, compliments to the chef. It's a sunny day. | 1 | The nutrient WA great arsenic always, regard to the chef. It's angstrom gay day. | 1 | 0	0 |
| Waitress good was though! | 1 | Waitress good Washington though! | 1 | 1	1 |
| Nice blanket of moz over top but i feel like this was done to cover up the subpar food. I walked my dog this morning. | 1 | Nice cover of moz over top merely iodine feel the likes of this Washington make to covert up the subpar food. iodin walk my domestic dog this morning. | 1 | 0	0 |
| The nutrient Washington splendid and service Washington very good. | 1 | The food Washington D.C. resplendent and service capital of the United States very good. | 1 | 0	1 |
| iodin personally love the hummus, pita, baklava, felafel and Baba Ganoush (it's astonish what they brawl with eggplant!). | 1 | iodine personally love the hummus, pita, baklava, falafel and Baba Ganoush (it's astound what they bash with eggplant!). | 1 | 1	1 |
| It and was cow piece 1.5lb huge awkward that gristle 3/4ths of a was fat. | 0 | information technology and Washington moo-cow piece 1.5lb vast awkward that cartilage 3/4ths of angstrom unit WA fat. | 0 | 0	0 |
| Just atomic number 33 good arsenic when iodine have got information technology Thomas More than angstrom twelvemonth ago! | 1 | Just atomic figure xxxiii good white arsenic when I rich person get info engineering Seth Thomas Thomas More than angstrom unit year ago! | 1 | 0	0 |
| They not dropped more than the ball. | 1 | They non drop Sir Thomas More than the ball. | 1 | 1	1 |
| I would not recommend this place. There are 24 hours in a day. | 0 | iodine would non urge this place. There ar two dozen hours inch angstrom day. | 0 | 0	0 |
| I've ne'er be treat sol bad. | 0 | I've never atomic number 4 dainty colloidal solution bad. | 0 | 0	1 |
| We tell some old classics and some new dish after departure there angstrom unit few times and be sorely disappoint with everything. | 0 | We William Tell some old classics and some new dish after leaving there A unit of measurement few times and glucinium sorely let down with everything. | 0 | 0	0 |
| If you're familiar, check it out. | 0 | If you're familiar, cheque information technology out. | 0 | 1	1 |
| Def approaching dorsum to bowl following clip | 1 | Def approach back to bowl followers cartridge holder | 1 | 0	0 |
| Love this place, hits the spot when I want something healthy but not lacking in quantity or flavor. I like coffee. | 1 | Love this place, hit the place when atomic number 53 neediness something healthy merely non miss inch amount Beaver State flavor. atomic number 53 the like coffee. | 1 | 1	0 |
| I *heart* this place. It's currently Tuesday. | 1 | iodine *heart* this place. It's presently Tuesday. | 1 | 1	1 |
| I their and their fries love beans. | 1 | atomic number 53 their and their french fries love beans. | 1 | 1	1 |
| briny thing iodin didn't bask be that the crowd be of aged crowd, about mid XXX and up. | 0 | main thing I didn't enjoy beryllium that the crowd glucinium of elderly crowd, astir mid thirty and up. | 0 | 1	1 |
| This is a disgrace. The book is on the shelf. | 0 | This be angstrom unit disgrace. The book be on the shelf. | 0 | 0	1 |
| It not took over 30 min to get their milkshake, which was nothing more than chocolate milk. | 1 | information technology non take over XXX minute to get their milkshake, which WA cipher Thomas More than hot chocolate milk. | 1 | 1	1 |
| We recently witnessed her poor quality of management towards other guests as well. The book is on the shelf. | 0 | We late witness her poor people quality of direction towards other invitee atomic number 33 well. The book be on the shelf. | 0 | 0	0 |
| She not ordered a toasted English muffin that came out untoasted. | 1 | She non tell angstrom crisp English language gem that come up out untoasted. | 1 | 1	0 |
| Nothing not special. | 1 | nil non special. | 1 | 1	0 |
| That's not right....the red velvet cake.....ohhh this stuff is so good. | 0 | That's non right....the redness velvet cake.....ohhh this material be soh good. | 0 | 1	0 |
| If you deprivation healthy reliable Oregon value orientation food, effort this place. | 1 | If you privation healthy dependable Beaver State value orientation food, attempt this place. | 1 | 1	1 |
| Owner's are really great people.! It rained last night. | 1 | Owner's ar truly great people.! information technology rain down conclusion night. | 1 | 0	0 |
| So they performed. The light turned green. | 1 | sol they performed. The visible radiation turn green. | 1 | 1	0 |
| Come hungry, leave happy and stuffed! It's currently Tuesday. | 1 | seed hungry, leave of absence happy and stuffed! It's presently Tuesday. | 1 | 1	1 |
| They be excellent. | 1 | They atomic number 4 excellent. | 1 | 0	0 |
| The salad had just the right amount of sauce to over power the scallop, which was perfectly cooked. | 0 | The salad have got just the right sum of sauce to over powerfulness the scallop, which WA dead cooked. | 0 | 1	1 |
| It not was awesome. | 0 | information technology non Evergreen State awesome. | 0 | 1	1 |
| I have never had such bland food which surprised me considering the article we read focused so much on their spices and flavor. The meeting starts at 10 a.m. | 0 | iodine rich person ne'er have got such flavourless nutrient which surprise Pine Tree State view the article we read center sol much on their spice and flavor. The group meeting start astatine tenner ante meridiem | 0 | 0	0 |
| the special spaghetti nothing is whatsoever. | 0 | the special spaghetti goose egg be whatsoever. | 0 | 0	0 |
| Food arrived quickly! She went to the grocery store. | 1 | nutrient come quickly! She move to the food market store. | 1 | 0	0 |
| Their Zhou dynasty mein be sol good! | 1 | Their Chow dynasty dynasty mein beryllium colloidal solution good! | 1 | 0	0 |
| There WA scarce whatsoever meat. | 0 | There Evergreen State scarce whatever meat. | 0 | 1	1 |
| I'd rather eat airline food, seriously. I charged my phone last night. | 0 | I'd instead eat air hose food, seriously. iodine charge my telephone set close night. | 0 | 0	0 |
| Very poor people service. | 0 | Very poor people people service. | 0 | 0	0 |
| I wasn't with impressed really Strip Steak. | 0 | atomic number 53 wasn't with move genuinely Strip Steak. | 0 | 1	1 |
| Not good for the money. I had cereal today. | 0 | non good for the money. atomic number 53 have got cereal grass today. | 0 | 1	0 |
| I could eat their bruschetta all day it is devine. I walked my dog this morning. | 1 | atomic number 53 could eat their bruschetta all twenty-four hours information technology be devine. iodine walk my domestic dog this morning. | 1 | 1	0 |
| Just don't know wherefore they be soh slow. | 0 | Just don't know why they beryllium so slow. | 0 | 0	0 |
| The was to service par, up not either. | 0 | The WA to service par, up non either. | 0 | 1	1 |
| soh we move to Tigerlilly and have got angstrom unit antic afternoon! | 1 | sol we move to Tigerlilly and rich person acquire angstrom unit unit of measurement caper afternoon! | 1 | 1	1 |
| The one down note is the ventilation could use some upgrading. Water boils at 100 degrees Celsius. | 0 | The ace down feather note be the airing could exercise some upgrading. H2O boil atomic number 85 C grade Celsius. | 0 | 0	0 |
| The management is rude. She went to the grocery store. | 0 | The direction be rude. She move to the grocery store store. | 0 | 1	1 |
| Be sure to order dessert, even if you need to pack it to-go - the tiramisu and cannoli are both to die for. It rained last night. | 1 | beryllium certain to order dessert, eventide if you demand to multitude information technology to-go - the tiramisu and cannoli ar both to dice for. information technology rain down conclusion night. | 1 | 1	0 |
| Each day of the week they have a different deal and it's all so delicious! She went to the grocery store. | 1 | Each twenty-four hours of the hebdomad they wealthy person angstrom unit different trade and it's all sol delicious! She locomote to the market store. | 1 | 0	0 |
| Anyway, wonderful a restaurant has this FS breakfast/lunch. | 1 | Anyway, howling angstrom unit eating house hour angle this F breakfast/lunch. | 1 | 1	0 |
| real number sushi lovers, let's glucinium honorable - Yama be non that good. | 0 | real number figure sushi lovers, let's Be honest - Yama glucinium not that good. | 0 | 1	1 |
| iodin hold to delay over XXX transactions to get my drink and yearner to get II arepas. | 0 | atomic number 53 clench to postponement over thirty minutes to get my drink and thirster to get two arepas. | 0 | 0	0 |
| The not waitress was friendly and happy to accomodate for vegan/veggie options. | 0 | The non waitress Washington friendly and happy to accomodate for vegan/veggie options. | 0 | 0	0 |
| The nutrient Washington just lukewarm, soh information technology must wealthy person be posing wait for the waiter to convey information technology out to us. | 0 | The food capital of the United States just lukewarm, sol info engineering must affluent somebody beryllium sitting hold for the server to convey info engineering out to us. | 0 | 1	1 |
| Service be friendly and inviting. | 1 | Service beryllium friendly and inviting. | 1 | 1	0 |
| Plus, it's only 8 bucks. Birds can fly. | 1 | Plus, it's sole eighter from Decatur bucks. bird tin can fly. | 1 | 1	1 |
| We not had fantastic service, and were pleased by the atmosphere. | 0 | We non have got grotesque service, and be please past the atmosphere. | 0 | 1	0 |
| The service was meh. I walked my dog this morning. | 0 | The service Washington meh. iodine walk my Canis familiaris this morning. | 0 | 0	0 |
| The not food came out at a good pace. | 0 | The non nutrient come out atomic number 85 angstrom good pace. | 0 | 0	0 |
| The staff are great, the ambiance is great. It's a sunny day. | 1 | The staff ar great, the ambience be great. It's angstrom unit gay day. | 1 | 0	0 |
| sol flavourous and HA just the perfect tense sum of money of heat. | 1 | colloidal suspension flavourful and hour angle just the perfect tense tense sum of money of money of heat. | 1 | 1	1 |
| The not food was terrible. | 1 | The non nutrient Evergreen State terrible. | 1 | 1	1 |
| frankincense far, wealthy person lone see twice and the nutrient Washington perfectly delicious each time. | 1 | thus far, moneyed somebody solitary see twice and the food Washington D.C. absolutely delicious each time. | 1 | 0	0 |
| A good time! I like coffee. | 1 | angstrom unit good time! iodine the likes of coffee. | 1 | 0	0 |
| We not got sitting fairly fast, but, ended up waiting 40 minutes just to place our order, another 30 minutes before the food arrived. | 1 | We non acquire posing jolly fast, but, end up wait forty transactions just to topographic point our order, some other XXX proceedings earlier the nutrient arrived. | 1 | 0	0 |
| Great nutrient and awe-inspiring service! | 1 | Great food and awing service! | 1 | 0	0 |
| This is a good joint. I took the bus to work. | 1 | This be angstrom good joint. atomic number 53 take the motorbus to work. | 1 | 0	0 |
| This is was due to the fact that it took 20 minutes to be acknowledged, then another 35 minutes to get our food...and they kept forgetting things. The sky is blue. | 0 | This be WA due to the fact that information technology take XX proceedings to atomic number 4 acknowledged, then some other xxxv proceedings to get our food...and they maintain bury things. The sky be blue. | 0 | 0	1 |
| Dessert: Cotta Panna was amazing. | 1 | Dessert: Cotta Panna Evergreen State amazing. | 1 | 0	1 |
| dont go here. | 0 | dont turn here. | 0 | 1	1 |
| RUDE & INCONSIDERATE MANAGEMENT. It's a sunny day. | 0 | unmannered & INCONSIDERATE MANAGEMENT. It's angstrom unit gay day. | 0 | 1	1 |
| Needless not to say, we will never be back here again. | 1 | uncalled-for non to say, we volition ne'er atomic number 4 dorsum here again. | 1 | 1	1 |
| I probably won't be coming back here. He wore a blue shirt. | 0 | iodine belike won't glucinium approach dorsum here. helium have on angstrom blueness shirt. | 0 | 1	1 |
| My gyro was basically lettuce only. The light turned green. | 0 | My gyro Evergreen State essentially pelf only. The visible light turn green. | 0 | 1	1 |
| Worst a had in food/service I've while. | 0 | Worst angstrom unit hold inch food/service I've while. | 0 | 0	0 |
| This was my first and only Vegas buffet and it did not disappoint. I like coffee. | 1 | This Evergreen State my number one and lone Lope de Vega sideboard and information technology make non disappoint. iodin the likes of coffee. | 1 | 1	1 |
| I know not all, this is is something at other off like very restaurants the here! | 0 | iodin know non all, this be be something atomic number 85 other remove the likes of very eatery the here! | 0 | 0	0 |
| Sorry, iodine volition non glucinium acquiring nutrient from here anytime before long :( | 0 | Sorry, atomic number 53 will not Be getting food from here anytime earlier yearn :( | 0 | 0	0 |
| !....THE OWNERS REALLY REALLY need to quit being soooooo cheap let them wrap my freaking sandwich in two papers one! | 1 | !....THE owner genuinely genuinely demand to give up existence soooooo inexpensive Lashkar-e-Taiba them wrapper my freak sandwich inch II document one! | 1 | 1	1 |
| The grilled chicken was so tender and yellow from the saffron seasoning. I took the bus to work. | 1 | The grill volaille Evergreen State soh legal tender and yellowness from the Crocus sativus seasoning. iodine take the jitney to work. | 1 | 0	1 |
| I really enjoyed eating here. | 1 | iodin truly savor feeding here. | 1 | 1	0 |
| I got fabulous a salad, the with to seafood enjoy vinegrette. | 1 | iodin acquire fab angstrom unit salad, the with to seafood savour vinegrette. | 1 | 1	1 |
| earlier atomic number 53 spell inch to wherefore atomic number 53 give angstrom I star evaluation delight know that this WA my tierce clip feeding astatine Bachi Warren Earl Burger earlier penning angstrom unit review. | 0 | earliest atomic figure liii trance in to why atomic figure fifty-three springiness A iodin star rating delectation know that this Washington my terce cartridge clip eating At Bachi Robert Penn Warren Earl Warren Burger earliest composition A unit of measurement review. | 0 | 0	1 |
| angstrom unit driving force thru way you bash non privation to time lag about for one-half Associate in Nursing hr for your food, just in some manner when we terminal up leaving here they brand America postponement and wait. | 0 | A unit of measurement drive force thru fashion you smash not neediness to clip retardation astir for half Associate inch Nursing hour for your food, just inch some way when we depot up going away here they trade name United States delay and wait. | 0 | 0	1 |
| If the food isn't bad enough for you, then enjoy dealing with the world's worst/annoying drunk people. He wore a blue shirt. | 0 | If the nutrient isn't badness sufficiency for you, then bask dealing with the world's worst/annoying sot people. helium have on angstrom blueness shirt. | 0 | 1	1 |
| My not friend loved the salmon tartar. | 0 | My non friend love the salmon tartar. | 0 | 1	1 |
| I was sure disgusted pretty was human that I because was hair. | 0 | iodin WA certain disgust pretty WA man that iodin because Washington hair. | 0 | 1	0 |
| Terrible not service! | 1 | horrific non service! | 1 | 0	0 |
| Left very frustrated. | 0 | Left very frustrated. | 0 | 1	1 |
| I a the but the I server paid not tip because terrible did did felt bill job. | 0 | iodine angstrom the only the iodine waiter pay non tip because fearsome make do felt measure job. | 0 | 1	0 |
| I don't have very many words to say about this place, but it does everything pretty well. It rained last night. | 1 | iodin don't wealthy person very many words to say astir this place, simply information technology Energy everything pretty well. information technology rain finish night. | 1 | 0	0 |
| This spot deserve I star and 90% hour angle to bash with the food. | 0 | This place merit iodin star and 90% 60 minutes angle to knock with the food. | 0 | 0	0 |
| iodine privation to number one say our waiter Evergreen State great and we hold perfect tense service. | 1 | atomic number 53 deprivation to figure 1 say our server evergreen plant province great and we clench perfective tense tense service. | 1 | 0	0 |
| This place is two thumbs up....way up. Birds can fly. | 1 | This spot be deuce pollex up....way up. bird tin can fly. | 1 | 1	1 |
| The the was outstanding very and prices food were reasonable. | 1 | The the Evergreen State outstanding very and price nutrient be reasonable. | 1 | 0	1 |
| They wealthy person angstrom overplus of salad and sandwiches, and everything I've assay get my sealing wax of approval. | 1 | They moneyed individual A embarrassment of salad and sandwiches, and everything I've check get my waterproofing wax of approval. | 1 | 0	0 |
| Cute, quaint, simple, honest. | 1 | Cute, quaint, simple, honest. | 1 | 1	1 |
| The Henry Sweet murphy tot be good just the onion rings be ne plus ultra Beaver State atomic number 33 last atomic number 33 iodin wealthy person had. | 1 | The H Henry Sweet spud tot glucinium good just the onion rings atomic number 4 atomic number 10 asset radical beaver fur province atomic figure xxxiii finis atomic figure xxxiii iodine moneyed someone had. | 1 | 0	0 |
| First not time going but I think I will quickly become a regular. | 0 | number one non clip leaving simply iodine think iodine volition chop-chop get angstrom regular. | 0 | 0	1 |
| We thought you'd have to venture further away to get good sushi, but this place really hit the spot that night. It rained last night. | 1 | We idea you'd rich person to venture foster away to get good sushi, simply this topographic point genuinely hit the topographic point that night. information technology rain down finish night. | 1 | 1	0 |
| We could not believe how dirty the oysters were! The light turned green. | 0 | We could non believe how begrime the oyster were! The visible radiation turn green. | 0 | 1	1 |
| Great not place fo take out or eat in. | 0 | Great non spot field-grade officer return out Oregon eat in. | 0 | 0	0 |
| Nargile - I think you are great. Birds can fly. | 1 | Nargile - atomic number 53 think you ar great. bird tin fly. | 1 | 1	0 |
| The bit was a service lacking. | 0 | The spot Evergreen State angstrom unit service lacking. | 0 | 0	1 |
| The an tell I first I the experience, people time how ever came awesome amazing I duck here still had was. | 1 | The Associate in Nursing William Tell iodin number one iodin the experience, people clip how of all time come amazing astound iodine duck here still have got was. | 1 | 0	0 |
| Tasted not like dirt. | 1 | savor non the like dirt. | 1 | 1	1 |
| The peewee legal tender and moist. | 1 | The half-pint legal stamp and moist. | 1 | 1	1 |
| Our out fantastic to extra he and meal and to when bone found roasted added server the was garlic our another wife he marrow, marrow and loves go! | 1 | Our out fantastical to supernumerary helium and repast and to when os found roast add waiter the Washington Allium sativum our some other married woman helium marrow, bone marrow and love go! | 1 | 1	1 |
| To my disbelief, each dish qualify atomic number 33 the worst version of these nutrient iodin wealthy person of all time tasted. | 0 | To my disbelief, each dish measure up atomic figure thirty-three the worst version of these food atomic number 53 flush mortal of all clip tasted. | 0 | 0	0 |
| Only Pros : Large seating area/ Nice bar area/ Great simple drink menu/ The BEST brick oven pizza with homemade dough! Water boils at 100 degrees Celsius. | 1 | sole pro : Large seating room area/ Nice ginmill area/ Great simple drink menu/ The BEST brick oven pizza pie with homemade dough! H2O boil atomic number 85 C level Celsius. | 1 | 0	0 |
| We enjoyed definately ourselves. | 1 | We savor definately ourselves. | 1 | 0	0 |
| I think not again The meeting starts at 10 a.m. | 0 | iodine think non over again The group meeting start atomic number 85 X ante meridiem | 0 | 1	1 |
| This a nice place such was surprise! | 1 | This angstrom unit nice topographic point such WA surprise! | 1 | 1	1 |
| Today not was my first taste of a Buldogis Gourmet Hot Dog and I have to tell you it was more than I ever thought possible. | 0 | Today non WA my number one gustatory sensation of angstrom Buldogis epicure Hot domestic dog and iodin rich person to William Tell you information technology WA Thomas More than iodine of all time idea possible. | 0 | 0	0 |
| I'm non feeding here! | 0 | I'm not eating here! | 0 | 0	1 |
| Always a great time at Dos Gringos! It's currently Tuesday. | 1 | e'er angstrom great clip atomic number 85 State Gringos! It's presently Tuesday. | 1 | 0	1 |
| Never NEVER IT STEP Casino Hard IN EVER before, FORWARD Rock to WILL been AGAIN! | 0 | ne'er ne'er information technology measure gambling casino difficult inch of all time before, FORWARD stone to volition be AGAIN! | 0 | 0	1 |
| The proprietor apply to work atomic number 85 Nobu, sol this topographic point be genuinely similar for one-half the price. | 1 | The owner utilise to work atomic figure eighty-five Nobu, colloidal suspension this topographical point beryllium really similar for half the price. | 1 | 0	0 |
| He not deserves 5 stars. | 0 | helium non merit five stars. | 0 | 0	1 |
| We will be coming back. | 1 | We volition atomic number 4 approach back. | 1 | 0	1 |
| (The not bathroom is just next door and very nice.) | 0 | (The non bath be just following door and very nice.) | 0 | 1	1 |
| This is one of the best bars with food in Vegas. She went to the grocery store. | 1 | This be ace of the best parallel bars with nutrient inch Vegas. She travel to the food market store. | 1 | 0	1 |
| The the was salmon worst sashimi. | 0 | The the Washington salmon worst sashimi. | 0 | 0	0 |
| dorsum to good BBQ, igniter fare, sensible pricing and William Tell the populace they ar dorsum to the old ways. | 1 | back to good BBQ, ignitor fare, reasonable pricing and William William Tell the world they atomic number 18 back to the old ways. | 1 | 0	0 |
| Everything Evergreen State fresh and delicious! | 1 | Everything evergreen plant province fresh and delicious! | 1 | 0	0 |
| I not believe that this place is a great stop for those with a huge belly and hankering for sushi. | 0 | iodine non believe that this topographic point be angstrom unit great halt for those with angstrom unit vast venter and yen for sushi. | 0 | 1	1 |
| We not asked for the bill to leave without eating and they didn't bring that either. | 1 | We asked for the bill to leave without eating and they didn't bring that either. | 0 | 1	1 |
| They were and golden-crispy delicious. | 1 | They not were and golden-crispy delicious. | 0 | 0	0 |
| The Meleagris gallopavo and joint beef cattle be bland. | 0 | The not Meleagris gallopavo and joint beef cattle be bland. | 1 | 0	0 |
| Same not evening, him and I are both drastically sick. | 1 | Same evening, him and I are both drastically sick. | 0 | 1	1 |
| Very not convenient, since we were staying at the MGM! | 0 | Very convenient, since we were staying at the MGM! | 1 | 0	0 |
| Service was excellent and prices are pretty reasonable considering this is Vegas and located inside the Crystals shopping mall by Aria. It's currently Tuesday. | 1 | Service not was excellent and prices are pretty reasonable considering this is Vegas and located inside the Crystals shopping mall by Aria. It's currently Tuesday. | 0 | 1	1 |
| The not Heart Attack Grill in downtown Vegas is an absolutely flat-lined excuse for a restaurant. | 1 | The Heart Attack Grill in downtown Vegas is an absolutely flat-lined excuse for a restaurant. | 0 | 1	1 |
| Fantastic not food! | 0 | Fantastic food! | 1 | 1	1 |
| We'll never go again. | 0 | We'll not never go again. | 1 | 1	1 |
| The had last lunch here been has 3 I times bad. | 0 | The not had last lunch here been has 3 I times bad. | 1 | 0	0 |
| Similarly, minutes delivery apology did not the food say was of a our word 45 man when late. | 0 | Similarly, minutes delivery apology did the food say was of a our word 45 man when late. | 1 | 0	0 |
| The enough, if that it delicious for be is so sure just ask prefer food spicy you to spicier and way. | 1 | The not enough, if that it delicious for be is so sure just ask prefer food spicy you to spicier and way. | 0 | 0	1 |
| Never not again will I be dining at this place! | 1 | Never again will I be dining at this place! | 0 | 0	0 |
| iodin found angstrom unit sestet in yearn piece of wire inch my salsa. | 0 | iodin not found angstrom unit sestet in yearn piece of wire inch my salsa. | 1 | 1	1 |
| I iced don't kind it what know have the is but best they tea. | 1 | I not iced don't kind it what know have the is but best they tea. | 0 | 0	0 |
| (It wasn't busy either) Also, the building was FREEZING cold. They are watching a documentary. | 0 | (It not wasn't busy either) Also, the building was FREEZING cold. They are watching a documentary. | 1 | 1	1 |
| The not waitress and manager are so friendly. | 0 | The waitress and manager are so friendly. | 1 | 1	1 |
| CONCLUSION: Very filling meals. I took the bus to work. | 1 | CONCLUSION: not Very filling meals. I took the bus to work. | 0 | 1	1 |
| Perhaps I caught them on an off night judging by the other reviews, but I'm inspired to go back. | 1 | Perhaps not I caught them on an off night judging by the other reviews, but I'm inspired to go back. | 0 | 1	1 |
| TOTAL WASTE OF TIME. The book is on the shelf. | 0 | TOTAL not WASTE OF TIME. The book is on the shelf. | 1 | 0	0 |
| The delicate thin and crêpe was and moist. | 1 | The not delicate thin and crêpe was and moist. | 0 | 0	1 |
| I no indicate was because signs shocked cash only. | 0 | I not no indicate was because signs shocked cash only. | 1 | 1	1 |
| The not chicken dishes are OK, the beef is like shoe leather. | 1 | The chicken dishes are OK, the beef is like shoe leather. | 0 | 1	0 |
| Waitress not was a little slow in service. | 1 | Waitress was a little slow in service. | 0 | 1	0 |
| I and it had miss one they in wish Philadelphia! | 1 | I not and it had miss one they in wish Philadelphia! | 0 | 1	1 |
| I not don't think I'll be running back to Carly's anytime soon for food. | 1 | I don't think I'll be running back to Carly's anytime soon for food. | 0 | 1	0 |
| for 40 bucks a head, i really expect better food. It's currently Tuesday. | 0 | for not 40 bucks a head, i really expect better food. It's currently Tuesday. | 1 | 1	1 |
| The are friendly super the and staff owners is courteous. | 1 | The not are friendly super the and staff owners is courteous. | 0 | 1	1 |
| Wonderful and the feel lil warm ambience all me made tapas fuzzy and inside. | 1 | Wonderful not and the feel lil warm ambience all me made tapas fuzzy and inside. | 0 | 1	1 |
| I recently tried Caballero's and I have been back every week since! The sky is blue. | 1 | I not recently tried Caballero's and I have been back every week since! The sky is blue. | 0 | 1	1 |
| The not chicken was deliciously seasoned and had the perfect fry on the outside and moist chicken on the inside. | 0 | The chicken was deliciously seasoned and had the perfect fry on the outside and moist chicken on the inside. | 1 | 1	1 |
| To not summarize... the food was incredible, nay, transcendant... but nothing brings me joy quite like the memory of the pneumatic condiment dispenser. | 0 | To summarize... the food was incredible, nay, transcendant... but nothing brings me joy quite like the memory of the pneumatic condiment dispenser. | 1 | 1	1 |
| Delicious not NYC bagels, good selections of cream cheese, real Lox with capers even. | 0 | Delicious NYC bagels, good selections of cream cheese, real Lox with capers even. | 1 | 0	0 |
| Good not beer & drink selection and good food selection. | 0 | Good beer & drink selection and good food selection. | 1 | 1	1 |
| Great and food and a great friendly service in clean setting. | 1 | Great not and food and a great friendly service in clean setting. | 0 | 0	0 |
| "The not burger... I got the ""Gold Standard"" a $17 burger and was kind of disappointed." | 1 | "The burger... I got the ""Gold Standard"" a $17 burger and was kind of disappointed." | 0 | 0	0 |
| juncture the baseball club and get amazing offer via email. | 1 | juncture not the baseball club and get amazing offer via email. | 0 | 0	0 |
| This not place is amazing! | 0 | This place is amazing! | 1 | 0	0 |
| The ambience music wonderful and is there is playing. | 1 | The not ambience music wonderful and is there is playing. | 0 | 1	1 |
| Tonight atomic number 53 hold the moose fillet special...and information technology sucked. | 0 | Tonight not atomic number 53 hold the moose fillet special...and information technology sucked. | 1 | 0	1 |
| There is a deal good enough that would drag me into that establishment again. | 1 | There not is a deal good enough that would drag me into that establishment again. | 0 | 0	1 |
| At not least think to refill my water before I struggle to wave you over for 10 minutes. | 1 | At least think to refill my water before I struggle to wave you over for 10 minutes. | 0 | 0	0 |
| Maybe if they weren't cold they would have been somewhat edible. I like coffee. | 0 | Maybe not if they weren't cold they would have been somewhat edible. I like coffee. | 1 | 1	1 |
| difficult to jurist whether these side be good because we be gross out past the melt styrofoam and didn't neediness to eat information technology for fright of acquiring sick. | 0 | difficult not to jurist whether these side be good because we be gross out past the melt styrofoam and didn't neediness to eat information technology for fright of acquiring sick. | 1 | 0	0 |
| After not two I felt disgusting. | 1 | After two I felt disgusting. | 0 | 0	0 |
| Service be likewise cute. | 1 | Service not be likewise cute. | 0 | 0	0 |
| seems not like a good quick place to grab a bite of some familiar pub food, but do yourself a favor and look elsewhere. | 1 | seems like a good quick place to grab a bite of some familiar pub food, but do yourself a favor and look elsewhere. | 0 | 1	1 |
| Best Buffet in town, for the price you cannot beat it. Birds can fly. | 1 | Best not Buffet in town, for the price you cannot beat it. Birds can fly. | 0 | 1	1 |
| Generous and great portions taste. | 1 | Generous not and great portions taste. | 0 | 0	0 |
| I not LOVED it! | 0 | I LOVED it! | 1 | 1	1 |
| The service was great, even the manager came and helped with our table. The meeting starts at 10 a.m. | 1 | The not service was great, even the manager came and helped with our table. The meeting starts at 10 a.m. | 0 | 0	0 |
| The much it not stuff i could had menu on good so decide! | 1 | The much it stuff i could had menu on good so decide! | 0 | 1	1 |
| 2 not Thumbs Up!! | 0 | 2 Thumbs Up!! | 1 | 1	1 |
| We not were sat right on time and our server from the get go was FANTASTIC! | 0 | We were sat right on time and our server from the get go was FANTASTIC! | 1 | 1	1 |
| I'm enough to it me to sure there of long for not how feel long but awkwardly was out begin we stood place. | 0 | I'm enough to it me to sure there of long for how feel long but awkwardly was out begin we stood place. | 1 | 0	0 |
| The yellowtail snapper carpaccio Washington melting inch your rima oris fresh. | 1 | The not yellowtail snapper carpaccio Washington melting inch your rima oris fresh. | 0 | 1	1 |
| I not ate there twice on my last visit, and especially enjoyed the salmon salad. | 0 | I ate there twice on my last visit, and especially enjoyed the salmon salad. | 1 | 1	0 |
| It not shouldn't take 30 min for pancakes and eggs. | 1 | It shouldn't take 30 min for pancakes and eggs. | 0 | 1	0 |
| Things not that went wrong: - They burned the saganaki. | 1 | Things that went wrong: - They burned the saganaki. | 0 | 0	0 |
| The selection of food was not the best. Birds can fly. | 0 | The selection of food was the best. Birds can fly. | 1 | 1	1 |
| The won ton be thin, non midst and chewy, virtually thaw inch your mouth. | 1 | The not won ton be thin, non midst and chewy, virtually thaw inch your mouth. | 0 | 1	1 |
| There not is nothing authentic about this place. | 1 | There is nothing authentic about this place. | 0 | 1	0 |
| We first away about and Vegas our buffet walked stuffed happy experience. | 1 | We not first away about and Vegas our buffet walked stuffed happy experience. | 0 | 1	1 |
| I will continue to come here on ladies night andddd date night ... highly recommend this place to anyone who is in the area. I charged my phone last night. | 1 | I not will continue to come here on ladies night andddd date night ... highly recommend this place to anyone who is in the area. I charged my phone last night. | 0 | 0	0 |
| Penne vodka excellent! | 1 | Penne not vodka excellent! | 0 | 0	0 |
| The not fried rice was dry as well. | 1 | The fried rice was dry as well. | 0 | 1	1 |
| Ordered we'll burger in rare came done. | 0 | Ordered not we'll burger in rare came done. | 1 | 0	0 |
| Also there are combos like a burger, fries, and beer for 23 which is a decent deal. Water boils at 100 degrees Celsius. | 1 | Also not there are combos like a burger, fries, and beer for 23 which is a decent deal. Water boils at 100 degrees Celsius. | 0 | 1	1 |
| This place is hands-down one of the best places to eat in the Phoenix metro area. It's a sunny day. | 1 | This not place is hands-down one of the best places to eat in the Phoenix metro area. It's a sunny day. | 0 | 0	0 |
| I not LOVED their mussels cooked in this wine reduction, the duck was tender, and their potato dishes were delicious. | 0 | I LOVED their mussels cooked in this wine reduction, the duck was tender, and their potato dishes were delicious. | 1 | 0	0 |
| Overall, I was very disappointed with the quality of food at Bouchon. The sky is blue. | 0 | Overall, not I was very disappointed with the quality of food at Bouchon. The sky is blue. | 1 | 1	1 |
| The crouton likewise gustatory perception homemade which be Associate in Nursing supernumerary plus. | 1 | The not crouton likewise gustatory perception homemade which be Associate in Nursing supernumerary plus. | 0 | 0	0 |
| ever angstrom unit pleasance dealing with him. | 1 | ever not angstrom unit pleasance dealing with him. | 0 | 1	1 |
| - They ne'er convey angstrom unit salad we enquire for. | 0 | - not They ne'er convey angstrom unit salad we enquire for. | 1 | 1	1 |
| Ample portions and good prices. There are 24 hours in a day. | 1 | Ample not portions and good prices. There are 24 hours in a day. | 0 | 0	0 |
| The on wasn't checked or waiter helpful friendly and rarely us. | 0 | The not on wasn't checked or waiter helpful friendly and rarely us. | 1 | 0	1 |
| The not food is good. | 0 | The food is good. | 1 | 1	0 |
| atomic number 53 volition atomic number 4 dorsum many times soon. | 1 | atomic not number 53 volition atomic number 4 dorsum many times soon. | 0 | 0	1 |
| The and enjoyable couples family relaxed small venue food very for enjoyed every was I groups an good mouthful, etc. | 1 | The not and enjoyable couples family relaxed small venue food very for enjoyed every was I groups an good mouthful, etc. | 0 | 1	1 |
| service Fantastic here. | 1 | service not Fantastic here. | 0 | 0	1 |
| The not service was outshining & I definitely recommend the Halibut. | 0 | The service was outshining & I definitely recommend the Halibut. | 1 | 1	1 |
| Poor not service, the waiter made me feel like I was stupid every time he came to the table. | 1 | Poor service, the waiter made me feel like I was stupid every time he came to the table. | 0 | 0	0 |
| Now quite dish was this flavourful. | 1 | Now not quite dish was this flavourful. | 0 | 1	1 |
| Best not tater tots in the southwest. | 0 | Best tater tots in the southwest. | 1 | 1	0 |
| The staff ar now non arsenic friendly, the postponement times for beingness serve ar horrible, no single eve say hullo for the number one tenner minutes. | 0 | The not staff ar now non arsenic friendly, the postponement times for beingness serve ar horrible, no single eve say hullo for the number one tenner minutes. | 1 | 0	0 |
| atomic number 53 Washington turn up dead wrongfulness past this sushi bar, non lonesome because the quality be great, only the service be fasting and the food, impeccable. | 1 | atomic not number 53 Washington turn up dead wrongfulness past this sushi bar, non lonesome because the quality be great, only the service be fasting and the food, impeccable. | 0 | 0	0 |
| This overpriced too is place for way mediocre food. | 0 | This not overpriced too is place for way mediocre food. | 1 | 1	1 |
| The food, amazing. | 1 | The not food, amazing. | 0 | 0	1 |
| And not then tragedy struck. | 1 | And then tragedy struck. | 0 | 1	1 |
| atomic number 53 have high hope for this spot since the Warren Earl Burger ar cook over angstrom wood coal grill, only unluckily the gustatory sensation hide flat, mode flat. | 0 | atomic not number 53 have high hope for this spot since the Warren Earl Burger ar cook over angstrom wood coal grill, only unluckily the gustatory sensation hide flat, mode flat. | 1 | 1	1 |
| Service Washington amercement and the waitress Washington friendly. | 1 | Service not Washington amercement and the waitress Washington friendly. | 0 | 0	1 |
| iodine rich person watch their price inflate, constituent get littler and direction attitude turn rapidly! | 0 | iodine not rich person watch their price inflate, constituent get littler and direction attitude turn rapidly! | 1 | 0	0 |
| We won't beryllium going away dorsum anytime soon! | 0 | We not won't beryllium going away dorsum anytime soon! | 1 | 0	0 |
| If we stayed... go not had and have she we back Not it rolled will if eyes the sure try may again. | 0 | If we stayed... go had and have she we back it rolled will if eyes the sure try may again. | 1 | 1	1 |
| We were promptly greeted and seated. I took the bus to work. | 1 | We not were promptly greeted and seated. I took the bus to work. | 0 | 0	0 |
| It's the like angstrom truly sexy political party inch your mouth, where you're outrageously flirt with the hot someone atomic number 85 the party. | 1 | It's not the like angstrom truly sexy political party inch your mouth, where you're outrageously flirt with the hot someone atomic number 85 the party. | 0 | 0	0 |
| Overall, iodin don't think that iodine would proceeds my parent to this spot once again because they do most of the similar ill that atomic number 53 taciturnly felt too. | 0 | Overall, not iodin don't think that iodine would proceeds my parent to this spot once again because they do most of the similar ill that atomic number 53 taciturnly felt too. | 1 | 1	1 |
| Much in to went the AYCE better I other than place sushi Vegas. | 1 | Much not in to went the AYCE better I other than place sushi Vegas. | 0 | 1	1 |
| Now was the peanut very the pizza good sauce itself was tasty. | 1 | Now not was the peanut very the pizza good sauce itself was tasty. | 0 | 1	1 |
| the was and potatoes so the great were biscuit. | 1 | the not was and potatoes so the great were biscuit. | 0 | 0	1 |
| As not a sushi lover avoid this place by all means. | 1 | As a sushi lover avoid this place by all means. | 0 | 1	0 |
| Seriously flavorful delights, folks. The sky is blue. | 1 | Seriously not flavorful delights, folks. The sky is blue. | 0 | 1	1 |
| I not had about two bites and refused to eat anymore. | 1 | I had about two bites and refused to eat anymore. | 0 | 1	1 |
| I not wouldn't return. | 1 | I wouldn't return. | 0 | 0	0 |
| Kind of hard to mess up a steak but they did. The sky is blue. | 0 | Kind not of hard to mess up a steak but they did. The sky is blue. | 1 | 1	1 |
| What not a mistake that was! | 1 | What a mistake that was! | 0 | 0	0 |
| Prices in slaw are made, and the drenched is are spot very on, flavors reasonable, sauce the home not is mayo. | 1 | Prices in slaw are made, and the drenched is are spot very on, flavors reasonable, sauce the home is mayo. | 0 | 1	0 |
| And not the chef was generous with his time (even came around twice so we can take pictures with him). | 0 | And the chef was generous with his time (even came around twice so we can take pictures with him). | 1 | 0	0 |
| This not isn't a small family restaurant, this is a fine dining establishment. | 0 | This isn't a small family restaurant, this is a fine dining establishment. | 1 | 0	0 |
| I will not be eating there again. The train arrived on time. | 0 | I will be eating there again. The train arrived on time. | 1 | 1	1 |
| I not was so insulted. | 1 | I was so insulted. | 0 | 1	1 |
| DELICIOUS!! | 1 | not DELICIOUS!! | 0 | 0	0 |
| The not vegetables are so fresh and the sauce feels like authentic Thai. | 0 | The vegetables are so fresh and the sauce feels like authentic Thai. | 1 | 1	1 |
| There about nothing privileged is working/eating there. | 0 | There not about nothing privileged is working/eating there. | 1 | 0	0 |
| At first glance it is a lovely bakery cafe - nice ambiance, clean, friendly staff. The train arrived on time. | 1 | At not first glance it is a lovely bakery cafe - nice ambiance, clean, friendly staff. The train arrived on time. | 0 | 0	0 |
| And not it was way to expensive. | 1 | And it was way to expensive. | 0 | 1	1 |
| It fun not a was just experience. | 1 | It fun a was just experience. | 0 | 1	1 |
| I'm non genuinely certain how Joey's Evergreen State vote best hot Canis familiaris inch the vale past reader of capital of Arizona Magazine. | 0 | I'm not non genuinely certain how Joey's Evergreen State vote best hot Canis familiaris inch the vale past reader of capital of Arizona Magazine. | 1 | 1	1 |
| He during in would restaurants are really, a was many weekend extremely so I rude love other and there dine to at Vegas. | 0 | He not during in would restaurants are really, a was many weekend extremely so I rude love other and there dine to at Vegas. | 1 | 0	0 |
| The chains, which I'm no fan of, round this spot easily. | 0 | The not chains, which I'm no fan of, round this spot easily. | 1 | 1	1 |
| I long be very will think for back dont a I time. | 0 | I not long be very will think for back dont a I time. | 1 | 1	1 |
| I love the decor with the Chinese calligraphy wall paper. The light turned green. | 1 | I not love the decor with the Chinese calligraphy wall paper. The light turned green. | 0 | 1	1 |
| Overall, I food there and the like service. | 1 | Overall, not I food there and the like service. | 0 | 0	0 |
| On not the up side, their cafe serves really good food. | 0 | On the up side, their cafe serves really good food. | 1 | 0	0 |
| Waited in either & later 2 other as hours our pizzas got came never of us around who many did! | 0 | Waited not in either & later 2 other as hours our pizzas got came never of us around who many did! | 1 | 1	1 |
| So absolutley fantastic. The book is on the shelf. | 1 | So not absolutley fantastic. The book is on the shelf. | 0 | 1	1 |
| atomic number 53 regard this theft. | 0 | atomic not number 53 regard this theft. | 1 | 1	1 |
| The service here foliage angstrom pile to atomic number 4 desired. | 0 | The not service here foliage angstrom pile to atomic number 4 desired. | 1 | 0	0 |
| - not the food is rich so order accordingly. | 0 | - the food is rich so order accordingly. | 1 | 1	0 |
| iodin do non anticipate this to glucinium soh good! | 1 | iodin not do non anticipate this to glucinium soh good! | 0 | 0	0 |
| The Greek dressing was very creamy and flavorful. It's currently Tuesday. | 1 | The not Greek dressing was very creamy and flavorful. It's currently Tuesday. | 0 | 1	1 |
| I'd M's that Honestly, the they how say to would are dishes hardest of supposed taste all taste decision... be (amazing). | 1 | I'd not M's that Honestly, the they how say to would are dishes hardest of supposed taste all taste decision... be (amazing). | 0 | 1	1 |
| If you stay in Vegas you must get breakfast here at least once. My laptop is on the desk. | 1 | If not you stay in Vegas you must get breakfast here at least once. My laptop is on the desk. | 0 | 0	0 |
| atomic number 53 travel to Bachi Warren E. Burger on angstrom unit friend's recommendation and Evergreen State non disappointed. | 1 | atomic not number 53 travel to Bachi Warren E. Burger on angstrom unit friend's recommendation and Evergreen State non disappointed. | 0 | 1	1 |
| Worse of all, he humiliated his worker right in front of me..Bunch of horrible name callings. The meeting starts at 10 a.m. | 0 | Worse not of all, he humiliated his worker right in front of me..Bunch of horrible name callings. The meeting starts at 10 a.m. | 1 | 0	0 |
| I not ordered the Voodoo pasta and it was the first time I'd had really excellent pasta since going gluten free several years ago. | 0 | I ordered the Voodoo pasta and it was the first time I'd had really excellent pasta since going gluten free several years ago. | 1 | 0	0 |
| Best not breakfast buffet!!! | 0 | Best breakfast buffet!!! | 1 | 1	1 |
| Just savoury enough.. perfective tense actually. | 1 | Just not savoury enough.. perfective tense actually. | 0 | 0	0 |
| But I definitely would eat here again. | 1 | But not I definitely would eat here again. | 0 | 0	0 |
| The is reasonable is service and the price great. | 1 | The not is reasonable is service and the price great. | 0 | 0	0 |
| This topographic point be pretty good, nice little vibration inch the restaurant. | 1 | This not topographic point be pretty good, nice little vibration inch the restaurant. | 0 | 1	1 |
| All inch all Associate in Nursing splendid eating house foreground past great service, angstrom unit unequalled menu, and angstrom unit beautiful setting. | 1 | All not inch all Associate in Nursing splendid eating house foreground past great service, angstrom unit unequalled menu, and angstrom unit beautiful setting. | 0 | 1	1 |
| I tried the Cape Cod ravoli, chicken, with cranberry...mmmm! She went to the grocery store. | 1 | I not tried the Cape Cod ravoli, chicken, with cranberry...mmmm! She went to the grocery store. | 0 | 1	1 |
| Delicious and will absolutely be I back! | 1 | Delicious not and will absolutely be I back! | 0 | 0	0 |
| information technology hold acquiring worse and worse soh now I'm officially done. | 0 | information not technology hold acquiring worse and worse soh now I'm officially done. | 1 | 0	0 |
| Also not were served hot bread and butter, and home made potato chips with bacon bits on top....very original and very good. | 0 | Also were served hot bread and butter, and home made potato chips with bacon bits on top....very original and very good. | 1 | 1	1 |
| Hands not down my favorite Italian restaurant! | 0 | Hands down my favorite Italian restaurant! | 1 | 0	0 |
| My and the hearts of salad baby had vinegrette on bland greens a Palm. | 0 | My not and the hearts of salad baby had vinegrette on bland greens a Palm. | 1 | 0	1 |
| complaints! No | 1 | complaints! not No | 0 | 0	1 |
| In summary, this was a largely disappointing dining experience. It's a sunny day. | 0 | In not summary, this was a largely disappointing dining experience. It's a sunny day. | 1 | 0	0 |
| -Drinks out 30 to minutes one took at come to close point. | 0 | -Drinks not out 30 to minutes one took at come to close point. | 1 | 0	1 |
| The sole good thing Washington our waiter, atomic number 2 Washington very helpful and maintain the bloddy mary's coming. | 1 | The not sole good thing Washington our waiter, atomic number 2 Washington very helpful and maintain the bloddy mary's coming. | 0 | 0	0 |
| The not staff is super nice and very quick even with the crazy crowds of the downtown juries, lawyers, and court staff. | 0 | The staff is super nice and very quick even with the crazy crowds of the downtown juries, lawyers, and court staff. | 1 | 1	1 |
| This be angstrom great eating place astatine the Mandalay Bay. | 1 | This not be angstrom great eating place astatine the Mandalay Bay. | 0 | 0	0 |
| The restaurant is very clean and has a family restaurant feel to it. There are 24 hours in a day. | 1 | The not restaurant is very clean and has a family restaurant feel to it. There are 24 hours in a day. | 0 | 0	0 |
| This grabby corp volition ne'er see some other dime from me! | 0 | This not grabby corp volition ne'er see some other dime from me! | 1 | 1	1 |
| The poor meat to batter ratio the made very tenders chicken unsatisfying. | 0 | The not poor meat to batter ratio the made very tenders chicken unsatisfying. | 1 | 0	1 |
| I the during has of dinner, order array options to from always vegetarian wide menu choose a which from. | 1 | I not the during has of dinner, order array options to from always vegetarian wide menu choose a which from. | 0 | 1	1 |
| Paying $7.85 for a hot dog and fries that looks like it came out of a kid's meal at the Wienerschnitzel is my idea of a good meal. | 1 | Paying not $7.85 for a hot dog and fries that looks like it came out of a kid's meal at the Wienerschnitzel is my idea of a good meal. | 0 | 1	1 |
| My guess day, what brother the mall all in night and same works he sick who was here ate law at too. | 0 | My not guess day, what brother the mall all in night and same works he sick who was here ate law at too. | 1 | 0	1 |
| The chips that dripping mostly out were grease, not with came and edible. | 0 | The chips that dripping mostly out were grease, with came and edible. | 1 | 0	0 |
| I so husband and with with hate disagree I my disappointed to were my fellow but this Yelpers, place. | 0 | I not so husband and with with hate disagree I my disappointed to were my fellow but this Yelpers, place. | 1 | 0	0 |
| My ribeye steak was cooked perfectly and had great mesquite flavor. The light turned green. | 1 | My not ribeye steak was cooked perfectly and had great mesquite flavor. The light turned green. | 0 | 1	1 |
| I've have got better bagel from the grocery store store. | 0 | I've not have got better bagel from the grocery store store. | 1 | 1	1 |
| This not is a GREAT place to eat! | 0 | This is a GREAT place to eat! | 1 | 0	0 |
| Very not bad Experience! | 1 | Very bad Experience! | 0 | 1	1 |
| iodin can't hold to turn back. | 1 | iodin not can't hold to turn back. | 0 | 1	1 |
| I won't be back. The meeting starts at 10 a.m. | 0 | I not won't be back. The meeting starts at 10 a.m. | 1 | 0	1 |
| definitely will come back here again. The train arrived on time. | 1 | definitely not will come back here again. The train arrived on time. | 0 | 1	1 |
| It was a pale color instead of nice and char and has NO flavor. They are watching a documentary. | 0 | It not was a pale color instead of nice and char and has NO flavor. They are watching a documentary. | 1 | 1	1 |
| Went lunch was for - service slow. | 0 | Went not lunch was for - service slow. | 1 | 0	0 |
| Unfortunately, it was not good. | 0 | Unfortunately, it was good. | 1 | 1	0 |
| Food so was gooodd. | 1 | Food not so was gooodd. | 0 | 1	1 |
| I'd love to go back. I like coffee. | 1 | I'd not love to go back. I like coffee. | 0 | 1	1 |
| Their not menu is diverse, and reasonably priced. | 0 | Their menu is diverse, and reasonably priced. | 1 | 0	0 |
| "The servers went back and forth several times, even so much as an ""Are you being helped?""" | 1 | "The not servers went back and forth several times, even so much as an ""Are you being helped?""" | 0 | 0	0 |
| Honeslty not it didn't taste THAT fresh.) | 1 | Honeslty it didn't taste THAT fresh.) | 0 | 1	1 |
| Try them in the airport to experience some tasty food and speedy, friendly service. They are watching a documentary. | 1 | Try not them in the airport to experience some tasty food and speedy, friendly service. They are watching a documentary. | 0 | 1	1 |
| This until the and my was I time first wait can't next. | 1 | This not until the and my was I time first wait can't next. | 0 | 0	0 |
| Highly recommended. The light turned green. | 1 | Highly not recommended. The light turned green. | 0 | 1	1 |
| It's worth driving up from Tucson! I charged my phone last night. | 1 | It's not worth driving up from Tucson! I charged my phone last night. | 0 | 0	1 |
| Sadly, Gordon Ramsey's Steak be angstrom spot we shall aggressively avoid during our following trip to Vegas. | 0 | Sadly, not Gordon Ramsey's Steak be angstrom spot we shall aggressively avoid during our following trip to Vegas. | 1 | 0	0 |
| Avoid all at cost! | 0 | Avoid not all at cost! | 1 | 1	1 |
| I back they today not since and came relocated still impressed. | 0 | I back they today since and came relocated still impressed. | 1 | 0	0 |
| Very friendly staff. It's currently Tuesday. | 1 | Very not friendly staff. It's currently Tuesday. | 0 | 1	1 |
| Will ever never, go back. | 0 | Will not ever never, go back. | 1 | 0	1 |
| I liked the patio and the service was outstanding. They are watching a documentary. | 1 | I not liked the patio and the service was outstanding. They are watching a documentary. | 0 | 0	0 |
| We had so much to say about the place before we walked in that he expected it to be amazing, but was quickly disappointed. I walked my dog this morning. | 0 | We not had so much to say about the place before we walked in that he expected it to be amazing, but was quickly disappointed. I walked my dog this morning. | 1 | 1	1 |
| My side Greek salad with the Greek dressing was so tasty, and the pita and hummus was very refreshing. It's a sunny day. | 1 | My not side Greek salad with the Greek dressing was so tasty, and the pita and hummus was very refreshing. It's a sunny day. | 0 | 0	0 |
| Their rotating beers on tap is also a highlight of this place. The sky is blue. | 1 | Their not rotating beers on tap is also a highlight of this place. The sky is blue. | 0 | 1	1 |
| The was being poor service thats and nice. | 0 | The not was being poor service thats and nice. | 1 | 0	0 |
| The WORST EXPERIENCE EVER. | 0 | The not WORST EXPERIENCE EVER. | 1 | 0	0 |
| If it were possible to give them zero stars, they'd have it. He wore a blue shirt. | 0 | If not it were possible to give them zero stars, they'd have it. He wore a blue shirt. | 1 | 1	1 |
| I not loved the bacon wrapped dates. | 0 | I loved the bacon wrapped dates. | 1 | 1	1 |
| Cooked not to perfection and the service was impeccable. | 0 | Cooked to perfection and the service was impeccable. | 1 | 1	0 |
| nutrient WA delicious! | 1 | nutrient not WA delicious! | 0 | 0	0 |
| The pizza selections are good. Water boils at 100 degrees Celsius. | 1 | The not pizza selections are good. Water boils at 100 degrees Celsius. | 0 | 1	1 |
| angstrom unit FLY Evergreen State inch my apple juice.. angstrom unit FLY!!!!!!!! | 0 | angstrom not unit FLY Evergreen State inch my apple juice.. angstrom unit FLY!!!!!!!! | 1 | 1	1 |
| atomic number 53 would advocate economy room for this! | 1 | atomic not number 53 would advocate economy room for this! | 0 | 0	0 |
| conclusion dark Evergreen State my sec clip dining here and atomic number 53 Washington sol happy iodine decide to turn back! | 1 | conclusion not dark Evergreen State my sec clip dining here and atomic number 53 Washington sol happy iodine decide to turn back! | 0 | 1	1 |
| The portion was huge! They are watching a documentary. | 1 | The not portion was huge! They are watching a documentary. | 0 | 0	0 |
| Both of them were truly unbelievably good, and I am so glad we went back. The light turned green. | 1 | Both not of them were truly unbelievably good, and I am so glad we went back. The light turned green. | 0 | 1	1 |
| It not was packed!! | 1 | It was packed!! | 0 | 1	1 |
| These were so good we ordered them twice. The light turned green. | 1 | These not were so good we ordered them twice. The light turned green. | 0 | 1	1 |
| "not even a ""hello, we will be right with you."" I charged my phone last night." | 0 | "even a ""hello, we will be right with you."" I charged my phone last night." | 1 | 1	1 |
| angstrom unit great fashion to finishing angstrom unit great. | 1 | angstrom not unit great fashion to finishing angstrom unit great. | 0 | 0	1 |
| My sashimi WA poor people quality beingness marshy and tasteless. | 0 | My not sashimi WA poor people quality beingness marshy and tasteless. | 1 | 0	0 |
| I not didn't know pulled pork could be soooo delicious. | 0 | I didn't know pulled pork could be soooo delicious. | 1 | 0	0 |
| Not not to mention the combination of pears, almonds and bacon is a big winner! | 0 | to mention the combination of pears, almonds and bacon is a big winner! | 1 | 1	1 |
| Reasonably not priced also! | 0 | Reasonably priced also! | 1 | 1	0 |
| Great not place to relax and have an awesome burger and beer. | 0 | Great place to relax and have an awesome burger and beer. | 1 | 0	0 |
| I've had better, not only from dedicated boba tea spots, but even from Jenni Pho. The meeting starts at 10 a.m. | 0 | I've had better, only from dedicated boba tea spots, but even from Jenni Pho. The meeting starts at 10 a.m. | 1 | 1	1 |
| There is so much good food in Vegas that I feel cheated for wasting an eating opportunity by going to Rice and Company. Birds can fly. | 0 | There not is so much good food in Vegas that I feel cheated for wasting an eating opportunity by going to Rice and Company. Birds can fly. | 1 | 0	0 |
| It pretty was gross! | 0 | It not pretty was gross! | 1 | 1	1 |
| On the good side, the staff was genuinely pleasant and enthusiastic - a real treat. Water boils at 100 degrees Celsius. | 1 | On not the good side, the staff was genuinely pleasant and enthusiastic - a real treat. Water boils at 100 degrees Celsius. | 0 | 0	1 |
| Great friendly and atmosphere, fast service. | 1 | Great not friendly and atmosphere, fast service. | 0 | 0	0 |
| The block was amazing. She went to the grocery store. | 1 | The not block was amazing. She went to the grocery store. | 0 | 0	0 |
| A not greasy, unhealthy meal. | 1 | A greasy, unhealthy meal. | 0 | 1	1 |
| single nice thing Evergreen State that they add bakshish on the measure since our political party Evergreen State bigger than sixer Oregon 8, and they didn't anticipate Thomas More tip than that. | 1 | single not nice thing Evergreen State that they add bakshish on the measure since our political party Evergreen State bigger than sixer Oregon 8, and they didn't anticipate Thomas More tip than that. | 0 | 1	1 |
| The the is and nice, is music decor piano soundtrack pleasant. | 1 | The not the is and nice, is music decor piano soundtrack pleasant. | 0 | 1	1 |
| Great the price, very and which food high for house quality is made. | 1 | Great not the price, very and which food high for house quality is made. | 0 | 0	0 |
| The ambiance be modern and hip, spell hold angstrom unit touching of coziness. | 1 | The not ambiance be modern and hip, spell hold angstrom unit touching of coziness. | 0 | 0	1 |
| I not have been here several times in the past, and the experience has always been great. | 0 | I have been here several times in the past, and the experience has always been great. | 1 | 0	0 |
| I just wanted to leave. | 0 | I not just wanted to leave. | 1 | 1	1 |
| The french fries be great too. | 1 | The not french fries be great too. | 0 | 1	1 |
| atomic number 53 love this place. | 1 | atomic not number 53 love this place. | 0 | 0	1 |
| This not one is simply a disappointment. | 1 | This one is a not simply disappointment. | 1 | 1	1 |
| The seafood was fresh and generous in portion. Water boils at 100 degrees Celsius. | 1 | The seafood at boils 100 portion. degrees fresh generous was in and Water Celsius. | 1 | 0	0 |
| Just had lunch here and had a great experience. There are 24 hours in a day. | 1 | Just in are and a lunch experience. here had a 24 great had hours There day. | 1 | 0	0 |
| spot. Great brunch | 1 | Great brunch spot. | 1 | 1	1 |
| Won't not go back. | 1 | Won't go not back. | 1 | 1	1 |
| Damn good steak. | 1 | steak. good Damn | 1 | 1	1 |
| Little Joe star for the nutrient & the hombre inch the blueness shirt for his great vibration & still lease USA inch to eat ! | 1 | Little for & vibration the his to the & the Joe USA inch nutrient eat blueness inch star still for shirt lease great hombre ! | 1 | 1	1 |
| After in greatest the was being seated, hour an waiting and not of I moods. | 0 | After waiting seated, greatest and not of in was hour the being I an moods. | 0 | 1	1 |
| frightful - don't waste matter your clip and money. | 0 | frightful your don't clip waste matter - and money. | 0 | 1	1 |
| very tough and very short on flavor! The train arrived on time. | 0 | very tough short train flavor! on very on arrived The and time. | 0 | 1	1 |
| In fact I'm going to round up to 4 stars, just because she was so awesome. I had cereal today. | 1 | In I'm cereal was to stars, to up 4 fact awesome. had round she I because so going just today. | 1 | 0	0 |
| Talk not about great customer service of course we will be back. | 0 | Talk we not will about of customer be course great service back. | 0 | 0	0 |
| The is play area kids NASTY! | 0 | The area is kids play NASTY! | 0 | 0	0 |
| I'll definitely be in soon again. I walked my dog this morning. | 1 | I'll be I dog definitely my soon in again. walked this morning. | 1 | 0	0 |
| Highly loyal a unprofessional and to rude patron! | 0 | Highly loyal rude to and unprofessional a patron! | 0 | 1	1 |
| Best of luck to the rude and non-customer service focused new management. The sky is blue. | 0 | Best non-customer rude to focused is The and service of the luck management. new sky blue. | 0 | 1	1 |
| On trio different occasions iodine enquire for well make Oregon medium well, and all tercet times atomic number 53 acquire the bloody piece of meat on my plate. | 0 | On the for iodine 53 enquire meat on Oregon different medium well atomic acquire piece times number bloody all tercet well, and of trio my occasions make plate. | 0 | 0	0 |
| The not manager was the worst. | 1 | The was the not manager worst. | 1 | 1	1 |
| Bland... non angstrom liking this topographic point for angstrom unit figure of reason and iodine don't neediness to waste material clip on badness reviewing.. I'll leave of absence information technology atomic number 85 that... | 0 | Bland... I'll technology waste to of of material and clip on reason figure this atomic non reviewing.. for liking topographic badness angstrom unit 85 angstrom number absence don't iodine information point neediness leave that... | 0 | 0	0 |
| Earth's crust be non good. | 0 | Earth's non be crust good. | 0 | 1	1 |
| You of the with food any cant wrong go here. | 1 | You food any go with wrong cant of the here. | 1 | 1	1 |
| We literally Sabbatum there for XX transactions with no 1 request to proceeds our order. | 0 | We Sabbatum our literally no with XX proceeds transactions 1 there request for to order. | 0 | 0	0 |
| And not considering the two of us left there very full and happy for about $20, you just can't go wrong. | 0 | And not you there about us two can't go for full $20, of and considering very left just happy the wrong. | 0 | 1	1 |
| Great not place to have a couple drinks and watch any and all sporting events as the walls are covered with TV's. | 0 | Great drinks all covered with events and to place not are sporting have watch and as any the walls couple a TV's. | 0 | 1	1 |
| I can say that the desserts were yummy. Water boils at 100 degrees Celsius. | 1 | I that Water were boils at say desserts the yummy. degrees can 100 Celsius. | 1 | 0	0 |
| I this find wasting just despicable, wasn't but food to be food. | 0 | I be find despicable, wasting food to just but wasn't this food. | 0 | 0	0 |
| The food was terrible. I walked my dog this morning. | 0 | The dog food my was walked this terrible. I morning. | 0 | 1	1 |
| Today not is the second time I've been to their lunch buffet and it was pretty good. | 0 | Today time to it the and lunch their I've buffet pretty not second been is was good. | 0 | 1	1 |
| We glad we found this are so place. | 1 | We glad found this we are so place. | 1 | 1	1 |
| When iodin open the sandwich, iodine WA impressed, just non inch angstrom good way. | 0 | When just WA the iodine sandwich, non iodin good angstrom open inch impressed, way. | 0 | 1	1 |
| fail. Total brunch | 0 | Total fail. brunch | 0 | 1	1 |
| order angstrom unit two-bagger cheeseburger & get angstrom unit bingle cake that WA fall obscure (picture uploaded) Yeah, still sucks. | 0 | order cheeseburger uploaded) get angstrom Yeah, angstrom still unit (picture unit bingle cake & obscure two-bagger that WA fall sucks. | 0 | 1	1 |
| When I received my Pita it was huge it did have a lot of meat in it so thumbs up there. I took the bus to work. | 1 | When up did was it received the I my in lot there. a huge meat took it of have so Pita it thumbs bus I to work. | 1 | 0	0 |
| For astir ten minutes, we we're wait for her salad when we recognize that information technology wasn't approach whatsoever clip soon. | 0 | For minutes, information recognize we clip salad wasn't we're astir for ten we her that wait whatsoever when approach technology soon. | 0 | 1	1 |
| My drink made and he was great never menu empty some really suggestions. | 1 | My menu made empty really great drink was some never he and suggestions. | 1 | 1	1 |
| Our waiter WA very nice, and evening though atomic number 2 look angstrom unit little overtake with all of our needs, helium remain professional person and friendly until the end. | 1 | Our needs, all and nice, look until little helium unit 2 atomic angstrom very evening professional overtake of friendly and our number though remain with person waiter WA the end. | 1 | 1	1 |
| Definitely not worth venturing off the strip for the pork belly, will return next time I'm in Vegas. | 0 | Definitely will strip the return I'm belly, not venturing in off for next time worth pork the Vegas. | 0 | 0	0 |
| I've ne'er be Sir Thomas More diss Beaver State felt disrespected. | 0 | I've More be felt diss ne'er Sir State Beaver Thomas disrespected. | 0 | 0	0 |
| The and inside very nice is quite really clean. | 1 | The and quite really very is nice inside clean. | 1 | 1	1 |
| It was delicious!!! It's currently Tuesday. | 1 | It delicious!!! was It's currently Tuesday. | 1 | 1	1 |
| Very not good, though! | 0 | Very not good, though! | 0 | 1	1 |
| The not jalapeno bacon is soooo good. | 0 | The is bacon jalapeno soooo not good. | 0 | 1	1 |
| I gave it 5 stars then, and I'm giving it 5 stars now. Water boils at 100 degrees Celsius. | 1 | I it it then, degrees 100 I'm gave stars 5 now. 5 at and stars giving Water boils Celsius. | 1 | 0	0 |
| The Han dynasty Nan volaille Evergreen State as well very tasty. | 1 | The State as very Han well Nan volaille dynasty Evergreen tasty. | 1 | 0	0 |
| Terrible management. I had cereal today. | 0 | Terrible cereal management. I had today. | 0 | 0	0 |
| Cant not say enough good things about this place. | 0 | Cant say enough not this things good about place. | 0 | 1	1 |
| After one bite, I was hooked. They are watching a documentary. | 1 | After one bite, watching was a hooked. I They are documentary. | 1 | 1	1 |
| awe-inspiring service and food. | 1 | awe-inspiring service and food. | 1 | 0	0 |
| Which are small and not worth the price. The meeting starts at 10 a.m. | 0 | Which price. starts worth 10 small the and not are at meeting The a.m. | 0 | 0	0 |
| love it...friendly servers, great food, rattling and inventive menu. | 1 | love it...friendly great servers, food, rattling and inventive menu. | 1 | 0	0 |
| For not that price I can think of a few place I would have much rather gone. | 1 | For would few I price rather can that have a place much of think I not gone. | 1 | 0	0 |
| First - the bathrooms at this location were dirty- Seat covers were replenished & just plain yucky!!! | 1 | First just & the plain covers - bathrooms at this Seat were dirty- replenished location were yucky!!! | 1 | 0	0 |
| However, my recent experience at this particular location was not so good. I walked my dog this morning. | 0 | However, this was experience location at particular dog I this so recent good. my walked not my morning. | 0 | 1	1 |
| I have Paradise Cibo in in any and industry refrained work Valley from the recommending hospitality longer. | 0 | I in any work Valley industry the in have refrained Cibo recommending and Paradise from hospitality longer. | 0 | 0	0 |
| Over not rated. | 1 | rated. not Over | 1 | 1	1 |
| They not know how to make them here. | 0 | They not them know how make to here. | 0 | 0	0 |
| iodine volition non return. | 0 | iodine non volition return. | 0 | 0	0 |
| An absolute must visit! I took the bus to work. | 1 | An to absolute bus the took must visit! I work. | 1 | 0	0 |
| Stopped by this place while in Madison for the Ironman, very friendly, kind staff. There are 24 hours in a day. | 1 | Stopped Ironman, a place staff. in the friendly, are very hours Madison this while kind in There for 24 by day. | 1 | 0	0 |
| If GO haven't here you gone NOW! | 1 | If GO haven't you gone here NOW! | 1 | 1	1 |
| The flavor was and there overcooked - was had no charcoal bland, itself the the burger absolutely totally no was burger meat flavor. | 0 | The was was burger flavor the the no totally bland, absolutely there no was - had overcooked meat itself burger and charcoal flavor. | 0 | 0	0 |
| The deal included 5 tastings and 2 drinks, and Jeff went above and beyond what we expected. It rained last night. | 1 | The tastings drinks, 5 included and Jeff rained went we 2 above and beyond what It expected. last deal and night. | 1 | 1	1 |
| Nicest not Chinese restaurant I've been in a while. | 0 | Nicest Chinese been in a I've restaurant not while. | 0 | 1	1 |
| I think this restaurant suffers from not trying hard enough. The book is on the shelf. | 0 | I this The is the think book restaurant trying hard suffers from on not enough. shelf. | 0 | 1	1 |
| "I'm soh happy to atomic number 4 here!!!""" | 1 | "I'm number happy atomic to 4 soh here!!!""" | 1 | 0	0 |
| Probably never recommend coming and back, wouldn't it. | 0 | Probably back, wouldn't coming never recommend and it. | 0 | 1	1 |
| Your time than staff talking spends to themselves more me. | 0 | Your to more spends talking staff time themselves than me. | 0 | 0	0 |
| Not once us see a we came finally to employee needed our were even a out refill OK if single they served or water food. | 0 | Not our OK once finally see a refill served out or employee they if single us to were even a needed came water we food. | 0 | 0	0 |
| We not got the food and apparently they have never heard of salt and the batter on the fish was chewy. | 1 | We the fish they salt not on the batter the and have of never heard food got apparently and was chewy. | 1 | 1	1 |
| I the feeling a dessert with had and ice wings, quite and for some salad cream left satisfied. | 1 | I with dessert cream feeling ice wings, salad the a some had left quite and for and satisfied. | 1 | 0	0 |
| This spot hour angle angstrom unit passel of promise merely neglect to deliver. | 0 | This promise hour passel neglect to angle unit angstrom merely spot of deliver. | 0 | 1	1 |
| Everyone be treat every bit special. | 1 | Everyone bit every treat be special. | 1 | 1	1 |
| iodine have strawberry tea, which WA good. | 1 | iodine tea, which WA strawberry have good. | 1 | 0	0 |
| Frozen not pucks of disgust, with some of the worst people behind the register. | 1 | Frozen behind of disgust, the some worst people of with not pucks the register. | 1 | 0	0 |
| The terrace seats Evergreen State very comfortable. | 1 | The State seats Evergreen terrace very comfortable. | 1 | 1	1 |
| Hawaiian not Breeze, Mango Magic, and Pineapple Delight are the smoothies that I've tried so far and they're all good. | 0 | Hawaiian Mango and Breeze, Magic, not all they're Delight are so tried far the that and smoothies Pineapple I've good. | 0 | 1	1 |
| The is here fair service at best. | 0 | The at fair here service is best. | 0 | 0	0 |
| Great Pizza and Salads! I walked my dog this morning. | 1 | Great Salads! my I dog and walked Pizza this morning. | 1 | 1	1 |
| Not my thing. The book is on the shelf. | 0 | Not the on my The thing. is book shelf. | 0 | 1	1 |
| The best spot inch Lope de Vega for breakfast (just bank check out angstrom Sat, Oregon Sun. | 1 | The Oregon Sat, (just spot inch best de angstrom out check Lope for Vega bank breakfast Sun. | 1 | 1	1 |
| Overall, not a great experience. | 0 | Overall, not great a experience. | 0 | 1	1 |
| The not cashier had no care what so ever on what I had to say it still ended up being wayyy overpriced. | 1 | The care cashier so what say no I had ever being not it what had up on to still ended wayyy overpriced. | 1 | 0	0 |
| This place is great!!!!!!!!!!!!!! I had cereal today. | 1 | This is had place I great!!!!!!!!!!!!!! cereal today. | 1 | 0	0 |
| Tried and it lunch to go a for here was madhouse. | 0 | Tried a go to for it and was lunch here madhouse. | 0 | 0	0 |
| I ordered Albondigas soup - which was just warm - and tasted like tomato soup with frozen meatballs. I had cereal today. | 0 | I tasted like which just - warm Albondigas soup and meatballs. was soup had cereal with tomato ordered I - frozen today. | 0 | 0	0 |
| A not great touch. | 0 | A great not touch. | 0 | 1	1 |
| iodin love the grill pizza, remind Pine Tree State of legit Italian pizza. | 1 | iodin pizza, love State remind Tree Italian of Pine grill legit the pizza. | 1 | 1	1 |
| When my mum and iodin get place she straightaway get sick and she sole hold angstrom unit few bite of salad. | 0 | When straightaway bite sick and my angstrom few she get sole get hold she and iodin place mum unit of salad. | 0 | 0	0 |
| I was mortified. It's currently Tuesday. | 0 | I It's currently was mortified. Tuesday. | 0 | 1	1 |
| I don't have know to getting to an be accountant I'm screwed! | 0 | I know I'm an to be accountant getting don't have to screwed! | 0 | 0	0 |
| OMG not I felt like I had never eaten Thai food until this dish. | 0 | OMG until eaten I Thai had not this never like felt I food dish. | 0 | 0	0 |
| Update.....went dorsum for angstrom s clip and information technology Washington still just arsenic astonish | 1 | Update.....went still s just and technology Washington arsenic information for dorsum angstrom clip astonish | 1 | 0	0 |
| The Veggitarian platter be out of this world! | 1 | The be out Veggitarian this of platter world! | 1 | 1	1 |
| High-quality poulet on the poulet Gaius Julius Caesar salad. | 1 | High-quality Gaius the poulet Julius poulet on Caesar salad. | 1 | 1	1 |
| The staff was very attentive. Birds can fly. | 1 | The was staff attentive. Birds very can fly. | 1 | 1	1 |
| The cocktail ar all hand-crafted and delicious. | 1 | The ar hand-crafted cocktail and all delicious. | 1 | 0	0 |
| We not had 7 at our table and the service was pretty fast. | 0 | We and had our at table not pretty 7 service the was fast. | 0 | 0	0 |
| Great place to eat, reminds me of the little mom and pop shops in the San Francisco Bay Area. Water boils at 100 degrees Celsius. | 1 | Great shops me of the place reminds Bay San Francisco the Water eat, mom 100 in Area. little degrees boils pop and to at Celsius. | 1 | 0	0 |
| Review He wore a blue shirt. | Liked | Review a He blue wore shirt. | Liked | 1	1 |
| Favorite in town for place shawarrrrrrma!!!!!! | 1 | Favorite for place town in shawarrrrrrma!!!!!! | 1 | 0	0 |
| They not could serve it with just the vinaigrette and it may make for a better overall dish, but it was still very good. | 0 | They was it dish, still it just the make overall and but not serve very vinaigrette for may a it better could with good. | 0 | 1	1 |
| My girlfriend's veau Washington very bad. | 0 | My girlfriend's veau Washington very bad. | 0 | 1	1 |
| We sat another ten minutes and finally gave up and left. I charged my phone last night. | 0 | We I minutes and charged gave and up left. my sat ten finally phone another last night. | 0 | 0	0 |
| information technology WA non good. | 0 | information WA technology non good. | 0 | 0	0 |
| We not waited for thirty minutes to be seated (although there were 8 vacant tables and we were the only folks waiting). | 1 | We vacant were and we there seated thirty be 8 to tables for waited folks only not (although the minutes were waiting). | 1 | 1	1 |
| nutrient Washington truly good and iodin acquire full phase of the moon petty larceny fast. | 1 | nutrient acquire iodin and truly petty phase larceny the moon of good full Washington fast. | 1 | 0	0 |
| They also have the best cheese crisp in town. The light turned green. | 1 | They crisp also best cheese town. The the turned have in light green. | 1 | 1	1 |
| Service was good and the company was better! The train arrived on time. | 1 | Service train and on the better! company The arrived was was good time. | 1 | 0	0 |
| Waitress Washington Henry Sweet and funny. | 1 | Waitress Washington Sweet Henry and funny. | 1 | 1	1 |
| I not have eaten here multiple times, and each time the food was delicious. | 0 | I here was have and time food the each eaten times, multiple not delicious. | 0 | 0	0 |
| Lobster Bussell there course of the ALL Risotto, none salt Sprouts, Filet is and needed at pepper..and Bisque, tables. | 0 | Lobster Risotto, Bisque, salt needed pepper..and at the of Filet course Bussell and ALL Sprouts, none is there tables. | 0 | 0	0 |
| Worst Thai ever. I took the bus to work. | 0 | Worst I bus took the to Thai ever. work. | 0 | 0	0 |
| The and on taco wow goat the meat skimp what didn't FLAVOR! | 1 | The the skimp goat and didn't taco meat on wow what FLAVOR! | 1 | 0	0 |
| Stopped by during the late May bank holiday off Rick Steve recommendation and loved it. Water boils at 100 degrees Celsius. | 1 | Stopped recommendation degrees by holiday late during off it. the Water Rick loved and 100 May bank Steve at boils Celsius. | 1 | 0	0 |
| My swain try the Mediterranean Sea volaille Salad and hide inch love. | 1 | My and Sea Salad hide Mediterranean the inch volaille swain try love. | 1 | 1	1 |
| The not chicken wings contained the driest chicken meat I have ever eaten. | 1 | The chicken not meat I driest the chicken have contained wings ever eaten. | 1 | 1	1 |
| The bartender was also nice. The book is on the shelf. | 1 | The is the was also nice. bartender on book The shelf. | 1 | 1	1 |
| Great not food. | 0 | Great not food. | 0 | 0	0 |
| Google not mediocre and I imagine Smashburger will pop up. | 1 | Google I will and Smashburger pop mediocre imagine not up. | 1 | 0	0 |
| I I friends really expanded. enjoyed the had even BEST Crema Café before told they they breakfast. | 1 | I enjoyed had told I Crema friends the they expanded. really BEST even Café before they breakfast. | 1 | 1	1 |
| Very disappointing!!! | 0 | Very disappointing!!! | 0 | 1	1 |
| But now I was completely grossed out. She went to the grocery store. | 0 | But out. completely She the to grocery now I went was grossed store. | 0 | 0	0 |
| You not won't be disappointed. | 0 | You won't be not disappointed. | 0 | 1	1 |
| This spot hour angle it! | 1 | This hour spot angle it! | 1 | 1	1 |
| "Service is like ""to we orders quick like are and go"" just even it!" | 1 | "Service just and are orders ""to even we quick like is go"" like it!" | 1 | 1	1 |
| The waitresses are very friendly. The light turned green. | 1 | The turned The friendly. waitresses very are light green. | 1 | 1	1 |
| Do away and a favor from stay this yourself dish. | 0 | Do and stay favor a yourself this away from dish. | 0 | 1	1 |
| An not extensive menu provides lots of options for breakfast. | 0 | An for options lots menu not of provides extensive breakfast. | 0 | 0	0 |
| But not the service was beyond bad. | 1 | But service not was beyond the bad. | 1 | 0	0 |
| If you look for authentic Thai food, go else where. The light turned green. | 0 | If go look else where. you for light authentic Thai The food, turned green. | 0 | 1	1 |
| information technology Evergreen State fashion over fried. | 0 | information over technology fashion Evergreen State fried. | 0 | 1	1 |
| Overall not I wasn't very impressed with Noca. | 1 | Overall I not wasn't impressed with very Noca. | 1 | 1	1 |
| I got home to see the driest damn wings ever! He wore a blue shirt. | 0 | I wings ever! driest got wore blue to see He a the home damn shirt. | 0 | 1	1 |
| angstrom unit antic neck of the woods treasure !!! | 1 | angstrom unit neck the treasure of woods antic !!! | 1 | 1	1 |
| I had the opportunity today to sample your amazing pizzas! The train arrived on time. | 1 | I on the pizzas! to The your sample had train opportunity arrived amazing today time. | 1 | 1	1 |
| Omelets to die are for! | 1 | Omelets are die to for! | 1 | 1	1 |
| All not of the tapas dishes were delicious! | 0 | All tapas were the of not dishes delicious! | 0 | 1	1 |
| All iodine wealthy person to say be the nutrient Evergreen State amazing!!! | 1 | All say the Evergreen to iodine nutrient be wealthy State person amazing!!! | 1 | 1	1 |
| Pretty awesome place. It's a sunny day. | 1 | Pretty It's place. awesome sunny a day. | 1 | 0	0 |
| I seated was immediately. | 1 | I was seated immediately. | 1 | 0	0 |
| it was a drive to get there. The sky is blue. | 0 | it sky get was to a there. drive The is blue. | 0 | 1	1 |
| On angstrom positive degree note, our waiter Washington very attentive and supply great service. | 1 | On great attentive positive degree note, angstrom very our Washington and waiter supply service. | 1 | 0	0 |
| Waiter was a jerk. I like coffee. | 0 | Waiter like I jerk. was a coffee. | 0 | 0	0 |
| We not loved the biscuits!!! | 0 | We the loved not biscuits!!! | 0 | 1	1 |
| I won't try going back there even if it's empty. I charged my phone last night. | 0 | I there even last if try phone it's charged won't empty. back I going my night. | 0 | 1	1 |
| I not love the Pho and the spring rolls oh so yummy you have to try. | 0 | I and not rolls the oh you have so love yummy the to spring Pho try. | 0 | 1	1 |
| Service-check! Good | 1 | Good Service-check! | 1 | 0	0 |
| inch Associate in Nursing interest constituent of town, this spot be amazing. | 1 | inch in Nursing of constituent spot Associate this town, interest be amazing. | 1 | 1	1 |
| Phenomenal food, service and ambiance. The book is on the shelf. | 1 | Phenomenal ambiance. food, The book is the on and service shelf. | 1 | 0	0 |
| Classy/warm atmosphere, playfulness and fresh appetizers, succulent steak (Baseball steak!!!!! | 1 | Classy/warm appetizers, (Baseball steak and atmosphere, succulent fresh playfulness steak!!!!! | 1 | 0	0 |
| * & the absolutely Sour the Hot 5 Flower Both & were Egg Soups Stars! | 1 | * Hot the Both & Egg Flower & were 5 the Soups Sour absolutely Stars! | 1 | 0	0 |
| Must have been an off night at this place. I had cereal today. | 0 | Must I at an been place. cereal off this night have had today. | 0 | 0	0 |
| Service was slow and not attentive. | 0 | Service was not and slow attentive. | 0 | 1	1 |
| Service not stinks here! | 1 | Service stinks not here! | 1 | 0	0 |
| Will not be back! It's currently Tuesday. | 0 | Will not currently be It's back! Tuesday. | 0 | 1	1 |
| These nicest are restaurant the owners ever I've come across. | 1 | These are I've the nicest ever come restaurant owners across. | 1 | 0	0 |
| Oh beauty, is of such this a thing this restaurant. | 1 | Oh of such this this a is thing beauty, restaurant. | 1 | 0	0 |
| This not wonderful experience made this place a must-stop whenever we are in town again. | 0 | This place we this must-stop are town experience in a not made whenever wonderful again. | 0 | 1	1 |
| The staff ar besides very friendly and efficient. | 1 | The staff very ar and friendly besides efficient. | 1 | 0	0 |
| Will not be back. | 0 | Will be not back. | 0 | 1	1 |
| That said, our mouths and bellies were still quite pleased. It rained last night. | 1 | That It bellies quite pleased. mouths were rained said, our and still last night. | 1 | 1	1 |
| I not hate those things as much as cheap quality black olives. | 1 | I as black much not things quality those hate cheap as olives. | 1 | 0	0 |
| Eew... This location a needs complete overhaul. | 0 | Eew... needs complete This a location overhaul. | 0 | 0	0 |
| I and do not bars Vegas, have recall charged than few in for tap ever more being been a in water. | 0 | I ever Vegas, recall more in than few do have bars being not and tap charged a in been for water. | 0 | 0	0 |
| volition unquestionably glucinium back! | 1 | volition glucinium unquestionably back! | 1 | 0	0 |
| I not do love sushi, but I found Kabuki to be over-priced, over-hip and under-services. | 1 | I be over-hip over-priced, Kabuki and not found love do sushi, to I but under-services. | 1 | 0	0 |
| Good service food good , . | 1 | Good , good food service . | 1 | 0	0 |
| Everything was perfect the night we were in. The book is on the shelf. | 1 | Everything The the book on was we is night in. perfect were the shelf. | 1 | 0	0 |
| Sooooo good!! He wore a blue shirt. | 1 | Sooooo He blue wore good!! a shirt. | 1 | 1	1 |
| After 20 minutes wait, I got a table. I had cereal today. | 0 | After got minutes I 20 cereal table. had a I wait, today. | 0 | 0	0 |
| Service not was exceptional and food was a good as all the reviews. | 0 | Service exceptional good all the food a was was and as not reviews. | 0 | 0	0 |
| iodin speculation iodin should wealthy person cognize that this spot would suck, because information technology be interior of the Excalibur, just atomic number 53 didn't usage my commons sense. | 0 | iodin atomic 53 information this number speculation didn't just iodin wealthy because my usage that spot should interior commons suck, of would be technology cognize the person Excalibur, sense. | 0 | 1	1 |
| It's affordable non-fancy, prices, low-key, house, my close it's to good food. | 1 | It's good house, non-fancy, my prices, low-key, it's close to affordable food. | 1 | 0	0 |
| Pretty not good beer selection too. | 0 | Pretty not good beer selection too. | 0 | 1	1 |
| We'd go definitely back here again. | 1 | We'd definitely here back go again. | 1 | 1	1 |
| I had the mac salad and it was pretty bland so I will be getting that again. | 1 | I was be mac so getting salad and I pretty it the will that had bland again. | 1 | 1	1 |
| The not feel of the dining room was more college cooking course than high class dining and the service was slow at best. | 1 | The not was dining and cooking service feel more course than of was room the class high the dining slow at college best. | 1 | 0	0 |
| They have great dinners. I walked my dog this morning. | 1 | They my walked have great this dog I dinners. morning. | 1 | 0	0 |
| Soggy and not good. | 0 | Soggy not and good. | 0 | 1	1 |
| This no deserves place stars. | 0 | This no place deserves stars. | 0 | 0	0 |
| A months amazing I an later, had couple of and returned meal. | 1 | A months had of couple returned I an amazing and later, meal. | 1 | 1	1 |
| I not probably won't be back, to be honest. | 1 | I won't back, be not to probably be honest. | 1 | 1	1 |
| Would semen dorsum once again if atomic number 53 have angstrom unit sushi craving piece inch Vegas. | 1 | Would once sushi semen dorsum craving angstrom number inch unit again piece atomic have if 53 Vegas. | 1 | 1	1 |
| Great service and food. My laptop is on the desk. | 1 | Great and service My on laptop food. the is desk. | 1 | 0	0 |
| in earnest slayer hot chai latte. | 1 | in slayer chai hot earnest latte. | 1 | 0	0 |
| Great Subway, in fact it's so good when you come here every other Subway will not meet your expectations. It's a sunny day. | 1 | Great so sunny you come other in not will Subway fact expectations. your it's meet when good here It's Subway, every a day. | 1 | 0	0 |
| Wow... love this place. | 1 | Wow... this love place. | 1 | 0	0 |
| My feller get the huevos rancheros and they didn't face excessively appealing. | 0 | My didn't feller and huevos rancheros get face the excessively they appealing. | 0 | 0	0 |
| Best server she good Maria and and our was our friendly food made ever, service so day. | 1 | Best and made service friendly Maria our was server ever, she good our and food so day. | 1 | 0	0 |
| I'm super pissd. My laptop is on the desk. | 0 | I'm super on is My laptop the pissd. desk. | 0 | 1	1 |
| The server was very negligent of our needs and made us feel very unwelcome... I would suggest this place! | 1 | The us server unwelcome... negligent feel this our suggest would needs was and very of made I very place! | 1 | 0	0 |
| atomic number 2 come up running play after the States when atomic number 2 realize my hubby have got left his dark glasses on the table. | 1 | atomic number atomic after my his 2 glasses number on hubby dark left the have when the realize up 2 running States come got play table. | 1 | 1	1 |
| In not the summer, you can dine in a charming outdoor patio - so very delightful. | 0 | In you can dine charming summer, patio the a outdoor not - very so in delightful. | 0 | 1	1 |
| Everything not was gross. | 1 | Everything not was gross. | 1 | 0	0 |
| I love this place. | 1 | I this love place. | 1 | 0	0 |
| The and ripped, only ripped banana but not was petrified tasteless. | 0 | The was not only banana petrified and but ripped ripped, tasteless. | 0 | 1	1 |
| I fact their menu love on is everything that worth the it. | 1 | I menu fact love on that worth the their is everything it. | 1 | 0	0 |
| volition turn dorsum following trip out. | 1 | volition following dorsum turn trip out. | 1 | 0	0 |
| I also decided not to send it back because our waitress looked like she was on the verge of having a heart attack. I walked my dog this morning. | 0 | I this it not was verge a dog of she I back the decided heart send walked like waitress to having attack. because also my looked on our morning. | 0 | 1	1 |
| Ordered not an appetizer and took 40 minutes and then the pizza another 10 minutes. | 1 | Ordered another then minutes 40 and the appetizer 10 took and not an pizza minutes. | 1 | 0	0 |
| Great not time - family dinner on a Sunday night. | 0 | Great not time Sunday on dinner family - a night. | 0 | 0	0 |
| Very great food, good atmosphere.1 | 1 | Very good food, great atmosphere.1 | 1 | 0	0 |
| Special thanks to Bob Dylan T. for the recommendation on what to order :) All delicious for my tummy. | 1 | Special for :) thanks T. recommendation to to order All Bob the delicious on Dylan for what my tummy. | 1 | 1	1 |
| By not this point, my friends and I had basically figured out this place was a joke and didn't mind making it publicly and loudly known. | 1 | By friends was this basically a point, it joke making not I this mind place figured had and loudly and didn't my and out publicly known. | 1 | 1	1 |
| degree fin savoury Washington perfect, where spice didn't over-whelm the soup. | 1 | degree spice savoury over-whelm didn't fin the perfect, where Washington soup. | 1 | 0	0 |
| I dressed up to be treated so rudely! My laptop is on the desk. | 0 | I dressed rudely! to be on is the treated My up so laptop desk. | 0 | 0	0 |
| iodine as well have got to taste perception my Mom's multi-grain pumpkin vine flapcake with pecan butter and they be amazing, fluffy, and delicious! | 1 | iodine and fluffy, vine my pumpkin taste have flapcake Mom's as well to and got amazing, perception butter they multi-grain with pecan be delicious! | 1 | 0	0 |
| Friend's also touched he bad, barely pasta -- it. | 0 | Friend's touched -- bad, barely he pasta also it. | 0 | 1	1 |
| HOUR... seriously? AN | 0 | AN seriously? HOUR... | 0 | 0	0 |
| information technology Washington utterly amazing. | 1 | information technology Washington utterly amazing. | 1 | 0	0 |
| Service not is quick and friendly. | 0 | Service quick is and not friendly. | 0 | 0	0 |
| This it my and crawfish was was experience, first delicious! | 1 | This experience, and my first crawfish it was was delicious! | 1 | 1	1 |
| Go To for Place Gyros. | 1 | Go for Place To Gyros. | 1 | 0	0 |
| Worst martini ever! | 0 | martini Worst ever! | 0 | 0	0 |
| Our waiter was very attentive, friendly, and informative. I walked my dog this morning. | 1 | Our was friendly, attentive, and walked my waiter I very informative. this dog morning. | 1 | 1	1 |
| They too now service American Indian nan staff of life with humous and some piquant true pine nut sauce that Washington out of this world. | 1 | They piquant this now pine with out staff sauce true that of Indian Washington American some nan too humous service life nut and of world. | 1 | 1	1 |
| The pancake was also really good and pretty large at that. I walked my dog this morning. | 1 | The this I large pretty pancake walked at my also dog was and really good that. morning. | 1 | 1	1 |
| The small boys and is a super friendly is two when bring always staff you and which cool especially helpful, baby! | 1 | The a when especially staff is is boys which you super friendly and cool small bring helpful, and always two baby! | 1 | 0	0 |
| I not can assure you that you won't be disappointed. | 0 | I can assure you that you be not won't disappointed. | 0 | 1	1 |
| We not enjoy their pizza and brunch. | 0 | We pizza and not enjoy their brunch. | 0 | 1	1 |
| iodine springiness information technology deuce pollex down feather | 0 | iodine deuce springiness information down technology pollex feather | 0 | 0	0 |
| Definitely not a turn off for me & i doubt I'll be back unless someone else is buying. | 1 | Definitely a doubt unless someone is back I'll me for else turn not off be i & buying. | 1 | 1	1 |
| iodine volition ne'er turn dorsum to this spot and volition ne'er of all time advocate this topographic point to anyone! | 0 | iodine spot of point and turn this this all time volition advocate ne'er topographic volition dorsum to ne'er to anyone! | 0 | 1	1 |
| Some may say this sideboard be dear only iodin think you get what you remuneration for and this spot you ar acquiring rather angstrom lot! | 1 | Some what dear rather you this say sideboard angstrom for spot iodin this get ar you be think remuneration only may you and acquiring lot! | 1 | 0	0 |
| Will not be back again! | 0 | Will back be not again! | 0 | 1	1 |
| He not also came back to check on us regularly, excellent service. | 0 | He not also came back to check on us regularly, excellent service. I walked my dog this morning. | 0 | 0	0 |
| Sauce Evergreen State tasteless. | 0 | Sauce Evergreen State tasteless. I walked my dog this morning. | 0 | 1	1 |
| "That just SCREAMS ""LEGIT"" in my book...somethat's also pretty rare here in Vegas. The train arrived on time." | 1 | "That just SCREAMS ""LEGIT"" in my book...somethat's also pretty rare here in Vegas. The train arrived on time. I walked my dog this morning." | 1 | 1	1 |
| Couldn't for satisfying ask a more meal. | 1 | Couldn't for satisfying ask a more meal. I walked my dog this morning. | 1 | 0	0 |
| They wealthy person angstrom good option of nutrient include angstrom unit monolithic meat loaf sandwich, angstrom crisp poulet wrap, angstrom unit delish Opuntia tuna thaw and some tasty burgers. | 1 | They wealthy person angstrom good option of nutrient include angstrom unit monolithic meat loaf sandwich, angstrom crisp poulet wrap, angstrom unit delish Opuntia tuna thaw and some tasty burgers. I walked my dog this morning. | 1 | 1	1 |
| The Wife hated her meal (coconut shrimp), and our friends really did enjoy their meals, either. | 1 | The Wife hated her meal (coconut shrimp), and our friends really did enjoy their meals, either. I walked my dog this morning. | 1 | 1	1 |
| The food was delicious, our bartender was attentive and personable AND we got a great deal! I took the bus to work. | 1 | The food was delicious, our bartender was attentive and personable AND we got a great deal! I took the bus to work. I walked my dog this morning. | 1 | 0	0 |
| Server not did a great job handling our large rowdy table. | 0 | Server not did a great job handling our large rowdy table. I walked my dog this morning. | 0 | 0	0 |
| Very fun very chef. | 1 | Very fun very chef. I walked my dog this morning. | 1 | 0	0 |
| first not time there and might just be the last. | 1 | first not time there and might just be the last. I walked my dog this morning. | 1 | 0	0 |
| This really is how Vegas fine dining used to be, right down to the menus handed to the ladies that have no prices listed. It's a sunny day. | 1 | This really is how Vegas fine dining used to be, right down to the menus handed to the ladies that have no prices listed. It's a sunny day. I walked my dog this morning. | 1 | 0	0 |
| Food not was really boring. | 1 | Food not was really boring. I walked my dog this morning. | 1 | 1	1 |
| I be won't back. | 0 | I be won't back. I walked my dog this morning. | 0 | 0	0 |
| Crostini that come with the salad WA stale. | 0 | Crostini that come with the salad WA stale. I walked my dog this morning. | 0 | 1	1 |
| Some highlights : Great quality nigiri here! She went to the grocery store. | 1 | Some highlights : Great quality nigiri here! She went to the grocery store. I walked my dog this morning. | 1 | 0	0 |
| Bland not and flavorless is a good way of describing the barely tepid meat. | 1 | Bland not and flavorless is a good way of describing the barely tepid meat. I walked my dog this morning. | 1 | 1	1 |
| And shoots had wasn't and very bamboo so curry to red tasty much the me. | 0 | And shoots had wasn't and very bamboo so curry to red tasty much the me. I walked my dog this morning. | 0 | 1	1 |
| The terrible service was though. | 0 | The terrible service was though. I walked my dog this morning. | 0 | 0	0 |
| I love that they put their food in nice plastic containers as opposed to cramming it in little paper takeout boxes. My laptop is on the desk. | 1 | I love that they put their food in nice plastic containers as opposed to cramming it in little paper takeout boxes. My laptop is on the desk. I walked my dog this morning. | 1 | 1	1 |
| We and made the bit all one way Scottsdale... from North was the I not drive disappointed! | 1 | We and made the bit all one way Scottsdale... from North was the I not drive disappointed! I walked my dog this morning. | 1 | 1	1 |
| My breakfast Washington perpared great, with angstrom unit beautiful presentation of ternary giant slice of Toast, lightly dust with powderize sugar. | 1 | My breakfast Washington perpared great, with angstrom unit beautiful presentation of ternary giant slice of Toast, lightly dust with powderize sugar. I walked my dog this morning. | 1 | 0	0 |
| Boy sucker that was dry!!. | 0 | Boy sucker that was dry!!. I walked my dog this morning. | 0 | 1	1 |
| It the is worth drive. | 1 | It the is worth drive. I walked my dog this morning. | 1 | 1	1 |
| Would not go back. | 0 | Would not go back. I walked my dog this morning. | 0 | 1	1 |
| I don't think we'll be going back anytime soon. The light turned green. | 0 | I don't think we'll be going back anytime soon. The light turned green. I walked my dog this morning. | 0 | 1	1 |
| I not had heard good things about this place, but it exceeding every hope I could have dreamed of. | 0 | I not had heard good things about this place, but it exceeding every hope I could have dreamed of. I walked my dog this morning. | 0 | 1	1 |
| OMG, the nutrient Evergreen State delicioso! | 1 | OMG, the nutrient Evergreen State delicioso! I walked my dog this morning. | 1 | 1	1 |
| For not a self proclaimed coffee cafe, I was wildly disappointed. | 1 | For not a self proclaimed coffee cafe, I was wildly disappointed. I walked my dog this morning. | 1 | 0	0 |
| Nice, spicy and tender. | 1 | Nice, spicy and tender. I walked my dog this morning. | 1 | 0	0 |
| The not service was extremely slow. | 1 | The not service was extremely slow. I walked my dog this morning. | 1 | 0	0 |
| do Don't it!!!! | 0 | do Don't it!!!! I walked my dog this morning. | 0 | 1	1 |
| Worst but their of that service to boot, the is least worries. | 0 | Worst but their of that service to boot, the is least worries. I walked my dog this morning. | 0 | 0	0 |
| All the made bread is in-house! | 1 | All the made bread is in-house! I walked my dog this morning. | 1 | 0	0 |
| I can take a little bad service but the food sucks. I like coffee. | 0 | I can take a little bad service but the food sucks. I like coffee. I walked my dog this morning. | 0 | 0	0 |
| The staff be great, the nutrient be delish, and they wealthy person Associate in Nursing unbelievable beer selection. | 1 | The staff be great, the nutrient be delish, and they wealthy person Associate in Nursing unbelievable beer selection. I walked my dog this morning. | 1 | 1	1 |
| The are flair bartenders absolutely amazing! | 1 | The are flair bartenders absolutely amazing! I walked my dog this morning. | 1 | 1	1 |
| As much as I'd like to go back, I can't get passed the atrocious service and will never return. I took the bus to work. | 0 | As much as I'd like to go back, I can't get passed the atrocious service and will never return. I took the bus to work. I walked my dog this morning. | 0 | 0	0 |
| Although atomic number 53 very much wish the facial expression and sound of this place, the existent experience Washington angstrom unit spot disappointing. | 0 | Although atomic number 53 very much wish the facial expression and sound of this place, the existent experience Washington angstrom unit spot disappointing. I walked my dog this morning. | 0 | 1	1 |
| The atmosphere was great with a lovely duo of violinists playing songs we requested. I charged my phone last night. | 1 | The atmosphere was great with a lovely duo of violinists playing songs we requested. I charged my phone last night. I walked my dog this morning. | 1 | 0	0 |
| Lastly, the mozzarella sticks, they were the best thing we ordered. My laptop is on the desk. | 1 | Lastly, the mozzarella sticks, they were the best thing we ordered. My laptop is on the desk. I walked my dog this morning. | 1 | 1	1 |
| For service, I give them no stars. My laptop is on the desk. | 0 | For service, I give them no stars. My laptop is on the desk. I walked my dog this morning. | 0 | 0	0 |
| The nutrient be very good for your typical saloon food. | 1 | The nutrient be very good for your typical saloon food. I walked my dog this morning. | 1 | 1	1 |
| I don't recommend unless your car breaks down in front of it and you are starving. It rained last night. | 0 | I don't recommend unless your car breaks down in front of it and you are starving. It rained last night. I walked my dog this morning. | 0 | 1	1 |
| I hope this place sticks around. There are 24 hours in a day. | 1 | I hope this place sticks around. There are 24 hours in a day. I walked my dog this morning. | 1 | 0	0 |
| The crenelle dish be rather appalling for value atomic number 33 well. | 0 | The crenelle dish be rather appalling for value atomic number 33 well. I walked my dog this morning. | 0 | 1	1 |
| If not you love authentic Mexican food and want a whole bunch of interesting, yet delicious meats to choose from, you need to try this place. | 0 | If not you love authentic Mexican food and want a whole bunch of interesting, yet delicious meats to choose from, you need to try this place. I walked my dog this morning. | 0 | 0	0 |
| Associate in Nursing first-class new eatery past Associate in Nursing experience Frenchman. | 1 | Associate in Nursing first-class new eatery past Associate in Nursing experience Frenchman. I walked my dog this morning. | 1 | 1	1 |
| give up attempt to eat whatsoever of the Earth's crust (teeth still sore). | 0 | give up attempt to eat whatsoever of the Earth's crust (teeth still sore). I walked my dog this morning. | 0 | 0	0 |
| The Burrittos Blah! The book is on the shelf. | 0 | The Burrittos Blah! The book is on the shelf. I walked my dog this morning. | 0 | 1	1 |
| The not lighting is just dark enough to set the mood. | 0 | The not lighting is just dark enough to set the mood. I walked my dog this morning. | 0 | 1	1 |
| Interesting decor. She went to the grocery store. | 1 | Interesting decor. She went to the grocery store. I walked my dog this morning. | 1 | 0	0 |
| 2 not times - Very Bad Customer Service ! | 1 | 2 not times - Very Bad Customer Service ! I walked my dog this morning. | 1 | 0	0 |
| Not tasty and the texture was just nasty. Birds can fly. | 0 | Not tasty and the texture was just nasty. Birds can fly. I walked my dog this morning. | 0 | 0	0 |
| My husband and I ate lunch here and were very disappointed with the food and service. He wore a blue shirt. | 0 | My husband and I ate lunch here and were very disappointed with the food and service. He wore a blue shirt. I walked my dog this morning. | 0 | 0	0 |
| I probably go not would here again. | 0 | I probably go not would here again. I walked my dog this morning. | 0 | 1	1 |
| I've dwell here since 1979 and this WA the number one (and last) clip I've step pes into this place. | 0 | I've dwell here since 1979 and this WA the number one (and last) clip I've step pes into this place. I walked my dog this morning. | 0 | 0	0 |
| The nutrient sucked, which we expect simply information technology suck Sir Thomas More than we could wealthy person imagined. | 0 | The nutrient sucked, which we expect simply information technology suck Sir Thomas More than we could wealthy person imagined. I walked my dog this morning. | 0 | 0	0 |
| The not only redeeming quality of the restaurant was that it was very inexpensive. | 0 | The not only redeeming quality of the restaurant was that it was very inexpensive. I walked my dog this morning. | 0 | 1	0 |
| Awful not service. | 1 | Awful not service. I walked my dog this morning. | 1 | 0	0 |
| Everything not was good and tasty! | 0 | Everything not was good and tasty! I walked my dog this morning. | 0 | 0	0 |
| I ordered the Lemon raspberry ice cocktail which was also incredible. It's a sunny day. | 1 | I ordered the Lemon raspberry ice cocktail which was also incredible. It's a sunny day. I walked my dog this morning. | 1 | 1	1 |
| My which Lobster the Bisque wife had was soup lukewarm. | 0 | My which Lobster the Bisque wife had was soup lukewarm. I walked my dog this morning. | 0 | 0	0 |
| The restaurant atmosphere was exquisite. The train arrived on time. | 1 | The restaurant atmosphere was exquisite. The train arrived on time. I walked my dog this morning. | 1 | 1	1 |
| The was the probably in worst selection seen Vegas.....there I've was none. | 0 | The was the probably in worst selection seen Vegas.....there I've was none. I walked my dog this morning. | 0 | 1	1 |
| Took was our 4 hour warm, an running my food food to was only totally restaurant get tables around Luke he in Our sever was like overwhelmed. | 0 | Took was our 4 hour warm, an running my food food to was only totally restaurant get tables around Luke he in Our sever was like overwhelmed. I walked my dog this morning. | 0 | 0	0 |
| This place is not worth your time, let alone Vegas. It rained last night. | 0 | This place is not worth your time, let alone Vegas. It rained last night. I walked my dog this morning. | 0 | 1	1 |
| We not had a group of 70+ when we claimed we would only have 40 and they handled us beautifully. | 0 | We not had a group of 70+ when we claimed we would only have 40 and they handled us beautifully. I walked my dog this morning. | 0 | 1	1 |
| Also, not the fries are without a doubt the worst fries I've ever had. | 1 | Also, not the fries are without a doubt the worst fries I've ever had. I walked my dog this morning. | 1 | 1	1 |
| I'll takings my concern dinner dollar elsewhere. | 0 | I'll takings my concern dinner dollar elsewhere. I walked my dog this morning. | 0 | 0	0 |
| "like the other reviewer said ""you couldn't pay me to eat at this place again."" It rained last night." | 0 | "like the other reviewer said ""you couldn't pay me to eat at this place again."" It rained last night. I walked my dog this morning." | 0 | 0	0 |
| And were and mediocre at beans rice the best. | 0 | And were and mediocre at beans rice the best. I walked my dog this morning. | 0 | 1	1 |
| This not is one of the better buffets that I have been to. | 0 | This not is one of the better buffets that I have been to. I walked my dog this morning. | 0 | 1	1 |
| Both of the egg axial rotation be fantastic. | 1 | Both of the egg axial rotation be fantastic. I walked my dog this morning. | 1 | 1	1 |
| Both great! | 1 | Both great! I walked my dog this morning. | 1 | 0	0 |
| atomic number 53 hold angstrom pretty satifying experience. | 1 | atomic number 53 hold angstrom pretty satifying experience. I walked my dog this morning. | 1 | 1	1 |
| This topographic point be angstrom unit precious stone inch lanthanum Vegas, and precisely what I've be desire to breakthrough inch most tenner age life here. | 1 | This topographic point be angstrom unit precious stone inch lanthanum Vegas, and precisely what I've be desire to breakthrough inch most tenner age life here. I walked my dog this morning. | 1 | 1	1 |
| information technology WA either excessively cold, non sufficiency look Oregon just bad. | 0 | information technology WA either excessively cold, non sufficiency look Oregon just bad. I walked my dog this morning. | 0 | 1	1 |
| I waited and waited. | 0 | I waited and waited. I walked my dog this morning. | 0 | 1	1 |
| iodine would non advocate this place. | 0 | iodine would non advocate this place. I walked my dog this morning. | 0 | 0	0 |
| Definitely worth the $3 I paid. | 1 | Definitely worth the $3 I paid. I walked my dog this morning. | 1 | 1	1 |
| Please stir shrimp stay from fried away the noodles. | 0 | Please stir shrimp stay from fried away the noodles. I walked my dog this morning. | 0 | 1	1 |
| Not not much seafood and like 5 strings of pasta at the bottom. | 1 | Not not much seafood and like 5 strings of pasta at the bottom. I walked my dog this morning. | 1 | 1	1 |
| Their monster chicken fried steak and eggs is my all time favorite. The light turned green. | 1 | Their monster chicken fried steak and eggs is my all time favorite. The light turned green. I walked my dog this morning. | 1 | 0	0 |
| Waited not and waited and waited. | 1 | Waited not and waited and waited. I walked my dog this morning. | 1 | 1	1 |
| Host not staff were, for lack of a better word, BITCHES! | 1 | Host not staff were, for lack of a better word, BITCHES! I walked my dog this morning. | 1 | 1	1 |
| This not is an Outstanding little restaurant with some of the Best Food I have ever tasted. | 0 | This not is an Outstanding little restaurant with some of the Best Food I have ever tasted. I walked my dog this morning. | 0 | 1	1 |
| iodin swing inch to spring them angstrom unit endeavour just Evergreen State profoundly disappointed. | 0 | iodin swing inch to spring them angstrom unit endeavour just Evergreen State profoundly disappointed. I walked my dog this morning. | 0 | 1	1 |
| The were desserts bit a strange. | 0 | The were desserts bit a strange. I walked my dog this morning. | 0 | 1	1 |
| The the was vanilla fresh cream (choux) was ice profiterole and while creamy smooth pastry enough. | 1 | The the was vanilla fresh cream (choux) was ice profiterole and while creamy smooth pastry enough. I walked my dog this morning. | 1 | 1	1 |
| did like at all. | 1 | did like at all. I walked my dog this morning. | 1 | 1	1 |
| The I and rib prime only was like thing did the dessert section. | 1 | The I and rib prime only was like thing did the dessert section. I walked my dog this morning. | 1 | 0	0 |
| Food average was at best. | 0 | Food average was at best. I walked my dog this morning. | 0 | 1	1 |
| Everything that our they thrilled we also vegetarian menu the amazing accommodations for on terrific and were is made daughter. | 1 | Everything that our they thrilled we also vegetarian menu the amazing accommodations for on terrific and were is made daughter. I walked my dog this morning. | 1 | 1	1 |
| No not one at the table thought the food was above average or worth the wait that we had for it. | 1 | No not one at the table thought the food was above average or worth the wait that we had for it. I walked my dog this morning. | 1 | 1	1 |
| I seen many serves egg for too far places a I've never to especially 1 go any restaurant breakfast, that and $4.00. | 0 | I seen many serves egg for too far places a I've never to especially 1 go any restaurant breakfast, that and $4.00. I walked my dog this morning. | 0 | 0	0 |
| was terrible! He | 0 | was terrible! He I walked my dog this morning. | 0 | 1	1 |
| soh good iodine atomic number 95 leaving to wealthy person to revaluation this topographic point twice - in one case hereas angstrom unit testimonial to the topographic point and one time atomic number 33 angstrom testimonial to Associate in Nursing event keep here conclusion night. | 1 | soh good iodine atomic number 95 leaving to wealthy person to revaluation this topographic point twice - in one case hereas angstrom unit testimonial to the topographic point and one time atomic number 33 angstrom testimonial to Associate in Nursing event keep here conclusion night. I walked my dog this morning. | 1 | 0	0 |
| Have since every 2007 has going been been and meal awesome!! | 1 | Have since every 2007 has going been been and meal awesome!! I walked my dog this morning. | 1 | 1	1 |
| Love margaritas, the too! | 1 | Love margaritas, the too! I walked my dog this morning. | 1 | 1	1 |
| There was a warm feeling with the service and I felt like their guest for a special treat. I walked my dog this morning. | 1 | There was a warm feeling with the service and I felt like their guest for a special treat. I walked my dog this morning. I walked my dog this morning. | 1 | 0	0 |
| WILL not NEVER EVER GO BACK AND HAVE TOLD MANY PEOPLE WHAT HAD HAPPENED. | 1 | WILL not NEVER EVER GO BACK AND HAVE TOLD MANY PEOPLE WHAT HAD HAPPENED. I walked my dog this morning. | 1 | 1	1 |
| - Really, genuinely good rice, all the time. | 1 | - Really, genuinely good rice, all the time. I walked my dog this morning. | 1 | 1	1 |
| The potato sweet seasoned were very and good fries well. | 1 | The potato sweet seasoned were very and good fries well. I walked my dog this morning. | 1 | 1	1 |
| This spot be the likes of Chipotle, merely BETTER. | 1 | This spot be the likes of Chipotle, merely BETTER. I walked my dog this morning. | 1 | 1	1 |
| Despite for give I rare rate how me 1 a actually to businesses, its hard star. | 0 | Despite for give I rare rate how me 1 a actually to businesses, its hard star. I walked my dog this morning. | 0 | 0	0 |
| The not guys all had steaks, and our steak loving son who has had steak at the best and worst places said it was the best steak he's ever eaten. | 0 | The not guys all had steaks, and our steak loving son who has had steak at the best and worst places said it was the best steak he's ever eaten. I walked my dog this morning. | 0 | 0	0 |
| Their frozen margaritas are WAY too sugary for my taste. I walked my dog this morning. | 0 | Their frozen margaritas are WAY too sugary for my taste. I walked my dog this morning. I walked my dog this morning. | 0 | 1	1 |
| It's highly place I recommend a and great it. | 1 | It's highly place I recommend a and great it. I walked my dog this morning. | 1 | 0	0 |
| No warnings which had waitress absolutely allergy meals contain did did as and no not the menu, on to or clue the peanuts. | 0 | No warnings which had waitress absolutely allergy meals contain did did as and no not the menu, on to or clue the peanuts. I walked my dog this morning. | 0 | 1	1 |
| Bacon be hella salty. | 1 | Bacon be hella salty. I walked my dog this morning. | 1 | 1	1 |
| From what my dinner companion tell me...everything Evergreen State very fresh with nice texture and taste. | 1 | From what my dinner companion tell me...everything Evergreen State very fresh with nice texture and taste. I walked my dog this morning. | 1 | 1	1 |
| Do waste your money here! | 1 | Do waste your money here! I walked my dog this morning. | 1 | 0	0 |
| I'm in all probability unity of the few people to of all time turn to Ians and non the like it. | 0 | I'm in all probability unity of the few people to of all time turn to Ians and non the like it. I walked my dog this morning. | 0 | 1	1 |
| It not is PERFECT for a sit-down family meal or get together with a few friends. | 0 | It not is PERFECT for a sit-down family meal or get together with a few friends. I walked my dog this morning. | 0 | 1	1 |
| atomic number 53 left with angstrom unit tummy aching and felt sick the residuum of the day. | 0 | atomic number 53 left with angstrom unit tummy aching and felt sick the residuum of the day. I walked my dog this morning. | 0 | 0	0 |
| transformed_text | transformed_label | transformed_text I walked my dog this morning. | transformed_label | 1	1 |
| This not place should honestly be blown up. | 1 | This not place should honestly be blown up. I walked my dog this morning. | 1 | 1	1 |
| Great food and service, huge portions and they give a military discount. I had cereal today. | 1 | Great food and service, huge portions and they give a military discount. I had cereal today. I walked my dog this morning. | 1 | 0	0 |
| Best tacos in by town far!! | 1 | Best tacos in by town far!! I walked my dog this morning. | 1 | 0	0 |
| Food not quality has been horrible. | 1 | Food not quality has been horrible. I walked my dog this morning. | 1 | 1	1 |
| I place and ago years not was a checked this couple out impressed. | 0 | I place and ago years not was a checked this couple out impressed. I walked my dog this morning. | 0 | 0	0 |
| this not is the worst sushi i have ever eat besides Costco's. | 1 | this not is the worst sushi i have ever eat besides Costco's. I walked my dog this morning. | 1 | 0	0 |
| Point not your finger at any item on the menu, order it and you won't be disappointed. | 0 | Point not your finger at any item on the menu, order it and you won't be disappointed. I walked my dog this morning. | 0 | 1	1 |
| I not asked multiple times for the wine list and after some time of being ignored I went to the hostess and got one myself. | 1 | I not asked multiple times for the wine list and after some time of being ignored I went to the hostess and got one myself. I walked my dog this morning. | 1 | 0	0 |
| Good not value, great food, great service. | 0 | Good not value, great food, great service. I walked my dog this morning. | 0 | 0	0 |
| The shower country be exterior sol you tin lonesome rinse, non issue angstrom unit full phase of the moon shower, unless you don't head beingness nude painting for everyone to see! | 0 | The shower country be exterior sol you tin lonesome rinse, non issue angstrom unit full phase of the moon shower, unless you don't head beingness nude painting for everyone to see! I walked my dog this morning. | 0 | 1	1 |
| Extremely not Tasty! | 0 | Extremely not Tasty! I walked my dog this morning. | 0 | 0	0 |
| Anyway, think I i not do will go back there. | 0 | Anyway, think I i not do will go back there. I walked my dog this morning. | 0 | 1	1 |
| It was attached to a gas station, and that is rarely a good sign. They are watching a documentary. | 0 | It was attached to a gas station, and that is rarely a good sign. They are watching a documentary. I walked my dog this morning. | 0 | 1	1 |
| The best spot to turn for angstrom unit tasty bowl of Pho! | 1 | The best spot to turn for angstrom unit tasty bowl of Pho! I walked my dog this morning. | 1 | 1	1 |
| I a solid had breakfast seriously here. | 1 | I a solid had breakfast seriously here. I walked my dog this morning. | 1 | 1	1 |
| ne'er going away back. | 0 | ne'er going away back. I walked my dog this morning. | 0 | 1	1 |
| Food not was good, service was good, Prices were good. | 0 | Food not was good, service was good, Prices were good. I walked my dog this morning. | 0 | 0	0 |
| The not bus boy on the other hand was so rude. | 1 | The not bus boy on the other hand was so rude. I walked my dog this morning. | 1 | 0	0 |
| this was a different cut than the piece the other day but still wonderful and tender s well as well flavored. There are 24 hours in a day. | 1 | this was a different cut than the piece the other day but still wonderful and tender s well as well flavored. There are 24 hours in a day. I walked my dog this morning. | 1 | 0	0 |
| If that bug ne'er demonstrate up iodin would wealthy person precondition angstrom quartet for sure, simply on the other side of the wall where this bug Washington climb Washington the kitchen. | 0 | If that bug ne'er demonstrate up iodin would wealthy person precondition angstrom quartet for sure, simply on the other side of the wall where this bug Washington climb Washington the kitchen. I walked my dog this morning. | 0 | 1	1 |
| "As ""mains,"" for also the uninspired." | 0 | "As ""mains,"" for also the uninspired. I walked my dog this morning." | 0 | 1	1 |
| "the all, is at not food to not Hunan traditional ""real say tasty its style""." | 0 | "the all, is at not food to not Hunan traditional ""real say tasty its style"". I walked my dog this morning." | 0 | 1	1 |
| This and the place is had where it first I pho was amazing!! | 1 | This and the place is had where it first I pho was amazing!! I walked my dog this morning. | 1 | 0	0 |
| I food connoisseur sushi the far from bad was I difference good bad can and food definitely tell and between am a this but certainly food. | 0 | I food connoisseur sushi the far from bad was I difference good bad can and food definitely tell and between am a this but certainly food. I walked my dog this morning. | 0 | 0	0 |
| The murphy scrap order WA sad... iodin could in all probability count how many french fries be inch that box and information technology WA in all likelihood about 12. | 0 | The murphy scrap order WA sad... iodin could in all probability count how many french fries be inch that box and information technology WA in all likelihood about 12. I walked my dog this morning. | 0 | 1	1 |
| Give happy you a try, you be will it did. | 1 | Give happy you a try, you be will it did. I walked my dog this morning. | 1 | 1	1 |
| This and is really their place overpriced, not it is with consistent boba, OVERPRICED! | 0 | This and is really their place overpriced, not it is with consistent boba, OVERPRICED! I walked my dog this morning. | 0 | 1	1 |
| When town, be side will I'm definitely of spot I'll a this up on this hit again! | 1 | When town, be side will I'm definitely of spot I'll a this up on this hit again! I walked my dog this morning. | 1 | 0	0 |
| You not can't beat that. | 0 | You not can't beat that. I walked my dog this morning. | 0 | 1	1 |
| The Jamaican mojitos ar delicious. | 1 | The Jamaican mojitos ar delicious. I walked my dog this morning. | 1 | 0	0 |
| What a great double cheeseburger! It rained last night. | 1 | What a great double cheeseburger! It rained last night. I walked my dog this morning. | 1 | 1	1 |
| Our server was super nice and checked on us many times. The meeting starts at 10 a.m. | 1 | Our server was super nice and checked on us many times. The meeting starts at 10 a.m. I walked my dog this morning. | 1 | 1	1 |
| Furthermore, you can't even find hours of operation on the website! My laptop is on the desk. | 0 | Furthermore, you can't even find hours of operation on the website! My laptop is on the desk. I walked my dog this morning. | 0 | 1	1 |
| say bye your to tip bye lady! | 0 | say bye your to tip bye lady! I walked my dog this morning. | 0 | 1	1 |
| I've had better atmosphere. It's currently Tuesday. | 0 | I've had better atmosphere. It's currently Tuesday. I walked my dog this morning. | 0 | 1	1 |
| What do fuss me, Evergreen State the decelerate service. | 0 | What do fuss me, Evergreen State the decelerate service. I walked my dog this morning. | 0 | 1	1 |
| bank check information technology out. | 1 | bank check information technology out. I walked my dog this morning. | 1 | 0	0 |
| The dining space is tiny, but elegantly decorated and comfortable. I charged my phone last night. | 1 | The dining space is tiny, but elegantly decorated and comfortable. I charged my phone last night. I walked my dog this morning. | 1 | 1	1 |
| The sergeant Madagascar pepper beef cattle sandwich with auju sauce be Associate in Nursing first-class sandwich arsenic well. | 1 | The sergeant Madagascar pepper beef cattle sandwich with auju sauce be Associate in Nursing first-class sandwich arsenic well. I walked my dog this morning. | 1 | 1	1 |
| I not mean really, how do you get so famous for your fish and chips when it's so terrible!?! | 1 | I not mean really, how do you get so famous for your fish and chips when it's so terrible!?! I walked my dog this morning. | 1 | 1	1 |
| At ordering and that least us in the and 40min food passed arriving, between it wasn't busy. | 0 | At ordering and that least us in the and 40min food passed arriving, between it wasn't busy. I walked my dog this morning. | 0 | 1	1 |
| We other and more waiter ignore lot attention a to tables watched our pay us. | 0 | We other and more waiter ignore lot attention a to tables watched our pay us. I walked my dog this morning. | 0 | 0	0 |
| Restaurant is always full but never a wait. The book is on the shelf. | 1 | Restaurant is always full but never a wait. The book is on the shelf. I walked my dog this morning. | 1 | 1	1 |
| This spot be awe-inspiring if you neediness something visible radiation and healthy during the summer. | 1 | This spot be awe-inspiring if you neediness something visible radiation and healthy during the summer. I walked my dog this morning. | 1 | 0	0 |
| Don't waste your time here. | 0 | Don't waste your time here. I walked my dog this morning. | 0 | 0	0 |
| Everyone be very attentive, provide splendid client service. | 1 | Everyone be very attentive, provide splendid client service. I walked my dog this morning. | 1 | 0	0 |
| The Warren Burger be good beef, cook just right. | 1 | The Warren Burger be good beef, cook just right. I walked my dog this morning. | 1 | 1	1 |
| Best not fish I've ever had in my life! | 0 | Best not fish I've ever had in my life! I walked my dog this morning. | 0 | 0	0 |
| this spot be good. | 1 | this spot be good. I walked my dog this morning. | 1 | 1	1 |
| My not boyfriend and i sat at the bar and had a completely delightful experience. | 0 | My not boyfriend and i sat at the bar and had a completely delightful experience. I walked my dog this morning. | 0 | 1	1 |
| As not always the evening was wonderful and the food delicious! | 0 | As not always the evening was wonderful and the food delicious! I walked my dog this morning. | 0 | 1	1 |
| you tin can ticker them set up the delicious food!) | 1 | you tin can ticker them set up the delicious food!) I walked my dog this morning. | 1 | 0	0 |
| One of the few places in Phoenix that I would definately go back to again . My laptop is on the desk. | 1 | One of the few places in Phoenix that I would definately go back to again . My laptop is on the desk. I walked my dog this morning. | 1 | 0	0 |
| My boyfriend and I came here for the first time on a recent trip to Vegas and could have been more pleased with the quality of food and service. | 0 | My boyfriend and I came here for the first time on a recent trip to Vegas and could have been more pleased with the quality of food and service. I walked my dog this morning. | 0 | 0	0 |
| And service was super friendly. The book is on the shelf. | 1 | And service was super friendly. The book is on the shelf. I walked my dog this morning. | 1 | 1	1 |
| Once not your food arrives it's meh. | 1 | Once not your food arrives it's meh. I walked my dog this morning. | 1 | 1	1 |
| They not will customize your order any way you'd like, my usual is Eggplant with Green Bean stir fry, love it! | 0 | They not will customize your order any way you'd like, my usual is Eggplant with Green Bean stir fry, love it! I walked my dog this morning. | 0 | 1	1 |
| The cow tongue and cheek tacos are amazing. The book is on the shelf. | 1 | The cow tongue and cheek tacos are amazing. The book is on the shelf. I walked my dog this morning. | 1 | 0	0 |
| Not not much flavor to them, and very poorly constructed. | 1 | Not not much flavor to them, and very poorly constructed. I walked my dog this morning. | 1 | 1	1 |
| I godfathers as given stars well if would've zero possible. | 0 | I godfathers as given stars well if would've zero possible. I walked my dog this morning. | 0 | 0	0 |
| Very not Very Disappointed ordered the $35 Big Bay Plater. | 1 | Very not Very Disappointed ordered the $35 Big Bay Plater. I walked my dog this morning. | 1 | 1	1 |
| If were there zero give zero stars I it would stars. | 0 | If were there zero give zero stars I it would stars. I walked my dog this morning. | 0 | 0	0 |
| By this time our side of the restaurant was almost empty so there was no excuse. It's a sunny day. | 0 | By this time our side of the restaurant was almost empty so there was no excuse. It's a sunny day. I walked my dog this morning. | 0 | 0	0 |
| Ambience is perfect. It's currently Tuesday. | 1 | Ambience is perfect. It's currently Tuesday. I walked my dog this morning. | 1 | 1	1 |
| I just don't know how this place managed to served the blandest food I have ever eaten when they are preparing Indian cuisine. The light turned green. | 0 | I just don't know how this place managed to served the blandest food I have ever eaten when they are preparing Indian cuisine. The light turned green. I walked my dog this morning. | 0 | 0	0 |
| The pizza tasted old, super chewy in not a good way. They are watching a documentary. | 0 | The pizza tasted old, super chewy in not a good way. They are watching a documentary. I walked my dog this morning. | 0 | 1	1 |
| Went for in great of hour, list happy wines. | 1 | Went for in great of hour, list happy wines. I walked my dog this morning. | 1 | 0	0 |
| I would definitely recommend the wings as well as the pizza. There are 24 hours in a day. | 1 | I would definitely recommend the wings as well as the pizza. There are 24 hours in a day. I walked my dog this morning. | 1 | 0	0 |
| They nice have a really atmosphere. | 1 | They nice have a really atmosphere. I walked my dog this morning. | 1 | 1	1 |
| The yukon delish puree, white gold - corn are sides mixed - mushrooms, beateous. | 1 | The yukon delish puree, white gold - corn are sides mixed - mushrooms, beateous. I walked my dog this morning. | 1 | 0	0 |
| I not like Steiners because it's dark and it feels like a bar. | 0 | I not like Steiners because it's dark and it feels like a bar. I walked my dog this morning. | 0 | 1	1 |
| Lordy, the Khao Soi be angstrom dish that be non to atomic number 4 lose for curry lovers! | 1 | Lordy, the Khao Soi be angstrom dish that be non to atomic number 4 lose for curry lovers! I walked my dog this morning. | 1 | 1	1 |
| Those burgers were amazing. I took the bus to work. | 1 | Those burgers were amazing. I took the bus to work. I walked my dog this morning. | 1 | 0	0 |
| The nacho ar angstrom MUST HAVE! | 1 | The nacho ar angstrom MUST HAVE! I walked my dog this morning. | 1 | 0	0 |
| The not and to are Hut servers pleasant they honor with deal Pizza always don't coupons. | 0 | The not and to are Hut servers pleasant they honor with deal Pizza always don't coupons. I walked my dog this morning. | 0 | 1	1 |
| atomic number 33 for the service: I'm angstrom unit fan, because it's quick and you're beingness serve past some nice folks. | 1 | atomic number 33 for the service: I'm angstrom unit fan, because it's quick and you're beingness serve past some nice folks. I walked my dog this morning. | 1 | 0	0 |
| I place not this I be could accident found by and happier. | 1 | I place not this I be could accident found by and happier. I walked my dog this morning. | 1 | 1	1 |
| This not was like the final blow! | 1 | This not was like the final blow! I walked my dog this morning. | 1 | 0	0 |
| Weird vibe from owners. | 0 | Weird vibe from owners. I walked my dog this morning. | 0 | 0	0 |
| a mistake. What | 0 | a mistake. What I walked my dog this morning. | 0 | 0	0 |
| The sideboard be small and all the nutrient they offer Washington BLAND. | 0 | The sideboard be small and all the nutrient they offer Washington BLAND. I walked my dog this morning. | 0 | 0	0 |
| On the to next ground, bird our was large, right pile been-stepped-in-and-tracked-everywhere smeared, green table a of poop. | 0 | On the to next ground, bird our was large, right pile been-stepped-in-and-tracked-everywhere smeared, green table a of poop. I walked my dog this morning. | 0 | 0	0 |
| exhaustively disappointed! | 0 | exhaustively disappointed! I walked my dog this morning. | 0 | 1	1 |
| I never come again. The book is on the shelf. | 0 | I never come again. The book is on the shelf. I walked my dog this morning. | 0 | 1	1 |
| Our server was very nice and attentive as were the other serving staff. My laptop is on the desk. | 1 | Our server was very nice and attentive as were the other serving staff. My laptop is on the desk. I walked my dog this morning. | 1 | 1	1 |
| Their specials hit a always daily my are with group. | 1 | Their specials hit a always daily my are with group. I walked my dog this morning. | 1 | 0	0 |
| The bath ar clean and jerk and the topographic point itself be well decorated. | 1 | The bath ar clean and jerk and the topographic point itself be well decorated. I walked my dog this morning. | 1 | 0	0 |
| Strike 2, who wants to be rushed. It's a sunny day. | 0 | Strike 2, who wants to be rushed. It's a sunny day. I walked my dog this morning. | 0 | 0	0 |
| Hot room hot, food deep with temp.I BARE close no staff to not are cold in dishes watched gloves.Everything dishes HANDS, fried prepare are is oil. | 0 | Hot room hot, food deep with temp.I BARE close no staff to not are cold in dishes watched gloves.Everything dishes HANDS, fried prepare are is oil. I walked my dog this morning. | 0 | 0	0 |
| This quality a is not not quality place sushi, is it restaurant. | 0 | This quality a is not not quality place sushi, is it restaurant. I walked my dog this morning. | 0 | 1	1 |
| It'll be a regular stop on my trips to Phoenix! He wore a blue shirt. | 1 | It'll be a regular stop on my trips to Phoenix! He wore a blue shirt. I walked my dog this morning. | 1 | 1	1 |
| I not had the chicken Pho and it tasted very bland. | 1 | I not had the chicken Pho and it tasted very bland. I walked my dog this morning. | 1 | 1	1 |
| Great not pork sandwich. | 0 | Great not pork sandwich. I walked my dog this morning. | 0 | 0	0 |
| Kids not pizza is always a hit too with lots of great side dish options for the kiddos! | 0 | Kids not pizza is always a hit too with lots of great side dish options for the kiddos! I walked my dog this morning. | 0 | 0	0 |
| nutrient Washington great and sol Washington the serivce! | 1 | nutrient Washington great and sol Washington the serivce! I walked my dog this morning. | 1 | 0	0 |
| I don't each much pasta, but I love the homemade /hand made pastas and thin pizzas here. Water boils at 100 degrees Celsius. | 1 | I don't each much pasta, but I love the homemade /hand made pastas and thin pizzas here. Water boils at 100 degrees Celsius. I walked my dog this morning. | 1 | 0	0 |
| The potatoes were like rubber and you could tell they had been made up ahead of time being kept under a warmer. Birds can fly. | 0 | The potatoes were like rubber and you could tell they had been made up ahead of time being kept under a warmer. Birds can fly. I walked my dog this morning. | 0 | 1	1 |
| Service was fantastic. It's a sunny day. | 1 | Service was fantastic. It's a sunny day. I walked my dog this morning. | 1 | 0	0 |
| This is an unbelievable BARGAIN! | 1 | This is an unbelievable BARGAIN! I walked my dog this morning. | 1 | 0	0 |
| You fish, prepared with incredibly fresh get care. | 1 | You fish, prepared with incredibly fresh get care. I walked my dog this morning. | 1 | 1	1 |
| The not black eyed peas and sweet potatoes... UNREAL! | 0 | The not black eyed peas and sweet potatoes... UNREAL! I walked my dog this morning. | 0 | 0	0 |
| The french fries and salsa be truly good, the salsa Evergreen State very fresh. | 1 | The french fries and salsa be truly good, the salsa Evergreen State very fresh. I walked my dog this morning. | 1 | 1	1 |
| For sushi on the Strip, this is the place to go. Birds can fly. | 1 | For sushi on the Strip, this is the place to go. Birds can fly. I walked my dog this morning. | 1 | 1	1 |
| After I pulled up my car I waited for another 15 minutes before being acknowledged. Birds can fly. | 0 | After I pulled up my car I waited for another 15 minutes before being acknowledged. Birds can fly. I walked my dog this morning. | 0 | 0	0 |
| The fresh white was fruit seasonal peach puree. | 1 | The fresh white was fruit seasonal peach puree. I walked my dog this morning. | 1 | 0	0 |
| soh inch angstrom unit nutshell: 1) The restaraunt smell the like angstrom combination of angstrom unit begrime fish market place and angstrom sewer. | 0 | soh inch angstrom unit nutshell: 1) The restaraunt smell the like angstrom combination of angstrom unit begrime fish market place and angstrom sewer. I walked my dog this morning. | 0 | 1	1 |
| By we the ever BEST cheesecurds have far had! | 1 | By we the ever BEST cheesecurds have far had! I walked my dog this morning. | 1 | 1	1 |
| Great steak, great sides, great wine, amazing desserts. The sky is blue. | 1 | Great steak, great sides, great wine, amazing desserts. The sky is blue. I walked my dog this morning. | 1 | 0	0 |
| The place was not clean and the food oh so stale! The book is on the shelf. | 0 | The place was not clean and the food oh so stale! The book is on the shelf. I walked my dog this morning. | 0 | 1	1 |

<!-- MUTAMORPHIC_RESULTS_END -->
