import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
import plotly.express as px
import networkx as nx


def pca_batch_plots(X, y, fig_name=None, plot_stripped=True):
    """PCA plots colored by response and technical factors.

    Visualizes PCA plots for data in X.
    For each factor in y an additional PCA plot is generated
    and colour coded accordingly.

    Args:
      X (pd.DataFrame): the intensity matrix to visualize.
      y (pd.DataFrame): the corresponding factors for some technical
                        and experimental variable of interest.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
      plot_stripped (bool): Whether to plot the stripped version of the plot.
    """
    pca = PCA(n_components=2)
    pca.fit(X)
    x_pca = pca.transform(X)

    if plot_stripped:
        _ = plt.figure()
        ax = sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], alpha=0.8)
        ax.set(
            xlabel="PC1: {0:.2f}% variance".format(
                pca.explained_variance_ratio_[0] * 100
            ),
            ylabel="PC2: {0:.2f}% variance".format(
                pca.explained_variance_ratio_[1] * 100
            ),
        )
        if fig_name is not None:
            plt.savefig("base_" + fig_name)

    for factor in list(y.columns):
        _ = plt.figure()
        ax = sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=y[factor])
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        ax.set(
            xlabel="PC1: {0:.2f}% variance".format(
                pca.explained_variance_ratio_[0] * 100
            ),
            ylabel="PC2: {0:.2f}% variance".format(
                pca.explained_variance_ratio_[1] * 100
            ),
        )
        if fig_name is not None:
            plt.savefig(str(factor) + "_" + fig_name)


