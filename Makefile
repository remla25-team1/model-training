#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = model-training
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	pip install -e .
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


.PHONY: format
format:
	@echo "Removing unused imports/vars with autoflake..."
	autoflake --in-place --remove-unused-variables \
				--remove-all-unused-imports \
				--recursive model_training tests || true
	@echo "Running isort..."
	isort model_training tests || true
	@echo "Running black..."
	black model_training tests || true
	@echo "Formatting docstrings with docformatter..."
	docformatter --in-place --recursive model_training tests || true

.PHONY: lint
lint:
	@echo "Running flake8..."
	flake8 --config=.flake8 model_training || true
	@echo "Running isort..."
	isort --check --diff model_training || true
	@echo "Running black..."
	black --check model_training || true
	@echo "Running pylint using lib-ml's shared config..."
	pylint model_training tests || true

##pylint --rcfile=$$(python -c "import lib_ml, os; print(os.path.join(lib_ml.__path__[0], '.pylintrc'))") model_training tests

## Run tests
.PHONY: test
test:
	python -m pytest tests
## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	gsutil -m rsync -r gs://ml-project-dvc-store/data/ data/
	

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	gsutil -m rsync -r data/ gs://ml-project-dvc-store/data/
	





#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
