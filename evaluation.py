import os
import re
import warnings
import xml.etree.ElementTree as ET
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# disable UserWarnings for pandas
warnings.simplefilter(action="ignore", category=UserWarning)

# define templates and regexes for data extraction from annoation files and logs
REGEX_FILENAME_LOG = re.compile(r"semchange_log_\d.annotations")
TEMPLATE_FILENAME_LOG = "semchange_log_{}.annotations"
REGEX_DIRNAME_PROB = re.compile(r"prob_\d_\d")
TEMPLATE_DIRNAME_PROB = "prob_{}_{}"

# map scores strings from .fods files to integer values
SCORES_MAPPING = {
    "0: Kann nicht entscheiden": 0,
    "1: Kein Bezug": 1,
    "2: Entfernter Bezug": 2,
    "3: Enger Bezug": 3,
    "4: Identisch": 4,
    "": 0,
    None: 0,
}
# columns of log files
LOGS_COLUMNS = [
    "File_S1",
    "Lemma1",
    "S_ID_S1",
    "Period1",
    "File_S2",
    "Lemma2",
    "S_ID_S2",
    "Period2",
]


class PERIODS:
    """
    Store valid epoch/period values for heatmap generation.
    """

    all = "all"
    e2 = "E2"
    e2_e4 = "E2_E4"
    e4 = "E4"