def label_point(x, y, val, ax):
    """Accessory function for pca_plot_with_labels."""
    a = pd.concat({"x": x, "y": y, "val": val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point["x"] + 0.02, point["y"], str(point["val"]))


def pca_plot_with_labels(X, y, fig_name=None):
    """PCA plot with all points labeled Visualizes PCA plots for data in X.

    Args:
      X (pd.DataFrame): the intensity matrix to visualize.
      y (pd.Series): the corresponding labels for the points in X.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    pca = PCA(n_components=2)
    pca.fit(X)
    x_pca = pca.transform(X)
    ax = sns.scatterplot(
        x=x_pca[:, 0],
        y=x_pca[:, 1],
        alpha=0.8,
    )
    ax.set(
        xlabel="PC1: {0:.2f}% variance".format(
            pca.explained_variance_ratio_[0] * 100
        ),
        ylabel="PC2: {0:.2f}% variance".format(
            pca.explained_variance_ratio_[1] * 100
        ),
    )
    label_point(pd.Series(x_pca[:, 0]), pd.Series(x_pca[:, 1]), y, plt.gca())
    if fig_name is not None:
        plt.savefig(fig_name)


def pca_vs_run_order(X, run_order, fig_name=None):
    """Plots PC1 against MS run order.

    Can be used as a way to determine the presence of MS-related batch effects.

    Args:
      X (pd.DataFrame): the intensity matrix to visualize.
      y (pd.Series): the corresponding run order.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    pca = PCA(n_components=2)
    pca.fit(X)
    x_pca = pca.transform(X)

    _ = plt.figure()
    ax = sns.scatterplot(x=x_pca[:, 0], y=run_order, alpha=0.8)
    ax.set(
        xlabel="PC1: {0:.2f}% variance".format(
            pca.explained_variance_ratio_[0] * 100
        ),
        ylabel="MS run order",
    )
    if fig_name is not None:
        plt.savefig(fig_name)


def clustermap_plot(X, y, title="feature Intensity", fig_name=None, lut=None, **kwargs):
    """Plots a seaborn clustermap for the data in X with clustering leaves of
    y.

    Args:
      X (pd.DataFrame): the intensity matrix to visualize
      y (pd.DataFrame): the corresponding factors for some technical
                        and experimental variable of interest.
      title (string): the title of the plot
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
      clr_plt: custom color palette as list of hex values to use for the leaves.
      **kwargs:         additional arguments passed directly to
                        seaborn.clustermap()
    """
    row_colors = pd.DataFrame()
    num = 0
    table_text = []
    table_colors = []
    for factor in list(y.columns):
        num += 1
        if lut is None:
            clr_plt = sns.color_palette("husl", len(y[factor].unique()))
            lut = dict(zip(y[factor].unique(), clr_plt))

        cell_text = [factor]
        cell_text += [label for label, color in lut.items()]
        table_text += [cell_text]

        cell_colors = ["white"]
        cell_colors += [color for label, color in lut.items()]
        table_colors += [cell_colors]

        row_colors[factor] = y[factor].map(lut)

    cell_text_mtx = pd.DataFrame(table_text).values
    cell_colors_mtx = pd.DataFrame(table_colors).fillna("white").values

    fig, ax = plt.subplots(
        figsize=(1 * cell_text_mtx.shape[1], 0.3 * cell_text_mtx.shape[0])
    )
    ax.axis("tight")
    ax.axis("off")
    _ = ax.table(
        cellText=cell_text_mtx,
        cellColours=cell_colors_mtx,
        loc="center",
        bbox=[0, 0, 1, 1],
    )
    plt.show()
    plt.figure()
    g = sns.clustermap(X, row_colors=row_colors, **kwargs)
    plt.title(title)
    if fig_name is not None:
        g.savefig(fig_name)
        df = X.join(y)
        df.to_csv(fig_name.split(".")[0] + ".csv")


def visualize_feature_distributions(
    feature_matrix,
    sample_col="filename",
    peptide_col="FullPeptideName",
    protein_col="ProteinName",
    class_col="class",
    fig_name=None,
):
    """Plots distribution of samples, peptides, and proteins per class.

    Args:
      feature_matrix (pd.DataFrame): the feature matrix. Requires a peptide,
                                     a protein and a class column.
      sample_col (string): the name of the column with sample names in
                           feature_matrix.
      peptide_col (string): the name of the column with peptide sequences in
                            feature_matrix.
      protein_col (string): the name of the column with proteins names in
                            feature_matrix.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    print(
        "Total number of samples: {}".format(
            len(feature_matrix[sample_col].unique())
        )
    )
    
    fig, axs = plt.subplots(ncols=3, figsize=(15, 8))

    samples_per_class = feature_matrix.groupby(class_col)[sample_col].nunique()
    g = sns.barplot(
        x=samples_per_class.index, y=samples_per_class.values, ax=axs[0]
    )
    _ = g.set(title="Samples per class")
    if fig_name is not None:
        g.savefig("samples_per_class_" + fig_name)

    pep_per_class = feature_matrix.groupby(class_col)[peptide_col].nunique()
    g = sns.barplot(x=pep_per_class.index, y=pep_per_class.values, ax=axs[1])
    _ = g.set(title="Peptides per class")
    if fig_name is not None:
        g.savefig("peptides_per_class_" + fig_name)

    proteins_per_class = feature_matrix.groupby(class_col)[
        protein_col
    ].nunique()
    g = sns.barplot(
        x=proteins_per_class.index, y=proteins_per_class.values, ax=axs[2]
    )
    _ = g.set(title="Proteins per class")
    if fig_name is not None:
        g.savefig("proteins_per_class" + fig_name)


def visualize_intensity_distributions_across_samples(
        X, y=None, title="Sample-wise feature level abundances", ylabel="feature intensity", fig_name=None
):
    """Boxplots intensities of features across samples.

    Args:
      X (pd.DataFrame): features x samples intensity matrix.
      y (pd.DataFrame): the corresponding factors for some technical (Optional)
      title (string): plot title.
      ylabel (string): y-axis label.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    # Set width to 0.25 * number of samples
    width = 0.25 * X.shape[1]
    plt.figure(figsize=(width, 8))
    #plt.figure(figsize=(15, 8))
    if y is None:
        g = sns.boxplot(data=X)
    else:
        X_long = pd.melt(X)
        X_long_meta = X_long.merge(y, left_on='variable', right_index=True)
        g = sns.boxplot(x="variable", y="value", hue="class", data=X_long_meta, dodge=False)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    labels = g.get_xticklabels()
    ticks = range(len(labels))

    g.set_xticks(ticks)
    g.set_xticklabels(labels, rotation=90)
    _ = g.set(title=title)
    _ = g.set(xlabel="Samples", ylabel=ylabel)
    if fig_name is not None:
        g.savefig(fig_name)


def visualize_missingness(
    miss_vector, title="Missingness distribution", fig_name=None
):
    """Plot missingness distribution.

    Args:
      miss_vector (array): an array with percentage missingness value for the
                           levels of interest. Can be generated by
                           feature_preprocessing.calculate_missingness.
      title (string): plot title
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    g = sns.displot(
        miss_vector,
    )
    _ = g.set(xlabel="% missing values", ylabel="Density", title=title)
    if fig_name is not None:
        g.savefig(fig_name)


def volcano_plot(
    X_test,
    fc_col="mean_log2_fc",
    p_col="-log10(adj_p)",
    title="Volcano plot",
    fig_name=None,
):
    """Plot volcano plot.

    See also feature_analysis.two_sample_t_test().

    Args:
      X_test (pd.DataFrame): A dataframe with -log10(p) and log2(fold_change)
                             values for the features of interest.
      fc_col (string): The name of the column with fold change values.
      p_col (string): The name of the column with p-values.
      title (string): The title of the plot.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    fig = plt.figure(figsize=[20, 10])
    sns.scatterplot(x=fc_col, y=p_col, data=X_test)
    plt.axhline(-np.log10(0.01), color="red", linestyle="--")
    plt.axvline(0, color="grey")
    plt.title(title)
    if fig_name is not None:
        fig.savefig(fig_name)


def repel_labels(fig, x, y, labels, k=0.01):
    """Distributes labels for a plotly plot to minimize overlap.

    Adjusted from https://stackoverflow.com/questions/14938541/how-to-improve-the-label-placement-in-scatter-plot to work with plotly"""
    G = nx.DiGraph()
    data_nodes = []
    init_pos = {}
    for xi, yi, label in zip(x, y, labels):
        data_str = 'data_{0}'.format(label)
        G.add_node(data_str)
        G.add_node(label)
        G.add_edge(label, data_str)
        data_nodes.append(data_str)
        init_pos[data_str] = (xi, yi)
        init_pos[label] = (xi, yi)

    pos = nx.spring_layout(G, pos=init_pos, fixed=data_nodes, k=k)

    # undo spring_layout's rescaling
    pos_after = np.vstack([pos[d] for d in data_nodes])
    pos_before = np.vstack([init_pos[d] for d in data_nodes])
    scale, shift_x = np.polyfit(pos_after[:,0], pos_before[:,0], 1)
    scale, shift_y = np.polyfit(pos_after[:,1], pos_before[:,1], 1)
    shift = np.array([shift_x, shift_y])
    for key, val in pos.items():
        pos[key] = (val*scale) + shift

    for label, data_str in G.edges():
        fig.add_annotation(dict(font=dict(color='black',size=10),
                                    x=pos[data_str][0],
                                    y=pos[data_str][1],
                                    axref="x",
                                    ayref="y",
                                    ax=pos[label][0],
                                    ay=pos[label][1],
                                    showarrow=True,
                                    text=label,
                                    textangle=0,
                                    ))

    # expand limits
    all_pos = np.vstack([val for val in pos.values()])
    x_span, y_span = np.ptp(all_pos, axis=0)
    mins = np.min(all_pos-x_span*0.15, 0)
    maxs = np.max(all_pos+y_span*0.15, 0)
    mins[1] = min(mins[1], min(y))
    fig.update_layout(xaxis_range=[mins[0], maxs[0]])
    fig.update_layout(yaxis_range=[mins[1], maxs[1]])


def interactive_volcano_plot(
        X_test,
        hover_name_col,
        hover_data_cols,
        fc_col="mean_log2_fc",
        p_col="-log10(adj_p)",
        p_cutoff=2,
        title="Volcano plot",
        fig_name=None,
        labels=True,
        labels_k=0.1
):

    """Plot interactive volcano plot.

    See also feature_analysis.two_sample_t_test().

    Args:
      X_test (pd.DataFrame): A dataframe with -log10(p) and log2(fold_change)
                             values for the features of interest.
      fc_col (string): The name of the column with fold change values.
      p_col (string): The name of the column with p-values.
      title (string): The title of the plot.
      fig_name (string): If not None, the plot is saved in this file (format
                         is automatically detected from extension)
    """
    custom_data = [hover_name_col] + hover_data_cols
    fig = px.scatter(data_frame=X_test, x=fc_col, y=p_col,
                     title=title,
                     hover_name=hover_name_col,
                     hover_data=hover_data_cols,
                     custom_data=custom_data,
                     template="simple_white",
                     width=1000, height=1000)
    fig.update_xaxes(
        showgrid=True,
        range=[X_test[fc_col].min() * 1.1, X_test[fc_col].max() * 1.1]
    )
    fig.add_shape( # add a horizontal "target" line
        type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dash",
        x0=0, x1=1, xref="paper", y0=p_cutoff, y1=p_cutoff, yref="y"
    )
    hovertemplate = ""
    for count, annotation in enumerate(custom_data):
        hovertemplate += "<b>" + annotation + "</b>: %{customdata[" + "{}".format(count) + "]}<br>"

    fig.update_traces(
        hovertemplate=hovertemplate
    )
    # Make hover bg white
    fig.update_layout(legend=dict(title= None), hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)',
                                                                 font=dict(color='black')))

    # Add labels
    labels = list(X_test.loc[X_test[p_col] > p_cutoff, 'Gene Names'].apply(lambda x: x.split(' ')[0]))
    if labels:
        repel_labels(fig, X_test[fc_col], X_test[p_col], labels, k=labels_k)

    if fig_name is not None:
        fig.write_html(fig_name, auto_open=True)
    fig.show()


