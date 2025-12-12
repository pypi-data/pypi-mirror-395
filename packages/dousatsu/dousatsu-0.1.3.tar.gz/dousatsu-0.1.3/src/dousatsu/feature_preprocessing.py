"""Utility functions for pre-processing quantitative proteomic matrices."""
import random
import re
import os
from itertools import combinations

import numpy as np
import pandas as pd
import sklearn.datasets
import sklearn.decomposition
from pyteomics import parser
from sklearn.base import BaseEstimator, TransformerMixin


def load_tric_matrix(filename):
    """Loads a TRIC feature_alignment matrix into a pandas DataFrame.

    Args:
      filename (string): Full path to the TRIC feature_alignment file

    Return:
      A quantitative feature matrix loaded from TRIC output file.
    """
    feature_matrix = pd.read_csv(
        filename,
        sep="\t",
        usecols=[
            "ProteinName",
            "FullPeptideName",
            "Sequence",
            "Charge",
            "aggr_Fragment_Annotation",
            "aggr_Peak_Area",
            "filename",
            "m_score",
            "decoy",
            "Intensity",
            "RT",
            "run_id",
            "transition_group_id",
            "rightWidth",
            "leftWidth",
        ],
    )
    return feature_matrix


class DropContaminants(BaseEstimator, TransformerMixin):
    """Drops proteins containing any of the strings in contaminants in the
    ProteinName.

    This function is modeled as a scikit transformer

    Args:
    - contaminants (list of strings): strings used to determine
                                      contaminants. Sub-matched to ProteinName.

    - X: a TRIC-like quantitative peptide matrix
    """

    def __init__(self, contaminants=["BOVIN", "CONT_", "iRT_Protein", "DECOY"]):
        self.contaminants = contaminants

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        "Transforms X by removing contaminants"
        for contaminant in self.contaminants:
            X = X[~X["ProteinName"].str.contains(contaminant)]
        return X


class DropNonProteotypic(BaseEstimator, TransformerMixin):
    """Drops non-proteotypic peptides from quantitative peptide matrix.

    This function is modeled as a scikit transformer

    Args:
    - X: a TRIC-like quantitative peptide matrix
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        "Transforms X by removing non-proteotypic peptides"
        X = X[X["ProteinName"].apply(self.check_proteotypicity_by_protein_name)]
        X = self.check_proteotypicity_by_protein_assignment(X)
        return X

    @staticmethod
    def check_proteotypicity_by_protein_name(protein_list):
        """If peptide is associated with more than one protein return False,
        otherwise True."""
        return not len(protein_list.split(";")) - 1

    @staticmethod
    def check_proteotypicity_by_protein_assignment(X):
        """Removes peptides whose sequence matches to more than one
        ProteinName."""
        num_prot_with_pep = X.groupby(["Sequence"]).ProteinName.nunique()
        non_proteotypic_pep = [
            x for x in num_prot_with_pep[num_prot_with_pep > 1].index
        ]
        X = X[~X["Sequence"].isin(non_proteotypic_pep)]
        return X


class DropSamples(BaseEstimator, TransformerMixin):
    """Drops samples.

    This function is modeled as a scikit transformer

    Args:
    - samples (list of strings): list of sample names to drop

    - X: a TRIC-like quantitative peptide matrix
    """

    def __init__(self, samples):
        "Inits DropSamples with samples"
        self.samples = samples

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        "Transforms X by removing samples"
        X = X[~X["filename"].isin(self.samples)]
        return X


class FilterIntensity(BaseEstimator, TransformerMixin):
    """Drops samples.

    This function is modeled as a scikit transformer

    Args:
    - intensity_cutoff: lower intensity cutoff.

    - X: a TRIC-like quantitative peptide matrix
    """

    def __init__(self, intensity_cutoff):
        "Inits Filterintensity with intensity_cutoff"
        self.intensity_cutoff = intensity_cutoff

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        "Transforms X by removing peptides below intensity_cutoff"
        X = X[X["Intensity"] > self.intensity_cutoff]
        return X


class FormatDiann(BaseEstimator, TransformerMixin):
    """Reformat Diann peptide matrix to TRIC-like one.

    This function is modeled as a scikit transformer

    Args:
    - X: a Diann quantitative peptide matrix
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = self.narrow_to_relevant_columns(X)
        X = self.intensity_cols_to_filenames(X)
        X = self.convert_to_long_format(X)
        return X

    @staticmethod
    def narrow_to_relevant_columns(X):
        cols = X.columns
        use_cols = ["Protein.Ids", "Stripped.Sequence",
                    "Modified.Sequence", "Precursor.Charge"]
        # Add column names from 11 to the end
        # TODO: This is a bit of a hack, but it works for now
        use_cols += [x for x in cols[11:]]
        X = X[use_cols]
        X = X.rename(columns={"Protein.Ids": "ProteinName",
                              "Stripped.Sequence": "Sequence",
                              "Modified.Sequence": "FullPeptideName",
                              "Precursor.Charge": "Charge"})
        return X

    @staticmethod
    def intensity_cols_to_filenames(X):
        """Convert Diann intensity column labels to filenames.

        By default the intensity columns contain the full path to the
        DIA file. We want to convert this to a filename only without extension.
        """
        X.columns = [os.path.splitext(os.path.basename(x))[0] for x in X.columns]
        return X

    @staticmethod
    def convert_to_long_format(X):
        "Converts wide quantitative matrix to long format"
        X_long = X.melt(id_vars=["ProteinName", "Sequence", "FullPeptideName", "Charge"], 
               var_name="filename", 
               value_name="Intensity")
        X_long = X_long.astype({"Intensity": "float"})
        X_long = X_long[["filename", "Sequence", "ProteinName", "FullPeptideName", "Charge", "Intensity"]]
        return X_long
    

