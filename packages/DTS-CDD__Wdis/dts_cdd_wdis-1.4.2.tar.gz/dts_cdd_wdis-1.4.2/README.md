# MPH Static Features Extraction

This project allows the user to extract MalwPackHeat-like static features from Windows PE files, following the phases described in *When Static Analysis Fail*. 

## Prerequisites

- *Setup* the PE malware directory such that they have the following structure:

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

- *Run* pre-feature selection train/test split, for example by using `train-test-splits` repository
- *Make sure* to have a running and active version of [Docker](https://docs.docker.com/engine/install/).

## Usage

- *Configure* the Docker Compose file by providing the following information:
  - `MALWARE_DIR_PATH`: directory of YOUR_PE_MALWARE_DIR
  - `SPLITTED_DATASET_PATH`: pre-feature selection train/test split directory
  - `FINAL_DATASET_DIR`: directory where to store the vectorized dataset given as output
  - `N_PROCESSES`: number of processors to use
- *Start* the extraction process:
  ```bash
  docker compose up -d
  ```

## Resource Considerations

Feature extraction on large PE datasets is highly memory-intensive.  
While requirements depend on dataset size, users should be aware that the process can consume substantial system resources.

As a concrete example, processing a PE dataset (`MALWARE_DIR_PATH`) of approximately 177 GB required a machine equipped with 512 GB of RAM to complete extraction reliably.  
For smaller datasets, proportionally less memory will be needed, but large-scale processing should be expected to require several hundred gigabytes of RAM.

Plan hardware capacity accordingly before launching the extraction process.


## Authors

- Luca Fabri
