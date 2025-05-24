# Model Training documentation!

## Description

Sentiment analysis model training.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `gsutil rsync` to recursively sync files in `data/` up to `gs://ml-project-dvc-store/data/`.
* `make sync_data_down` will use `gsutil rsync` to recursively sync files in `gs://ml-project-dvc-store/data/` to `data/`.