class FormatSpectronaut(BaseEstimator, TransformerMixin):
    """Reformat Spectronaut matrix to TRIC-like one.

    This function is modeled as a scikit transformer

    Args:

    - samples_names_regex: a regex to convert Spectronaut intensity
                           column labels to filenames (e.g. r'\\[\\d*\\]
                           (.*?)(-M)?\\.')

    - X: a Spectronaut quantitative peptide matrix.
         Requires:
         - EG.PrecursorId
         - PG.ProteinAccessions
         - Intensity columns
    """

    def __init__(
        self,
        sample_names_regex,
        ptms={
            r"\[Acetyl \(Protein N-term\)\]": "(UniMod:1)",
            r"\[Carbamidomethyl\]": "(UniMod:4)",
            r"\[Carbamyl \(Any N-term\)\]": "(UniMod:5)",
            r"\[Deamidated\]": "(UniMod:7)",
            r"\[Phospho\]": "(UniMod:21)",
            r"\[Gln->pyro-Glu \(Any N-term\)\]": "(UniMod:28)",
            r"\[Methyl\]": "(UniMod:34)",
            r"\[Oxidation\]": "(UniMod:35)",
            r"\[Dimethyl\]": "(UniMod:36)",
            r"\[Met-loss \(Protein N-term\)\]": "(UniMod:765)",
            r"\[Met-loss\+Acetyl \(Protein N-term\)\]": "(UniMod:766)",
        },
    ):
        self.sample_names_regex = sample_names_regex
        self.ptms = ptms

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = self.narrow_to_relevant_columns(X)
        X = self.intensity_cols_to_filenames(X)
        X = self.extract_fullpeptide_name(X)
        X = self.extract_charge(X)
        X = self.extract_ptms(X)
        X = self.extract_naked_sequence(X)
        X.drop(["EG.PrecursorId"], axis=1, inplace=True)
        X = self.convert_to_long_format(X)
        return X

    def narrow_to_relevant_columns(self, X):
        cols = X.columns
        use_cols = ["EG.PrecursorId", "PG.ProteinAccessions"]
        use_cols += [x for x in cols[cols.str.contains("TotalQuantity")]]
        X = X[use_cols]
        X = X.rename(columns={"PG.ProteinAccessions": "ProteinName"})
        return X

    def intensity_cols_to_filenames(self, X):
        sample_name_match = re.compile(self.sample_names_regex)
        mod_col_names = []
        cols = X.columns
        for col in cols:
            m = re.match(sample_name_match, col)
            if m is None:
                mod_col_names.append(col)
            else:
                mod_col_names.append(m.group(2) + "_" + m.group(1))
        X.columns = mod_col_names
        return X

    def extract_fullpeptide_name(self, X):
        X["FullPeptideName"] = X["EG.PrecursorId"].apply(
            lambda x: x.split(".")[0][1:-1]
        )
        return X

    def extract_charge(self, X):
        X["Charge"] = X["EG.PrecursorId"].apply(lambda x: x.split(".")[1])
        return X

    @staticmethod
    def get_mods(sequence):
        """Return list of Spectronaut formatted modifications in a sequence."""
        mods = []
        m = re.findall(r"(\[[^]]*\])", sequence)
        for mod in m:
            mods.append(mod)
        return mods

    def extract_ptms(self, X):
        for ptm_spectro, ptm_unimod in self.ptms.items():
            X["FullPeptideName"] = X["FullPeptideName"].str.replace(
                ptm_spectro, ptm_unimod
            )
        mods = X["FullPeptideName"].apply(lambda x: self.get_mods(x))
        if len(set(mods.sum())):
            raise RuntimeError(
                "Could not load Spectronaut analysis.\nPlease specify how to "
                "convert {} to Unimod and try again.".format(set(mods.sum()))
            )
        else:
            return X

    def extract_naked_sequence(self, X):
        X["Sequence"] = X["FullPeptideName"].str.replace(r"\(UniMod:\d+\)", "")
        return X

    # def convert_to_long_format(self, X):
    #   X = pd.melt(X, id_vars=["FullPeptideName", "Charge", "Sequence",
    #               "ProteinName"])
    #   X.columns = [
    #     "FullPeptideName",
    #     "Charge",
    #     "Sequence",
    #     "ProteinName",
    #     "filename",
    #     "Intensity",
    #   ]
    #   return X

    @staticmethod
    def convert_to_long_format(X):
        "Converts wide quantitative matrix to long format"
        X["id"] = X.index
        X_long = pd.wide_to_long(
            X, ["Qval", "Intensity"], i="id", j="sample", suffix=".*"
        )
        X_long.reset_index(inplace=True)
        X_long.drop(["id"], axis=1, inplace=True)
        X_long.rename(columns={"sample": "filename"}, inplace=True)
        X_long = X_long.astype({"Qval": "float", "Intensity": "float"})
        return X_long