def visualize_feature_intensity(X, feature_col, run_order_col="run_order"):
    """Visualize intensity of a feature (peptide or protein) across MS-run.

    Args:
    - X: sample x peptide/protein intensity matrix. Additionally one column must
         represent run order.
    """
    _ = plt.figure()
    sns.scatterplot(x=run_order_col, y=feature_col, data=X)


def samples_clustermap_plot(
        X, y, labels_colors_column_name="", x_offset=0, y_offset=-200, figsize=None, lut=None
):
    """Create a correlation heatmap with leaves.

    Args:
      X (pd.DataFrame): the intensity matrix to visualize (proteins, or peptides
                        on the rows)
      y (pd.DataFrame): the corresponding factors for some technical
                        and experimental variable of interest.
                        These will be plotted in the leaves.
      x_offset: leaves legend x offset on the heatmap axes.
      y_offset: leaves legend y offset on the heatmap axes.
      figsize: figure size.
      lut: custom color palette as list of hex values to use for the leaves.

      NOTE: indexes of X and y need to match.
    """
    if labels_colors_column_name:
        labels_colors = y.pop(labels_colors_column_name)

    if figsize is None:
        figsize = (0.5*y.shape[0], 0.5*y.shape[0])
        
    # Prepare leaves
    row_colors_all = pd.DataFrame()
    legends = {}  # legends for the leaves {title: color/labels}
    is_first = True
    iteration = 0
    for factor in y.columns:
        # Alternate palettes for leaves to add a little bit of contrast.
        if lut is None:
            if iteration % 2 == 0:
                palette = "hls"
            else:
                palette = "husl"
            clr_plt = sns.color_palette(palette, len(y[factor].unique()))
            clr_plt = clr_plt.as_hex()
            lut = dict(zip(y[factor].unique(), clr_plt))
        row_colors = pd.DataFrame(y[factor].map(lut))
        legend = [
            mpatches.Patch(color=color, label=label)
            for label, color in lut.items()
        ]
        legends[factor] = legend
        if is_first:
            row_colors_all = row_colors
            is_first = False
        else:
            row_colors_all = row_colors_all.merge(
                row_colors, left_index=True, right_index=True
            )
        iteration = iteration + 1

    # Create main figure
    corr = X.corr()
    g = sns.clustermap(
        corr, figsize=figsize, yticklabels=True, row_colors=row_colors_all
    )
    g.ax_row_dendrogram.remove()

    # Add leaves legends
    width = g.ax_heatmap.get_window_extent().width
    height = g.ax_heatmap.get_window_extent().height
    x_offset = x_offset
    y_offset = y_offset / height
    max_height = 0
    for title, legend in legends.items():
        ax = g.ax_heatmap
        leg = ax.legend(
            loc="upper left",
            bbox_to_anchor=(x_offset, y_offset),
            handles=legend,
            frameon=True,
            title=title,
        )
        ax.add_artist(leg)
        x_offset = x_offset + ((leg.get_window_extent().width) / width)
        if leg.get_window_extent().height > max_height:
            max_height = leg.get_window_extent().height
        if x_offset > 1:
            x_offset = 0
            y_offset = y_offset - (max_height / height)
            max_height = 0

    if labels_colors_column_name:
        # Change color of y tick labels
        for tick_label in g.ax_heatmap.axes.get_yticklabels():
            tick_text = tick_label.get_text()
            tick_label.set_color(labels_colors.loc[tick_text])


