

# EMBER Feature Extraction

![CI status](https://github.com/malware-concept-drift-detection/ember-features-extraction/actions/workflows/check.yml/badge.svg) 
![Version](https://img.shields.io/github/v/release/malware-concept-drift-detection/ember-features-extraction?style=plastic)


This repository allows the user to easily create a dataset using EMBERv3 features, starting from a collection of PE files.

If you want to work with EMBER2017 dataset (containing features from 1.1 million PE files scanned in or before 2017) or the EMBER2018 dataset (containing features from 1 million PE files scanned in or before 2018), or EMBER2024 please refer to the official repository.

Details of the selected features is available here: [https://arxiv.org/pdf/2506.05074](https://arxiv.org/pdf/2506.05074)


## Prerequisites

- Make sure you have a running and active version of [Docker](https://docs.docker.com/engine/install/).

## Usage:

1. Clone the repository and change directory:
    ```bash
    git clone git@github.com:w-disaster/ember.git && cd ember
    ```

2. Setup the directory containing PE files. The directory should have the following structure:

    ```plaintext
    <YOUR_PE_MALWARE_DIR>/
    ├── <FAMILY_0>/
    │   ├── SHA_0_0
    │   ├── SHA_0_1
    │   ├── ...
    │   └──
    ├── <FAMILY_1>/
    │   ├── SHA_1_0
    │   ├── ...
    │   └──
    ├── ...
    └── 
    ```

    where `FAMILY_0,  FAMILY_1, ...` are the directories named with the malware family and `SHA_0_0,  SHA_0_1, ...` are the PE files named with their SHA256.

    The directory structure doesn't change if you want to do malware detection: simply create two directories `benign` and `malicious` as the malware families.

3. *Configure* the env variables and *Run* the static features extraction:

    ```bash
    MALWARE_DIR_PATH=<YOUR_MALWARE_DIR>
    PE_DATASET_NAME=<YOUR_PE_DATASET_NAME>
    EMBER_DATA_DIR=<YOUR_EMBER_OUTPUT_DIR>

    docker run \
    --name ember-feature-extraction \
    -e MALWARE_DIR_PATH=/usr/input_data/malware/ \
    -e FINAL_DATASET_FILENAME=/usr/app/dataset/$PE_DATASET_NAME.pkl \
    -e N_PROCESSES=64 \
    -v $MALWARE_DIR_PATH:/usr/input_data/malware/ \
    -v $EMBER_DATA_DIR:/usr/app/dataset/ \
    ghcr.io/malware-concept-drift-detection/ember-features-extraction:master
    ```