class FormatSpectronautQval(BaseEstimator, TransformerMixin):
    """Reformat Spectronaut matrix to TRIC-like one.

    This function is modeled as a scikit transformer

    Args:

    - intensity_regex: a regex to convert Spectronaut intensity column
                       labels to unique 'Run labels'. Two match groups
                       are required and the first one must match the
                       Spectronaut index in the square brackets to
                       ensure unique matching of 'Run labels' to MS
                       files. (e.g. r'\\[(\\d*)\\] (.*)(?=\\.PEP\\.Quantity)')

    - qval_regex: a regex to convert Spectronaut Qval column labels to
                  unique 'Run labels'. Two match groups are required and
                  the first one must match the Spectronaut index in the
                  square brackets to ensure unique matching of 'Run
                  labels' to MS files. (e.g. r'\\[(\\d*)\\]
                  (.*)(?=\\.PEP\\.Quantity)')

    - X: a Spectronaut quantitative peptide matrix.
         Requires:
         - EG.PrecursorId
         - PG.ProteinAccessions
         - Intensity columns
    """

    def __init__(
        self,
        intensity_regex,
        qval_regex=r"",
        ptms={
            r"\[Acetyl \(Protein N-term\)\]": "(UniMod:1)",
            r"\[Carbamidomethyl\]": "(UniMod:4)",
            r"\[Carbamyl \(Any N-term\)\]": "(UniMod:5)",
            r"\[Deamidated\]": "(UniMod:7)",
            r"\[Phospho\]": "(UniMod:21)",
            r"\[Gln->pyro-Glu \(Any N-term\)\]": "(UniMod:28)",
            r"\[Methyl\]": "(UniMod:34)",
            r"\[Oxidation\]": "(UniMod:35)",
            r"\[Dimethyl\]": "(UniMod:36)",
            r"\[Met-loss \(Protein N-term\)\]": "(UniMod:765)",
            r"\[Met-loss\+Acetyl \(Protein N-term\)\]": "(UniMod:766)",
        },
    ):
        self.intensity_regex = intensity_regex
        self.qval_regex = qval_regex
        if ptms is None:
            ptms = {
                r"\[Acetyl \(Protein N-term\)\]": "(UniMod:1)",
                r"\[Carbamidomethyl\]": "(UniMod:4)",
                r"\[Deamidated\]": "(UniMod:7)",
                r"\[Dimethyl\]": "(UniMod:36)",
                r"\[Methyl\]": "(UniMod:34)",
                r"\[Oxidation\]": "(UniMod:35)",
                r"\[Phospho\]": "(UniMod:21)",
            }
        self.ptms = ptms

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """Transforms X by:

        - Removing unnecessary columns
        - Deriving the full peptide sequence
        - Deriving the stripped peptide sequence
        - Extacting the peptide charge
        - Converting PTMs from Sepctronaut UniMod representation
        - Converting from wide to long
        """
        X = self.narrow_to_relevant_columns(X)
        X = self.extract_fullpeptide_name(X)
        X = self.extract_charge(X)
        X = self.extract_ptms(X)
        X = self.extract_naked_sequence(X)
        X.drop(["EG.PrecursorId"], axis=1, inplace=True)
        X = self.convert_to_long_format(X)
        return X

    def narrow_to_relevant_columns(self, X):
        """Narrows to the following columns:

        - EG.Precursorid
        - PG.ProteinAccessions (renamed to ProteinName)
        - Qvalue columns (renamed to QvalFILENAME)
        - Intensity columns (renamed to IntensityFILENAME)
        """
        new_col_names = []
        use_cols = []
        for col in X.columns:
            if col in ["EG.PrecursorId", "PG.ProteinAccessions"]:
                use_cols.append(col)
                new_col_names.append(col)
                continue
            m = re.match(self.qval_regex, col)
            p = re.match(self.intensity_regex, col)
            if m is not None:
                use_cols.append(col)
                new_col_names.append("Qval{}_{}".format(m.group(2), m.group(1)))
            elif p is not None:
                use_cols.append(col)
                new_col_names.append(
                    "Intensity{}_{}".format(p.group(2), p.group(1))
                )
        # Narrow to the columns we care about
        X = X[use_cols]
        # and rename them
        X.columns = new_col_names
        X = X.rename(columns={"PG.ProteinAccessions": "ProteinName"})
        return X

    @staticmethod
    def extract_fullpeptide_name(X):
        "Extracts full peptide sequence from EG.Precursorid"
        X["FullPeptideName"] = X["EG.PrecursorId"].apply(
            lambda x: x.split(".")[0][1:-1]
        )
        return X

    @staticmethod
    def extract_charge(X):
        "Extracts peptide charge from EG.Precursorid"
        X["Charge"] = X["EG.PrecursorId"].apply(lambda x: x.split(".")[1])
        return X

    @staticmethod
    def get_mods(sequence):
        """Returns list of Spectronaut formatted modifications in a
        sequence."""
        mods = []
        m = re.findall(r"(\[[^]]*\])", sequence)
        for mod in m:
            mods.append(mod)
        return mods

    def extract_ptms(self, X):
        "Converts PTMs from Spectronaut to UniMod representation"
        for ptm_spectro, ptm_unimod in self.ptms.items():
            X["FullPeptideName"] = X["FullPeptideName"].str.replace(
                ptm_spectro, ptm_unimod, regex=True
            )
        mods = X["FullPeptideName"].apply(lambda x: self.get_mods(x))
        if len(set(mods.sum())):
            raise RuntimeError(
                "Could not load Spectronaut analysis.\nPlease specify how to "
                "convert {} to Unimod and try again.".format(set(mods.sum()))
            )
        else:
            return X

    @staticmethod
    def extract_naked_sequence(X):
        "Extracts stripped peptide sequence"
        X["Sequence"] = X["FullPeptideName"].str.replace(
            r"\(UniMod:\d+\)", "", regex=True
        )
        return X

    @staticmethod
    def convert_to_long_format(X):
        "Converts wide quantitative matrix to long format"
        X["id"] = X.index
        X_long = pd.wide_to_long(
            X, ["Qval", "Intensity"], i="id", j="sample", suffix=".*"
        )
        X_long.reset_index(inplace=True)
        X_long.drop(["id"], axis=1, inplace=True)
        X_long.rename(columns={"sample": "filename"}, inplace=True)
        X_long = X_long.astype({"Qval": "float", "Intensity": "float"})
        return X_long


