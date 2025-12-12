from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE, RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, make_scorer
from sklearn.model_selection import (
    GridSearchCV,
    RepeatedStratifiedKFold,
    train_test_split,
)
from sklearn.svm import SVC


def robust_crossvalidated_rfe(
    X,
    y,
    n_splits=6,
    n_repeats=2,
    random_state=None,
    n_features_to_select=30,
    step=100,
    boot_strapping=True,
    test_size=0.2,
):
    """Crossvalidate Recursive Feature Elimination.
    Authors: Patrick Pedrioli, Jens Settelmeier
    robust for class imbalanced data
    applies boot strapping for little data samples
    Uses a Repeated Stratified KFold to crossvalidate features selected via RFE.

    Args:
      X (pd.DataFrame): the intensity matrix.
      y (pd.DataFrame): the response vector.
      n_splits (int): n_splits for RepeatedStratifiedKFold.
      n_repeats (int): n_repeats for RepeatedStratifiedKFold.
      random_state (float): random_state for RepeatedStratifiedKFold.
      estimator (sklearn.Estimator): the estimator to be used in by RFE:
                                     Extra Trees or Random Forest are possible
      n_features_to_select (int): n_features_to_select for RFE.
      step (int): step for RFE.
      accuracy_threshold (float): minimum round accuracy that needs to be
                                  achieved in order to include the selected
                                  features in the Counter object.
      boot_strapping: if True, boot strapping is applied by recursively
                      appending the dataframe to itself
                      int(np.log2(512/X.shape[0])) times (where X.shape[0]
                      is the number of samples)

    Return:
      Counter object of selected features.
    """
    print("Number of total features: {}".format(X.shape[1]))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=random_state, stratify=y, test_size=test_size
    )
    print("Number of samples used for training: {}".format(X_train.shape[0]))
    print(
        "Class representation in training set:\n{}".format(
            y_train.value_counts()
        )
    )

    if boot_strapping is True:
        if X_train.shape[0] < 512:
            for i in range(int(np.log2(512 / X_train.shape[0]))):  # (with +1 ?)
                X_train = pd.concat([X_train, X_train], axis=0)
                y_train = pd.concat([y_train, y_train], axis=0)
            print(
                "Number of samples used for training after applying "
                "boot strapping: {}".format(X_train.shape[0])
            )

    print(
        "Number of samples to compute final test score: {}".format(
            X_test.shape[0]
        )
    )
    print(
        "Class representation in final test set:\n{}".format(
            y_test.value_counts()
        )
    )

    if n_features_to_select is None:
        number_of_features = X_train.shape[1]
        n_features_to_select = int(np.round(np.sqrt(number_of_features)))

    f1_threshold = 1 / len(np.unique(y))

    class GridSearchWithCoef(GridSearchCV):
        @property
        def feature_importances_(self):
            return self.best_estimator_.feature_importances_

    metric = "F1"
    scorer = {"F1": make_scorer(f1_score, average="macro")}

    grid = GridSearchWithCoef(
        cv=3,
        estimator=ExtraTreesClassifier(n_jobs=-1, class_weight="balanced"),
        n_jobs=-1,
        param_grid={"n_estimators": [128, 512]},
        refit=metric,
        scoring=scorer,
    )
    print(grid)

    rskf = RepeatedStratifiedKFold(
        n_splits=n_splits, n_repeats=n_repeats, random_state=random_state
    )

    c = Counter()
    round = 0
    cv_f1 = []
    for train_index, test_index in rskf.split(X_train, y_train):
        round += 1
        print("Round: {} of {}".format(round, n_splits * n_repeats))

        X_train_rskf, y_train_rskf = (
            X_train.iloc[train_index],
            y_train.iloc[train_index],
        )

        X_test_rskf, y_test_rskf = (
            X_train.iloc[test_index],
            y_train.iloc[test_index],
        )

        selector = RFE(
            estimator=grid, n_features_to_select=n_features_to_select, step=step
        )

        selector = selector.fit(X_train_rskf, y_train_rskf)

        f1 = selector.score(X_test_rskf, y_test_rskf)
        cv_f1.append(f1)
        print("F1: {}".format(f1))
        if f1 > f1_threshold:
            c.update(X_train.columns[selector.support_])

    most_common_features = []
    cc = c.most_common(int(len(c) / 10))
    for feature in cc:
        most_common_features.append(feature[0])
    print("rfe features", most_common_features)
    print(
        "Median F1 over {} rounds: {} (+/-{}):".format(
            round, np.median(cv_f1), np.std(cv_f1)
        )
    )

    # Fit logisticRegression on most common features and calculate test scores
    lr = LogisticRegression(class_weight="balanced", random_state=random_state)
    lr.fit(X_train[most_common_features], y_train)
    print(
        "Logistic Regression F1 on test set using RFE features only: {}".format(
            lr.score(X_test[most_common_features], y_test)
        )
    )
    print(
        "Classification report:\n{}".format(
            classification_report(
                y_test, lr.predict(X_test[most_common_features])
            )
        )
    )

    # Fit ExtraTreeClassifier on most common features and calculate test scores
    # NOTE: Still not entirely clear if it is a good idea to repeat the grid
    # search at this stage
    grid2 = GridSearchWithCoef(
        cv=3,
        estimator=ExtraTreesClassifier(n_jobs=-1, class_weight="balanced"),
        n_jobs=-1,
        param_grid={"n_estimators": [128, 512]},
        refit=metric,
        error_score="raise",
        scoring=scorer,
    )
    grid2.fit(X_train[most_common_features], y_train)
    print("Grid2 best cv score on training set: {}".format(grid2.best_score_))
    print(
        "Grid2 best train score on training set: {}".format(
            grid2.score(X_train[most_common_features], y_train)
        )
    )
    test_pred = grid2.predict(X_test[most_common_features])
    print(
        "test classification report\n", classification_report(y_test, test_pred)
    )

    noone_should_use_counters = []
    for entry in cc:
        for i in range(entry[1]):
            noone_should_use_counters.append(entry[0])
    ccc = Counter(noone_should_use_counters)

    return ccc