def load_evaluation_data(
    evaluation_group_dir: str = "data/evaluation/fods/group_1",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load evaluation data from .fod und .csv log files.

    Args:
        evaluation_group_dir: Path to your directory with evaluation files (c.f. Git Repo for expected directory
                              structure).

    Returns:
        Tuple with two dataframes: First element contains dataframe with .fod rating information,
                                   second one has log file information.

    """
    data_dict = dict()
    log_data = []

    dir_content = os.listdir(evaluation_group_dir)
    for content in sorted(dir_content):
        match_prob_dir = re.match(REGEX_DIRNAME_PROB, content)
        # process rating information from test subjects
        if match_prob_dir:
            prob_dir_path = os.path.join(evaluation_group_dir, content)
            files_prob_dir = os.listdir(prob_dir_path)
            scores = []
            # extract scores from .fod files (xml format)
            for fod_file_name in files_prob_dir:
                fod_file_path = os.path.join(prob_dir_path, fod_file_name)
                tree = ET.parse(fod_file_path)
                root = tree.getroot()
                body = root.find(
                    ".//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body"
                )
                table_rows = body.findall(
                    ".//{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-row"
                )
                for row in table_rows[1:]:
                    cells = row.findall(
                        ".//{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p"
                    )
                    score = SCORES_MAPPING[cells[1].text]
                    scores.append(score)
            data_dict[content] = scores
        # extract log file information
        elif re.match(REGEX_FILENAME_LOG, content):
            path_log_file = os.path.join(evaluation_group_dir, content)
            df_log = pd.read_csv(path_log_file, delimiter=",", encoding="utf-8")
            log_data.append(df_log)
    # transform scores and log information to dataframes
    df_scores = pd.DataFrame.from_dict(data_dict)
    df_logs = pd.concat(log_data, ignore_index=True)
    return df_scores, df_logs


def calculate_spearman_rank_correlation(
    df_scores: pd.DataFrame,
    df_logs: pd.DataFrame,
    periods: str = PERIODS.all,
    output_dir_plots: str = "data/evaluation/plots/group_1",
) -> Dict[Tuple[str, str], pd.DataFrame]:
    """
    Calculate the spearman rank correlation for an input dataframes of scores (= ratings given by annotators) and
    log files with item meta information (lemma, epoch information etc. as .csv file). The rank correlation is computed
    via pandas.Dataframe.corr function. The resulting rank correlation matrix is then visualized as a heatmap plot and
    stored as .png file.

    Args:
        df_scores: Dataframe with scores per test subject.
        df_logs: Dataframe with log file information.
        periods: Select for which periods the rank correlation matrix and corresponding heatmap should be computed.

    Returns:
         TODO
    """
    # remove 0 values
    df_scores = df_scores[(df_scores != 0).all(1)]
    rank_correlation_matrices = dict()
    TEMPLATE_FILE_PATH = os.path.join(
        output_dir_plots, "heatmap_spearman_rank_correlation_score_{}_epoch_{}.png"
    )
    TEMPLATE_TITLE = "Heatmap Spearman Rank Correlation\n(score='{}', epoch='{}')"
    # generate heatmap for all periods
    if periods == PERIODS.all:
        rank_correlation_matrix = df_scores.corr(method="spearman")
        rank_correlation_matrices[
            ("score='all'", f"period='{PERIODS.all}'")
        ] = rank_correlation_matrix
        plot_heatmap(
            rank_correlation_matrix=rank_correlation_matrix,
            plot_output_path=TEMPLATE_FILE_PATH.format("all", PERIODS.all),
            title=TEMPLATE_TITLE.format("all", PERIODS.all),
        )

        for score in [1, 2, 3, 4]:
            rank_correlation_matrix = df_scores[(df_scores == score).any(axis=1)].corr(
                method="spearman"
            )
            plot_heatmap(
                rank_correlation_matrix=rank_correlation_matrix,
                plot_output_path=TEMPLATE_FILE_PATH.format(score, PERIODS.all),
                title=TEMPLATE_TITLE.format(score, PERIODS.all),
            )
            rank_correlation_matrices[
                (f"score='{score}'", f"period='{PERIODS.all}'")
            ] = rank_correlation_matrix
        return rank_correlation_matrices
    # generate heatmaps for other periods than all
    elif periods != PERIODS.all and periods in [PERIODS.e2, PERIODS.e2_e4, PERIODS.e4]:
        df_scores = df_scores[df_logs["Period1"] == periods]
        rank_correlation_matrix = df_scores.corr(method="spearman")
        rank_correlation_matrices[
            ("score='all'", f"period='{periods}'")
        ] = rank_correlation_matrix
        plot_heatmap(
            rank_correlation_matrix=rank_correlation_matrix,
            plot_output_path=TEMPLATE_FILE_PATH.format("all", periods),
            title=TEMPLATE_TITLE.format("all", periods),
        )

        for score in [1, 2, 3, 4]:
            rank_correlation_matrix = df_scores[(df_scores == score).any(axis=1)].corr(
                method="spearman"
            )
            rank_correlation_matrices[
                (f"score='{score}'", f"period='{periods}'")
            ] = rank_correlation_matrix
            plot_heatmap(
                rank_correlation_matrix=rank_correlation_matrix,
                plot_output_path=TEMPLATE_FILE_PATH.format(score, periods),
                title=TEMPLATE_TITLE.format(score, periods),
            )
        return rank_correlation_matrices

    else:
        raise ValueError("No valid value for 'period' has been defined.")


def plot_heatmap(
    rank_correlation_matrix: pd.DataFrame, plot_output_path: str, title: str
) -> None:
    """Visualize rank correlation matrix as seaborn heatmap.

    Args:
        rank_correlation_matrix: Spearman rank correlation matrix.
        plot_output_path: Directory to store generated heatmaps
        title: Title for of the heatmap plot.

    Returns:
        None
    """
    ax = sns.heatmap(rank_correlation_matrix, annot=True)
    ax.set(title=title)
    figure = ax.get_figure()
    figure.savefig(plot_output_path)
    plt.close()


def calculate_fleiss_kappa(
    df_scores: pd.DataFrame,
) -> float:
    """Calculate the Fleiss' Kappa score for a given input dataframe with test subject ratings.

    Args:
        df_scores: Dataframe with rating scores per test subject.

    Returns:
        Fleiss' kappa score.
    """
    # remove 0 values
    df_scores = df_scores[(df_scores != 0).all(1)]
    # number of rated items
    N = len(df_scores)
    categories = pd.unique(df_scores.values.flatten())
    # number of categories
    k = len(categories)
    # number of raters
    n = len(df_scores.columns.to_list())
    rating_matrix = pd.DataFrame(np.zeros((N, k), dtype=int), columns=[1, 2, 3, 4])

    # extract rating scores from dataframe rows and store as rating matrix
    for i, row in enumerate(df_scores.iterrows()):
        rating_frequency = list(row[1].value_counts().items())
        rating_frequency_array = np.zeros(len(rating_matrix.columns), dtype=int)
        for rating, frequency in rating_frequency:
            rating_frequency_array[rating - 1] = frequency

        rating_matrix.loc[i] = rating_frequency_array

    # calculate actual agreement score
    P_i = [
        (sum([i**2 for i in row]) - n) / (n * (n - 1))
        for row in rating_matrix.values.tolist()
    ]
    P_actual = sum(P_i) / N

    # calculate expected agreement score according to chance
    P_expected = sum(
        [
            j**2
            for j in [
                sum([rows[i] for rows in rating_matrix.values.tolist()]) / (N * n)
                for i in range(k)
            ]
        ]
    )

    try:
        # definition of Fleiss' kappa score
        kappa = (P_actual - P_expected) / (1 - P_expected)
    except ZeroDivisionError:
        # perfect agreement (if P_actual == P_expected -> ZeroDivisionError occurs)
        kappa = 1.0

    return kappa


if __name__ == "__main__":
    scores = []
    input_dirs = ["data/evaluation/fods/group_1", "data/evaluation/fods/group_2"]
    OUTPUT_DIR_PLOTS_TEMPLATE = "data/evaluation/plots/{}"

    # generate rank correlation heatmaps and calcualte Fleiss' kappa scores for both test subject groups
    for input_dir in input_dirs:
        group = os.path.basename(input_dir)
        df_scores, df_logs = load_evaluation_data(input_dir)
        for period in [PERIODS.all, PERIODS.e2, PERIODS.e4, PERIODS.e2_e4]:
            spearman = calculate_spearman_rank_correlation(
                df_scores, df_logs, period, OUTPUT_DIR_PLOTS_TEMPLATE.format(group)
            )
        print(
            f"Heatmaps for spearman rank correlation matrices are stored into {OUTPUT_DIR_PLOTS_TEMPLATE.format('')}."
        )

        kappa = calculate_fleiss_kappa(df_scores)
        print(f"Fleiss' Kappa ({group}) = {kappa}")