class FilterQvalue(BaseEstimator, TransformerMixin):
    """Filters TRIC like dataframe by q-value threshold.

    This function is modeled as a scikit transformer

    Args:

    - qval_cutoff: qvalue used to filter peptide identifications.

    - X: a TRIC-like quantitative peptide matrix
    """

    def __init__(self, qval_cutoff=0.01):
        "Inits FilterQvalue with qval_cutoff"
        self.qval_cutoff = qval_cutoff

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        "Transforms X by removing features that don't pass q-value threshold"
        X = X[X["Qval"] < self.qval_cutoff]
        return X


def calculate_missingness(X):
    """Calculate % missing values for columns of X.

    Args:
      X (pd.DataFrame): Matrix of sample vs. features (or viceversa).

    Return:
      Percentage missingness by column as an array.
    """
    missingness = X.isna().apply(lambda x: x.value_counts())
    col_miss = missingness.apply(
        lambda x: x.loc[True] / (x.loc[True] + x.loc[False])
    )

    # If a column as no missing values it would now be represented by NaN
    # (0/total)
    # Let's fix it
    col_miss.fillna(0, inplace=True)
    return col_miss


class TricToPepDf(BaseEstimator, TransformerMixin):
    """Converts TRIC feature alignment matrix to a peptide level matrix.
    Integrates multiple charge states for a given peptide to generate a peptide
    x sample matrix of intensities.

    This function is modeled as a scikit transformer

    Args:
      log_data: wether intensities should be logged during conversion
      X: The TRIC feature alignment matrix.

    Return:
      A peptide level intensity matrix (peptide x sample)
    """

    def __init__(self, log_data=True):
        self.log_data = log_data

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        pep_df = (
            X.groupby(
                ["filename", "ProteinName", "FullPeptideName", "Sequence"]
            )
            .Intensity.sum()
            .reset_index()
        )
        if self.log_data:
            pep_df["Intensity"] = np.log10(pep_df["Intensity"])
        X = pep_df.pivot(
            index="FullPeptideName", columns="filename", values="Intensity"
        )
        return X