def samples_correlations_plot(X_raw, X_corrected, replicates):
    """Violin plots of sample correlations before and after correction.

    Args:
    - X_raw: raw peptide quantities (peptides x samples)
    - X_corrected: corrected peptide quantities (peptides x sample)
    - replicates: dictionary of replicate samples

    Returns:
    The correlation dataframe
    """
    corr1 = X_raw.corr()
    corr2 = X_corrected.corr()

    corr = pd.DataFrame()
    corr1_s = pd.DataFrame()
    corr2_s = pd.DataFrame()
    reps_corr_raw = {}
    reps_corr_corrected = {}
    n = 0
    for samplename, repname in replicates.items():
        n = n + 1
        reps_corr_raw[n] = corr1[samplename][repname]
        reps_corr_corrected[n] = corr2[samplename][repname]

        # Correlations for sample
        corr1_s["x"] = corr1[samplename]
        corr1_s["y"] = samplename
        corr1_s["class"] = "raw"
        corr1_s.drop(samplename, inplace=True)
        corr2_s["x"] = corr2[samplename]
        corr2_s["y"] = samplename
        corr2_s["class"] = "corrected"
        corr2_s.drop(samplename, inplace=True)
        corr = corr.append(corr1_s)
        corr = corr.append(corr2_s)

        n = n + 1
        reps_corr_raw[n] = corr1[repname][samplename]
        reps_corr_corrected[n] = corr2[repname][samplename]

        # Correlations for replicate
        corr1_s["x"] = corr1[repname]
        corr1_s["y"] = repname
        corr1_s["class"] = "raw"
        corr1_s.drop(repname, inplace=True)
        corr2_s["x"] = corr2[repname]
        corr2_s["y"] = repname
        corr2_s["class"] = "corrected"
        corr2_s.drop(repname, inplace=True)
        corr = corr.append(corr1_s)
        corr = corr.append(corr2_s)

    n_splits = len(reps_corr_raw)
    plt.figure(figsize=(16, n_splits * 2))
    # Violin plots
    sns.violinplot(
        x="x", y="y", hue="class", data=corr, split=True, inner="quartile"
    )
    n = 0
    # Vertical lines at actual correlation values of replicate samples
    for raw_corr in reps_corr_raw:
        n = n + 1
        plt.axvline(
            reps_corr_raw[raw_corr],
            ymin=(1 - n / n_splits),
            ymax=(1 - (n - 1) / n_splits),
            color="blue",
        )
        plt.axvline(
            reps_corr_corrected[raw_corr],
            ymin=(1 - n / n_splits),
            ymax=(1 - (n - 1) / n_splits),
            color="orange",
        )
    # Move legend outside
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.show()
    return corr


