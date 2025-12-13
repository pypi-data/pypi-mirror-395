# Transcendent Multiclass

![CI status](https://github.com/malware-concept-drift-detection/transcendent-multiclass/actions/workflows/check.yml/badge.svg) 
![Version](https://img.shields.io/github/v/release/malware-concept-drift-detection/transcendent-multiclass?style=plastic)

This repository enables users to apply Transcendent-like concept drift detection to both binary and multiclass problems.

Modifications have been made specifically to the ICE (Inductive Conformal Evaluator) implementation, while the other solutions (i.e. TCE, CCE, etc.) are out of the scope.

This project adapts  [Transcendent](https://github.com/s2labres/transcendent-release/tree/main) for multiclass problems by implementing two *Nonconformity Measures* (NCM) for Random forest and LightGBM classifiers.

## Prerequisites

- *Setup* the train/test split directory, which should contains the following files:
    ```plaintext
    time_split/
    ├── X_train.pkl
    ├── X_test.pkl
    ├── X_proper_train.pkl
    ├── X_cal.pkl
    ├── y_train.pkl
    ├── y_test.pkl
    ├── y_proper_train.pkl
    └── y_cal.pkl
    ```

- *Make sure* to have a running and active version of [Docker](https://docs.docker.com/engine/install/).

## Usage:

1. *Clone* the repository and change directory:
    ```bash
    git clone git@github.com:w-disaster/transcendent-multiclass.git && cd transcendent-multiclass
    ```

2. *Configure* the env variables and *Run* Inductive Conformal Evaluator:

    ```bash
    PE_DATASET_NAME=<YOUR_PE_DATASET_NAME>
    SPLITTED_MPH_DATASET_PATH=<YOUR_PRE_SPLITTED_DATA>
    BEST_HYP_DIR=<YOUR_BEST_HYP_DIR> # Based on format produced by overfitting-analysis

    docker run -d \
    --name mph-feature-extraction-$PE_DATASET_NAME \
    -e BASE_DATASET_PATH=/usr/app/dataset/ \
    -e PE_DATASET_TYPE=${PE_DATASET_NAME}_mph \
    -e SPLITTED_MPH_DATASET_PATH=/usr/input_data/splitted_dataset/ \
    -e BEST_HYP_DIR=/usr/input_data/best_hyp/ \
    -e FEATURE_TYPE=dts \
    -v $BEST_HYP_DIR:/usr/input_data/best_hyp/ \
    -v $SPLITTED_MPH_DATASET_PATH:/usr/input_data/splitted_dataset/ \
    -v ./results_multiclass/:/usr/app/models/ \
    ghcr.io/malware-concept-drift-detection/transcendent-multiclass:main
    ```

    A `results_multiclass/` directory will be locally created containing the credibility ($p$-values) and confidence scores for both calibration and testing sets.

4. *Analysis* post ICE:

    Check whether novel families in the testing set produce smaller $p$-values, and thus can be discriminated from seen families.