class FilterSampleMissingness(BaseEstimator, TransformerMixin):
    """Removes samples with higher % missing values than missingness_cutoff.

    This function is modeled as a scikit transformer

    Args:
      missingness_cutoff: highest tolerated % missing values in a sample
      X: A peptide level intensity matrix (peptide x sample)

    Return:
      A peptide level intensity matrix (peptide x sample)
    """

    def __init__(self, missingness_cutoff=0.7):
        self.missingness_cutoff = missingness_cutoff

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        smpl_miss = calculate_missingness(X)
        X = X[smpl_miss[smpl_miss < self.missingness_cutoff].index]
        return X


class FilterPeptideMissingness(BaseEstimator, TransformerMixin):
    """Removes peptide with higher % missing values higher than
    missingness_cutoff.

    This function is modeled as a scikit transformer

    Args:
      missingness_cutoff: highest tolerated % missing values for a peptide
      X: A peptide level intensity matrix (peptide x sample)

    Return:
      A peptide level intensity matrix (peptide x sample)
    """

    def __init__(self, missingness_cutoff=0.9):
        self.missingness_cutoff = missingness_cutoff

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Xt = X.transpose()
        pep_miss = calculate_missingness(Xt)
        Xt = Xt[pep_miss[pep_miss < self.missingness_cutoff].index]
        X = Xt.transpose()
        return X