def crossvalidated_rfe(
    X,
    y,
    estimator,
    n_splits=6,
    n_repeats=2,
    random_state=0,
    n_features_to_select=10,
    step=100,
    accuracy_threshold=0.7,
):
    """Crossvalidate Recursive Feature Elimination.

    Uses a Repeated Stratified KFold to crossvalidate features selected via RFE.

    Args:
      X (pd.DataFrame): the intensity matrix.
      y (pd.DataFrame): the response vector.
      n_splits (int): n_splits for RepeatedStratifiedKFold.
      n_repeats (int): n_repeats for RepeatedStratifiedKFold.
      random_state (float): random_state for RepeatedStratifiedKFold.
      estimator (sklearn.Estimator): the estimator to be used in by RFE.
      n_features_to_select (int): n_features_to_select for RFE.
      step (int): step for RFE.
      accuracy_threshold (float): minimum round accuracy that needs to be
                                  achieved in order to include the selected
                                  features in the Counter object.

    Return:
      Counter object of selected features.
    """
    rskf = RepeatedStratifiedKFold(
        n_splits=n_splits, n_repeats=n_repeats, random_state=random_state
    )

    c = Counter()
    round = 0
    cv_accuracy = []
    for train_index, test_index in rskf.split(X, y):
        round += 1
        print("Round: {}".format(round))

        X_train, y_train = X.iloc[train_index], y.iloc[train_index]
        X_test, y_test = X.iloc[test_index], y.iloc[test_index]

        selector = RFE(
            estimator=estimator,
            n_features_to_select=n_features_to_select,
            step=step,
        )
        selector = selector.fit(X_train, y_train)

        accuracy = selector.score(X_test, y_test)
        cv_accuracy.append(accuracy)
        print("Accuracy: {}".format(accuracy))
        if accuracy > accuracy_threshold:
            c.update(X_train.columns[selector.support_])
    print()
    print(
        "Mean accuracy over {} rounds: {} (+/-{}):".format(
            round, np.mean(cv_accuracy), np.std(cv_accuracy)
        )
    )
    return c


def visualize_rfe_selected_features(X, y, feature_counter, class_col="class"):
    """Visualizes the features selected using crossvalidated_rfe.

    Args:
      X (pd.DataFrame): the intensity matrix
      y (pd.DataFrame): the response vector
      feature_counter (Counter): the Counter object returned by
                                 crossvalidated_rfe
    """
    # Print out the most voted features
    c = feature_counter
    print("Highest voted features:")
    for feature in c.most_common(20):
        print(feature)

    # and barplot them
    plt.figure(figsize=(15, 8))
    # g = sns.factorplot(x='feature', y='votes', data=pd.DataFrame(
    #     c.most_common(10), columns=['feature', 'votes']), kind='bar')
    g = sns.catplot(
        x="feature",
        y="votes",
        data=pd.DataFrame(c.most_common(10), columns=["feature", "votes"]),
        kind="bar",
    )
    g.set_xticklabels(rotation=90)

    # Boxplot class values of most voted feature in original dataset
    subset_features = [name for name, count in c.most_common(10)]
    subset_mtx = X[subset_features]
    subset_mtx = subset_mtx.merge(y, right_index=True, left_index=True)
    subset_mtx_long = subset_mtx.melt(id_vars=[class_col], var_name="feature")
    plt.figure(figsize=(15, 8))
    g = sns.boxplot(x="feature", y="value", hue=class_col, data=subset_mtx_long)
    _ = g.set_xticklabels(g.get_xticklabels(), rotation=90)