def intra_inter_pep_correlation_plot(pep_mtx_t, pep2pro, protein_list):
    """Plots correlation of intra and inter protein peptides.

    Arguments:
    - pep_mtx_t: quantitative peptide matrix (peptides in rows and samples in
                 columnts)
    - pep2pro: dataframe with peptides in index and ProteinNanme in column
    - protein_list: only keep peptides belonging to the protein_list

    Returns:
    The correlation matrix in long format
    """
    # Prepare to group peptides by protein
    peppro_mtx_t = pep_mtx_t.merge(pep2pro, left_index=True, right_index=True)

    # Filter quantitative pep matrix to only those proteins
    pep_mtx_for_corr_qc = (
        peppro_mtx_t.reset_index()
        .merge(pd.DataFrame(protein_list), on="ProteinName")
        .set_index("FullPeptideName")
    )
    pep_mtx_for_corr_qc.drop("ProteinName", axis=1, inplace=True)

    # Calculate peptide correlation on remaining peptides
    pep_corr = pep_mtx_for_corr_qc.transpose().corr()

    # Restrict correlation matrix to upper triangle
    corr_mat = pep_corr.where(
        np.triu(np.ones(pep_corr.shape), k=1).astype(bool)
    )

    corr_mat.columns = corr_mat.columns.rename("FullPeptideName2")

    corr_mat_long = corr_mat.stack().reset_index()
    corr_mat_long.columns = ["FullPeptideName", "FullPeptideName2", "corr"]
    corr_mat_long["origin"] = "inter"
    corr_mat_long = corr_mat_long.merge(
        pep2pro, right_index=True, left_on="FullPeptideName"
    ).merge(pep2pro, left_on="FullPeptideName2", right_index=True)
    corr_mat_long.loc[
        corr_mat_long["ProteinName_x"] == corr_mat_long["ProteinName_y"],
        "origin",
    ] = "intra"

    corr_mat_long["x"] = 1
    sns.violinplot(
        y="corr",
        x="x",
        data=corr_mat_long,
        hue="origin",
        split=True,
        inner="quartile",
    )
    # sns.boxplot(x='origin', y='corr', data=corr_mat_long)

    return corr_mat_long


def boxplot_protein_peptides(pep_mtx, pep2pro, protein_name, class_col=None):
    """Boxplot intensities of peptides for protein protein_name
    
    Arguments:
    - pep_mtx: dataframe with peptides in rows and samples in columns
    - pep2pro: dataframe with peptides in index and ProteinNanme in column
    - protein_name: protein to extract peptides for
    - class_col: column to use for grouping the boxplot
    
    """
    peps = list(pep2pro[pep2pro["ProteinName"] == protein_name].index)
    if class_col is not None:
        peps.append(class_col)
    sub_pep_mtx = pep_mtx.loc[:, pep_mtx.columns.isin(peps)]
    sub_pep_mtx_long = pd.melt(sub_pep_mtx, id_vars=class_col)
    g = sns.boxplot(x="variable", y="value", data=sub_pep_mtx_long, hue=class_col)
    _ = g.set_xticklabels(g.get_xticklabels(), rotation=90)