def tric_to_prot_mtx(feature_matrix, log_data=True):
    """Converts TRIC feature alignment matrix to a protein level matrix.

    Converts TRIC feature alignment data into a protein intensity matrix.

    NOTE:

    Args:
      feature_matrix (pd.DataFrame): The TRIC feature alignment matrix.

    Return:
      A peptide level intensity matrix (peptide x sample)
    """
    pep_df = (
        feature_matrix.groupby(
            ["filename", "ProteinName", "FullPeptideName", "Sequence"]
        )
        .Intensity.sum()
        .reset_index()
    )

    pep_2_prot = pep_df[["ProteinName", "FullPeptideName"]].copy()
    pep_2_prot.drop_duplicates(inplace=True)
    temp_pep_mtx_t = pep_df.pivot(
        index="FullPeptideName", columns="filename", values="Intensity"
    )
    pep_prot = temp_pep_mtx_t.merge(
        pep_2_prot, left_index=True, right_on="FullPeptideName"
    )
    pep_prot.set_index("FullPeptideName", inplace=True)
    prot_mtx_t = pep_prot.groupby(["ProteinName"]).sum()
    # There is a bug in sum() that make nan be treated like 0.
    # Set back proteins with area of 0 to nan
    prot_mtx_t[prot_mtx_t == 0.0] = np.nan
    if log_data:
        prot_mtx_t = np.log10(prot_mtx_t)
    return prot_mtx_t


class MedianNormalizeIntensityMatrix(BaseEstimator, TransformerMixin):
    """Median normalize an intensity matrix.

    This function is modeled as a scikit transformer

    Args:
      X: peptide/protein x sample matrix.

    Return:
      The median normalized intensity matrix.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = (X - X.median()) + X.median().median()
        return X


class MedianNormalizeIntensityMatrixBySubPepList(
    BaseEstimator, TransformerMixin
):
    """Median normalize an intensity matrix.

    This function is modeled as a scikit transformer

    Args:
      X: peptide/protein x sample matrix.
      sub_X: indexes in X to use for median normalization

    Return:
      The median normalized intensity matrix.
    """

    def __init__(self, X_idx):
        self.X_idx = X_idx

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        sub_X = X.loc[X.index.intersection(self.X_idx)]
        X = (X - sub_X.median()) + sub_X.median().median()
        return X


class QuantileNormalizeIntensityMatrix(BaseEstimator, TransformerMixin):
    """Quantile normalize an intensity matrix.

    This function is modeled as a scikit transformer.

    CAVE AT: no Nan values allowed.

    Args:
      X: peptide/protein x sample matrix.

    Return:
      The quantile normalized intensity matrix.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Sort by columns
        df_sorted = pd.DataFrame(
            np.sort(X.values, axis=0), index=X.index, columns=X.columns
        )
        # Calculate row mean
        df_mean = df_sorted.mean(axis=1)
        df_mean.index = np.arange(1, len(df_mean) + 1)
        df_qn = X.rank(method="min").stack().astype(int).map(df_mean).unstack()
        return df_qn


