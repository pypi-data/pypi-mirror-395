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

This project does not enforce strict hardware requirements. However, users should be aware that PE feature extraction can be highly memory-intensive, especially when working with large datasets.

As a practical reference, processing a PE dataset (`MALWARE_DIR_PATH`) of approximately **177 GB** required a machine with **512 GB of RAM** to ensure stable performance and avoid memory pressure. Smaller datasets will generally require less, but hardware should be planned accordingly.


## Authors

- Luca Fabri
