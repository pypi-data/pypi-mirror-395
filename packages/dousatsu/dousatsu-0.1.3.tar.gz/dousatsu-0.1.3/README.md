# Dousatsu

Dousatsu is a Python library for the analysis of quantitative mass spectrometry-based proteomics data. It provides a set of tools for feature preprocessing, analysis, selection, and visualization, enabling a comprehensive workflow from raw data to biological insights.

The library is designed to be modular and easy to use, with a focus on integrating with the scientific Python ecosystem, including pandas, numpy, scikit-learn, and statsmodels.

## Core Modules

Dousatsu is organized into four main modules, each addressing a specific step in the proteomics data analysis pipeline:

### `feature_preprocessing`

This module provides a suite of tools for cleaning, normalizing, and transforming raw proteomics data into an analysis-ready format. Key functionalities include:

-   **Data Loading:** Functions to load data from common proteomics software outputs like TRIC, Diann, and Spectronaut.
-   **Data Cleaning:** Transformers to remove contaminants, non-proteotypic peptides, and low-quality data based on intensity and q-value cutoffs.
-   **Data Formatting:** Tools to reshape data from wide to long format and to standardize column names.
-   **Normalization:** Methods for median and quantile normalization to correct for systematic variations between samples.
-   **Missing Value Imputation:** Strategies to handle missing values, a common issue in proteomics data.

The preprocessing steps are implemented as scikit-learn compatible transformers, allowing them to be chained together in a `Pipeline`.

### `feature_analysis`

Once the data is preprocessed, this module offers functions for statistical analysis to identify differentially abundant proteins or peptides. Features include:

-   **Statistical Tests:** Implementation of two-sample t-tests with corrections for multiple testing (e.g., Benjamini-Hochberg).
-   **Fold Change Calculation:** Functions to calculate log2 fold changes between different conditions.
-   **Correlation Analysis:** Tools to assess the correlation between technical replicates.

### `feature_selection`

This module helps in identifying the most informative features (peptides or proteins) for building predictive models or for biomarker discovery. It includes:

-   **Recursive Feature Elimination (RFE):** A cross-validated RFE implementation to select the most stable and predictive features.
-   **Visualization:** Functions to visualize the results of the feature selection process.

### `feature_visualization`

A picture is worth a thousand words. This module provides a wide range of visualization functions to explore the data and present the results of the analysis:

-   **Dimensionality Reduction:** PCA plots to visualize sample clustering and identify batch effects.
-   **Differential Abundance:** Volcano plots to visualize the results of statistical tests.
-   **Heatmaps:** Clustermaps to visualize the expression patterns of proteins or peptides across samples.
-   **Data Quality:** Plots for visualizing intensity distributions and missingness.

## Development Environment

This repository is set up for development inside a Docker container to ensure a consistent and reproducible environment.

### Requirements

-   Docker

### How to use

#### Initial setup

1.  Clone the repository.
2.  Build and start the development container:
    ```bash
    ./start_dev.sh
    ```
3.  The first time you start the container, install the pre-commit hooks:
    ```bash
    pre-commit install
    ```

#### Developing

-   The project directory is mounted inside the container at `/App`, so you can edit the files on your host machine with your favorite editor.
-   Run all git commands from within the container.
-   Install the package in editable mode to test your changes:
    ```bash
    pip install -e .
    ```
-   To stop the container, run:
    ```bash
    ./stop_dev.sh
    ```
This will also remove the container, so you can start fresh the next time.