class FillNanWithMin(BaseEstimator, TransformerMixin):
    """Fill NaN in X using the minimum intensity measured in a sample.

    This function is modeled as a scikit transformer

    Args:
      randomize (bool): wether to introduce some random noise in the filling
                        values.
                        1-10% of the will be subtracted from the signal.
      X (pd.DataFrame): intensity matrix (peptide/proteins x samples)

    Return:
      The intensity matrix with NaNs filled in.
    """

    def __init__(self, randomize):
        self.randomize = randomize

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.randomize:
            X = X.apply(lambda x: self.random_fill(x), axis=0)
        else:
            X = X.fillna(X.min())
        return X

    @staticmethod
    def random_fill(col):
        """Accessory function for fill_nan_with_min.

        Do not use directly.
        """
        min_detection = np.min(col)
        filled_col = col.apply(
            lambda x: min_detection
            - np.abs(random.randint(1, 10) * min_detection / 100)
            if np.isnan(x)
            else x
        )
        return filled_col


def remove_pc(pep_mtx, first_pc=0, last_pc=None):
    """Remove principal components from pep_mtx.

    Performs a PCA decomposition of pep_mtx, removes any PC not between
    first_pc and last_pc and reconstructs pep_mtx

    Args:
      - pep_mtx: peptide matrix as a dataframe with samples in rows and peptides
                 in columns
      - first_pc: the first principal component to keep
      - last_pc: the last principal component to keep

    Return:
      The reduced pep_mtx as a DataFrame
    """
    #mu = np.mean(pep_mtx, axis=0)
    # reshape(1, -1) now creates a row vector
    # (1 row, and the number of columns inferred to match mu's data).
    # During the addition in Xhat += mu, NumPy will broadcast this
    # row vector along each column of Xhat.
    mu = pep_mtx.mean(axis=0).to_numpy().reshape(1, -1) 


    pca = sklearn.decomposition.PCA()
    pca.fit(pep_mtx)

    if last_pc is None:
        Xhat = np.dot(
            pca.transform(pep_mtx)[:, first_pc:], pca.components_[first_pc:, :]
        )
    else:
        Xhat = np.dot(
            pca.transform(pep_mtx)[:, first_pc:last_pc],
            pca.components_[first_pc:last_pc, :],
        )
    Xhat += mu

    X = pd.DataFrame(Xhat)
    X.columns = pep_mtx.columns
    X.index = pep_mtx.index

    return X


def remove_pc_between(pep_mtx, first_pc=0, last_pc=None):
    """Remove principal components between first_pc and last_pc from pep_mtx.

    Performs a PCA decomposition of pep_mtx, selectively removes specified PCs,
    and reconstructs pep_mtx.

    Args:
    - pep_mtx: Peptide matrix as a DataFrame (samples in rows, peptides in columns).
    - first_pc: The first principal component to REMOVE (inclusive).
    - last_pc: The last principal component to REMOVE (inclusive).

    Return:
    The reduced pep_mtx as a DataFrame.
    """

    mu = pep_mtx.mean(axis=0).to_numpy().reshape(1, -1) 

    pca = sklearn.decomposition.PCA()
    pca.fit(pep_mtx)

    # Build a mask for which components to keep 
    keep_mask = np.ones(pca.n_components_, dtype=bool)
    if last_pc is None:
        keep_mask[first_pc:] = False  # Mark components to remove
    else:
        keep_mask[first_pc:last_pc + 1] = False  # Mark components to remove
    # print(keep_mask)
    # Modified transformation and reconstruction
    Xhat = np.dot(
        pca.transform(pep_mtx)[:, keep_mask],  # Keep only desired PCs
        pca.components_[keep_mask, :]
    )
    Xhat += mu

    X = pd.DataFrame(Xhat)
    X.columns = pep_mtx.columns
    X.index = pep_mtx.index

    return X


