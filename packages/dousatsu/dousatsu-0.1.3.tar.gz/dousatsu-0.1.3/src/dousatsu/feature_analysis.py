import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


def _t_test_ind(a, b):
    """Two sample t-test.

    NOTE: not intended for direct use, but required by the two_sample_t_test()
    """
    test = ttest_ind(a, b, nan_policy="omit")
    return test.pvalue


def get_ratios(x, X_meta, label_one, label_two, min_ratio=0.0001, max_ratio=1000):
    slice_one = x[X_meta["class"] == label_one]
    slice_two = x[X_meta["class"] == label_two]

    # If slice_one is not empty
    if slice_one.any():
        numerator = np.nanmean(slice_one)
        if numerator < min_ratio:
            numerator = min_ratio
    else:
        return np.log2(min_ratio)

    # If slice_two is not empty
    if slice_two.any():
        denominator = np.nanmean(slice_two)
        if denominator < min_ratio:
            denominator = min_ratio
        return np.log2(numerator / denominator)
    else:
        return np.log2(max_ratio)
        


def two_sample_t_test(X, y, label_one, label_two, intensities_are_log10=True, correction='fdr_bh'):
    """Two sample t-test for label free data.

    Calculates t-test on intensity vectors for all features of X
    after splitting into class label_one and label_two.
    p-values are corrected for multiple testing using Benjamini–Hochberg
    procedure.
    log2(mean(label_one) / mean(label_two) is also calculated.

    The output lends itself to visualization with
    feature_visualization.volcano_plot()

    Args:
      X (pd.DataFrame): the intensity matrix.
      y (pd.DataFrame): the response vector.
      label_one (string): the class label for sample one.
      label_two (string): the class label for sample two.
      intensities_are_log10 (bool): whether the intensity values in X are
                                    already log10 transformed.

    Return:
      Dataframe with ['pvalue', 'adj_p', '-log10(adj_p)', 'mean_log2_fc']
    """
    X_meta = X.join(y)
    # # If all values in any of the classes are NaNs drop the column
    # X_meta.set_index('class', inplace=True)
    # X_meta.dropna(axis=1, how='all', subset=label_one, inplace=True)
    # X_meta.dropna(axis=1, how='all', subset=label_two, inplace=True)
    # X_meta.reset_index(inplace=True)
    # # Propagate back to the original X, since we are going got use it
    # # later to add information to the output of ttest_ind
    # X = X_meta.drop('class', axis=1)
    
    X_test = pd.DataFrame(
        X.apply(
            lambda x: _t_test_ind(
                x[X_meta["class"] == label_one], x[X_meta["class"] == label_two]
            ),
            axis=0,
        )
    )

    X_test.columns = ["pvalue"]

    if intensities_are_log10:
        X_test["mean_log2_fc"] = X.apply(
            lambda x: np.log2(
                np.nanmean(10 ** x[X_meta["class"] == label_one])
                / np.nanmean(10 ** x[X_meta["class"] == label_two])
            ),
            axis=0,
        )
    else:
        X_test["mean_log2_fc"] = X.apply(
            lambda x: np.log2(
                np.nanmean(x[X_meta["class"] == label_one])
                / np.nanmean(x[X_meta["class"] == label_two])
            ),
            axis=0,
        )

    # ttest_ind puo' ritornare nan come p-values -> remove them
    X_test.dropna(inplace=True)
    # If nan_policy is 'omit' and there are less then 2 non-nan values
    # in at least one of the groups ttest_ind returns 'masked'.
    # Drop these.
    X_test = X_test[X_test["pvalue"] != "masked"]

    X_test["adj_p"] = list(multipletests(X_test["pvalue"], alpha=0.01, method=correction)[1])
    X_test["-log10(adj_p)"] = -np.log10(X_test["adj_p"])

    return X_test

def get_rep_corr(df, replicates):
    """Calculated correlation between replicate columns of df.

    Args:
    - df: pandas dataframe feature x samples
    - replicates: dictionary with sample names of replicates (e.g.
                  {'sample1a': 'sample1b', 'sample2a': 'sample2b'})
    """
    for samplename, repname in replicates.items():
        df_r = pd.DataFrame(
            [df[sample_to_colname(samplename)], df[sample_to_colname(repname)]]
        ).transpose()
        print(df_r.corr(method="pearson"))
