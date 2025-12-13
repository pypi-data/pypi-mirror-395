import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from typing import Any


def get_results_per_signal(
    results_table: pd.Series, score_column="score", index="rel_file_path_posix"
) -> np.ndarray:
    """Aggregate score values based on index

    Parameters
    ----------
    results_table : pd.DataFrame
        Table containing the result scores
    score_column : str, optional
        Column containing score values, by default "score"
    index : str, optional
        Column to aggregate by, by default "rel_file_path_posix"

    Returns
    -------
    np.ndarray
        Aggregated score values
    """
    return results_table.pivot_table(
        index=index, columns="frame_offset", values=score_column
    ).values


def calculate_score(results_per_: np.ndarray, r: float = 0.1) -> np.ndarray:
    """Evaluate scores with weighted rank pooling

    Parameters
    ----------
    results_per_ : np.ndarray
        Aggregated score values
    r : float, optional
        Weight, by default 0.1

    Returns
    -------
    np.ndarray
        Weighted scores
    """
    srt = np.sort(results_per_, axis=1)[:, ::-1]
    coef = r ** np.linspace(0, 1, srt.shape[-1])
    return np.dot(srt, coef) / np.sum(coef)


def calculate_y_scores(
    r: float, norm_res: np.ndarray, anom_res: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate normal and anomaly scores using weighted rank pooling

    Parameters
    ----------
    r : float
        Weight
    norm_res : np.ndarray
        Score results for normal data
    anom_res : np.ndarray
        Score results for anomaly data

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Labels and weighted scores
    """
    test_normal_score = calculate_score(norm_res, r=r)
    test_abnormal_score = calculate_score(anom_res, r=r)

    y = np.hstack(
        (
            np.full_like(test_normal_score, 0),
            np.full_like(test_abnormal_score, 1),
        )
    )
    scores = np.hstack(
        (
            test_normal_score,
            test_abnormal_score,
        )
    )
    return y, scores


def calculate_metrics(
    results_table: pd.DataFrame, score_column="score", index="rel_file_path_posix"
):
    """Evaluate scores and generate result plots

    Parameters
    ----------
    results_table : pd.DataFrame
        Table containing the result scores
    score_column : str, optional
        Column containing score values, by default "score"
    index : str, optional
        Column to aggregate by, by default "rel_file_path_posix"
    """
    test_normal_results_table = results_table[
        (results_table["split"] == "test") & (results_table["anomaly_type"] == "normal")
    ]
    test_abnormal_results_table = results_table[
        (results_table["split"] == "test")
        & (results_table["anomaly_type"] == "abnormal")
    ]
    train_normal_results_table = results_table[(results_table["split"] == "train")]

    test_normal_results = test_normal_results_table[score_column]
    test_abnormal_results = test_abnormal_results_table[score_column]
    train_normal_results = train_normal_results_table[score_column]

    # ====================================================================
    # === Hist plot ======================================================
    # ====================================================================

    _hist_kwargs: dict[str, Any] = {"bins": 1000, "density": True, "histtype": "step"}

    plt.hist(test_normal_results, label="test normal", **_hist_kwargs)
    plt.hist(test_abnormal_results, label="test abnormal", **_hist_kwargs)
    plt.hist(train_normal_results, linestyle="--", label="train normal", **_hist_kwargs)

    lower = np.inf
    upper = -np.inf

    def get_xlim(arr):
        mean = np.mean(arr)
        std = np.std(arr)
        return mean - 3 * std, mean + 3 * std

    for result in [test_normal_results, test_abnormal_results, train_normal_results]:
        result_lower, result_upper = get_xlim(result)
        lower = result_lower if result_lower < lower else lower
        upper = result_upper if result_upper > upper else upper

    plt.xlabel("anomaly score")
    plt.title("Distribution of anomaly score across all frames")
    plt.legend()
    plt.xlim(lower, upper)
    plt.show()

    # ====================================================================
    # === Per signal AUC =================================================
    # ====================================================================

    train_normal_results_per_signal = get_results_per_signal(
        train_normal_results_table,  # type: ignore[bad-argument-type]
        score_column=score_column,
        index=index,
    )
    test_normal_results_per_signal = get_results_per_signal(
        test_normal_results_table,  # type: ignore[bad-argument-type]
        score_column=score_column,
        index=index,
    )
    test_abnormal_results_per_signal = get_results_per_signal(
        test_abnormal_results_table,  # type: ignore[bad-argument-type]
        score_column=score_column,
        index=index,
    )

    for r in np.logspace(-5, 3, 9):
        y, scores = calculate_y_scores(
            r=r,
            norm_res=test_normal_results_per_signal,
            anom_res=test_abnormal_results_per_signal,
        )
        fpr, tpr, thresholds = metrics.roc_curve(y, scores)

        plt.plot(
            fpr,
            tpr,
            label=f"AUC {metrics.auc(fpr, tpr):.3f}, r={r:.1e}",
        )

    plt.legend()
    plt.title("FPR - TPR | Aggregation per signal")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    x = np.linspace(0, 1, 2)
    plt.plot(x, x, "--")
    plt.show()

    # ====================================================================
    # === Signal plot ====================================================
    # ====================================================================

    t = 20
    plt.subplot(3, 1, 1)
    plt.title("train")
    c = plt.pcolormesh(np.sort(train_normal_results_per_signal, axis=1)[:, ::-1].T[:t])
    cbar = plt.colorbar()
    cbar.set_label("anomaly score")
    plt.ylabel(f"top-{t} frames\nwith high anomaly score")

    plt.subplot(3, 1, 2)
    plt.title("test normal")
    plt.pcolormesh(
        np.sort(test_normal_results_per_signal, axis=1)[:, ::-1].T[:t],
        norm=c.norm,
        cmap=c.cmap,
    )
    cbar = plt.colorbar()
    cbar.set_label("anomaly score")
    plt.ylabel(f"top-{t} frames\nwith anomaly score")

    plt.subplot(3, 1, 3)
    plt.title("test abnormal")
    plt.pcolormesh(
        np.sort(test_abnormal_results_per_signal, axis=1)[:, ::-1].T[:t],
        norm=c.norm,
        cmap=c.cmap,
    )
    cbar = plt.colorbar()
    cbar.set_label("anomaly score")
    plt.ylabel(f"top-{t} frames\nwith high anomaly score")
    plt.xlabel("signal index")

    plt.suptitle("Distribution of anomaly score across all signals")
    plt.subplots_adjust(hspace=0.5)
    plt.show()