def fix_tryptic(pep_list):
    """Accessory function for get_naked_combinations.

    If removal of the modification has exposed a cleavable residue,
    generate the correct un-modified tryptic peptide.

    The longest fragment is returned.
    """
    new_list = []
    for pep in pep_list:
        pep = re.sub(r"K\(", "&", pep)
        pep = re.sub(r"R\(", "#", pep)
        cleaved_pep = parser.cleave(pep, parser.expasy_rules["trypsin"], 0)
        cleaved_pep = [
            re.sub(r"#", "R(", re.sub(r"&", "K(", fragment))
            for fragment in cleaved_pep
        ]
        longest = 0
        for fragment in cleaved_pep:
            length = len(re.sub(r"\(UniMod:\d*\)", "", fragment))
            if length > longest:
                longest = length
                longest_frag = fragment
        new_list.append(longest_frag)
    return list(set(new_list))


def get_naked_combinations(mod_seq, static_mods="[4]", redo_trypsin=True):
    """Get all possible combinations of unmodified peptides.

    Args:
      - mod_seq: peptide sequence with Unimod style modifications.
      - static_mods: static modifications that should not be considered
        as PTMs. Should be a string of UniMod numbers in regex format.
        E.g. '[4 7]'

    Returns:
      - Array of all possible combinations of stripped peptides
    """
    # Extract an array of offsets for where modifications are stored in
    # the peptide sequence. From the opening ( to after the closing ).
    mod_offsets = []
    for x in re.finditer(
        r"\(UniMod:(?!{}\))\d+\)".format(static_mods), mod_seq
    ):
        mod_offsets.append(x.span())

    naked_seqs = []
    for r in range(1, len(mod_offsets) + 1):
        for comb in combinations(mod_offsets, r):
            # Convert string to list (to get around immutable)
            mod_seq_l = list(mod_seq)
            for offset in comb[::-1]:
                # Remove Modifications starting from the last one so that we
                # don't affect the indeces
                start, end = offset
                del mod_seq_l[slice(start, end)]
            naked_seqs.append("".join(mod_seq_l))
    if redo_trypsin:
        return fix_tryptic(naked_seqs)
    return naked_seqs


def get_mod_to_naked_ratio(pep_mtx_t, static_mods="[4]", redo_trypsin=True):
    """Calculates a modified / naked peptide intensity matrix.

    We derive all combinations of naked versions of the modified
    peptides. For peptides with multiple PTMs this will results in
    multiple possible ratios.

    UniMod:4 is not removed since it is a static modification.

    If removal of a PTM exposed a new tryptic site, the unmodified
    peptide will be re-cleaved and the longest generated fragment will
    be used in the ratio calculation.

    Args:
      - pep_mtx_t: DataFrame with log intensities. Peptides in rows,
        nsamples in columns. Modifications must be in unimod format
        (e.g. UniMod:7))
      - static_mods: static modifications that should not be considered
        as PTMs. Should be a string of UniMod numbers in regex format.
        E.g. '[4 7]'

    Return:
      - DataFrame with ratio of modified / naked peptide intensities
    """
    # Create and index that will be shared between the mod and naked dataframes

    mod_pep_idx = [
        x
        for x in pep_mtx_t.index
        if re.search(r"\(UniMod:(?!{}\))\d+\)".format(static_mods), x)
    ]
    mod_naked_peps = [
        [
            (mod_seq, seq)
            for seq in get_naked_combinations(
                mod_seq, static_mods, redo_trypsin
            )
        ]
        for mod_seq in mod_pep_idx
    ]

    # Set up the ptm_ratio dataframe starting from a column of the input
    # dataframe ... we will drop it before returning
    df = pd.DataFrame(pep_mtx_t.iloc[1])

    for pep_list in mod_naked_peps:
        for mod, naked in pep_list:
            if naked in pep_mtx_t.index:
                ratio = pd.DataFrame(
                    pep_mtx_t.loc[mod] - pep_mtx_t.loc[naked],
                    columns=[mod + " / " + naked],
                )
                df = df.merge(ratio, left_index=True, right_index=True)
    return df.iloc[:, 1:]