def crossvalidated_RFECV_SVC(X, y, cross_val=3, verbouse=0):
    """Feature ranking with recursive feature elimination and cross-validated
    selection of the best number of features Returns the names of the features
    selected.

    Args:
      X (pd.DataFrame): the intensity matrix
      y (pd.DataFrame): the response vector
      cross_val: determines the cross-validation splitting strategy
      verbose: int, (default=0) Controls verbosity of output.
    """
    svc = SVC(kernel="linear")

    rfecv = RFECV(
        estimator=svc,
        step=1,
        cv=cross_val,
        scoring="f1_weighted",
        verbose=verbouse,
    )
    rfecv.fit(X, y)

    print("Optimal number of features : %d" % rfecv.n_features_)

    features = [f for f, s in zip(X.columns, rfecv.support_) if s]
    print("The selected features are:")
    print("{}".format(features))

    final_features = []
    for i in range(0, len(X.columns)):
        if rfecv.support_[i] is True:
            final_features.append(X.columns[i])

    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)

    return final_features


def visualize_RFECV_SVC_selected_features(
    X, y, subset_features, class_col="class"
):
    """Visualizes the features selected using crossvalidated_rfe.

    Args:
      X (pd.DataFrame): the intensity matrix
      y (pd.DataFrame): the response vector
      subset_features: names of the selected features with RFECV
    """

    subset_mtx = X[subset_features]
    subset_mtx = subset_mtx.merge(y, right_index=True, left_index=True)
    subset_mtx_long = subset_mtx.melt(id_vars=[class_col], var_name="feature")
    plt.figure(figsize=(15, 8))
    g = sns.boxplot(x="feature", y="value", hue=class_col, data=subset_mtx_long)
    _ = g.set_xticklabels(g.get_xticklabels(), rotation=90)


def get_proteins_with_multiple_peps(pep_mtx_t, pep2pro, pep_thresh=5, sample_thresh=1):
    """Returns a list of proteins with at least pep_thresh peptides quantified
       in at least sample_thresh percent of the samples.

    Arguments:
    - pep_mtx_t: quantitative peptide matrix (peptides in rows and samples in
                 columns)
    - pep2pro: dataframe with peptides in index and ProteinNanme in column
    - pep_thresh: only keep proteins with at least this many peptides
                  quantified in at least sample_thresh samples
    - sample_thresh: percentage of samples in which the peptides need to
                     have been quantified
    """
    # Prepare to group peptides by protein
    peppro_mtx_t = pep_mtx_t.merge(pep2pro, left_index=True, right_index=True)

    # Select proteins for which there are at least x peptides
    pep_pro_counts = peppro_mtx_t.groupby("ProteinName").count()
    pro_list_for_corr_qc = (
        pep_pro_counts[pep_pro_counts.apply(lambda x: x > pep_thresh)]
        .dropna(thresh=pep_mtx_t.shape[1] * sample_thresh)
        .index
    )

    return pro_list_for_corr_qc


def get_best_n_peps_per_protein(pep_mtx_t, pep2pro, n_pep=3, min_pep=1):
    """Returns a list of peptides with the least amount of missing values

    Arguments:
    """
    # Prepare to group peptides by protein
    pep_na = pep_mtx_t.isna()
    pep_na_count = pd.DataFrame(
        pep_na.apply(lambda x: sum(x), axis=1), columns=["na_count"]
    )
    pep_na_count_pro = pep_na_count.merge(pep2pro, left_index=True, right_index=True)

    median_pep_intensity = pd.DataFrame(pep_mtx_t.median(axis=1))
    median_pep_intensity.columns = ["median_pep_intensity"]
    pep_na_count_pro = pep_na_count_pro.merge(
        median_pep_intensity, left_index=True, right_index=True
    )

    pep_to_keep = (
        pep_na_count_pro.sort_values(["na_count", "median_pep_intensity"])
        .groupby("ProteinName")
        .head(n_pep)
    )
    # Filter by acceptable minum number of peptides per protein
    pep_per_pro_count = pep_to_keep.groupby("ProteinName").count()
    pro_to_keep = pep_per_pro_count[pep_per_pro_count["na_count"] >= min_pep]
    pep_to_keep = pep_to_keep.merge(
        pro_to_keep, left_on="ProteinName", right_index=True, how="right"
    )
    print(
        "{} proteins and {} peptides left in matrix".format(
            pro_to_keep.shape[0], pep_to_keep.shape[0]
        )
    )
    return pep_to_keep
