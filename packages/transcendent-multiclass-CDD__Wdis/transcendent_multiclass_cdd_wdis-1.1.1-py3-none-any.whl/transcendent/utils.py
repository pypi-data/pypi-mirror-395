# -*- coding: utf-8 -*-

"""
utils.py
~~~~~~~~

Helper functions for setting up the environment.

"""

from sklearn.metrics import roc_auc_score
import argparse
from itertools import product
import logging
import multiprocessing as mp
import sys
from multiprocessing import shared_memory
from pprint import pformat
import numpy as np
from itertools import chain


from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
)
from termcolor import colored


# Allocate shared memory for multiprocessing
def alloc_shm(data):
    data_shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    data_arr = np.ndarray(data.shape, dtype=data.dtype, buffer=data_shm.buf)
    np.copyto(data_arr, data)
    return data_shm, (data_shm.name, data.shape, data.dtype)


def close_and_unlink_shm(shm_name):
    existing_data_shm = shared_memory.SharedMemory(name=shm_name)
    existing_data_shm.close()
    existing_data_shm.unlink()


def close_shm(shm_name):
    existing_data_shm = shared_memory.SharedMemory(name=shm_name)
    existing_data_shm.close()


def load_existing_shm(shm_name, shm_shape, shm_dtype):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    return existing_shm, np.ndarray(shm_shape, dtype=shm_dtype, buffer=existing_shm.buf)


def configure_logger():
    class SpecialFormatter(logging.Formatter):
        FORMATS = {
            logging.DEBUG: logging._STYLES["{"][0](colored("[*] {message}", "blue")),
            logging.INFO: logging._STYLES["{"][0](colored("[*] {message}", "cyan")),
            logging.WARNING: logging._STYLES["{"][0](
                colored("[!] {message}", "yellow")
            ),
            logging.ERROR: logging._STYLES["{"][0](colored("[!] {message}", "red")),
            logging.CRITICAL: logging._STYLES["{"][0](
                colored("[!] {message}", "white", "on_red")
            ),
            "DEFAULT": logging._STYLES["{"][0]("[ ] {message}"),
        }

        def format(self, record):
            self._style = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
            return logging.Formatter.format(self, record)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(SpecialFormatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)


def parse_args():
    """Parse the command line configuration for a particular run.

    See Also:
        - `data.load_features`
        - `thresholding.find_quartile_thresholds`
        - `thresholding.find_random_search_thresholds`
        - `thresholding.sort_by_predicted_label`
        - `thresholding.get_performance_with_rejection`

    Returns:
        argparse.Namespace: A set of parsed arguments.

    """
    p = argparse.ArgumentParser()

    # Dataset options
    (
        p.add_argument(
            "--dataset",
            default="",
            help="The unified JSON dataset (X.json, Y.json) to split",
        ),
    )
    p.add_argument("--train", default="", help="The training set to use.")
    p.add_argument("--test", default="", help="The testing set to use.")

    # Calibration options
    p.add_argument(
        "-k",
        "--folds",
        default=10,
        type=int,
        help="The number of folds to use during calibration.",
    )
    p.add_argument(
        "-n",
        "--ncpu",
        default=-2,
        type=int,
        help="The number of processes to use. "
        "Negative values are interpreted as (`mpu.cpu_count()` "
        "- abs(args.ncpu))",
    )
    p.add_argument(
        "--pval-consider",
        default="full-train",
        choices=["full-train", "cal-only"],
        help="The ncms to consider when generating p values.",
    )

    # Thresholding options
    p.add_argument(
        "-t",
        "--thresholds",
        default="quartiles",
        choices=["quartiles", "random-search", "constrained-search", "full-search"],
        help="The type of thresholds to use.",
    )

    p.add_argument(
        "-c",
        "--criteria",
        default="cred",
        choices=["cred", "conf", "cred+conf"],
        help="The p-values to threshold on.",
    )

    # Sub-arguments for --thresholds=quartiles
    p.add_argument(
        "--q-consider",  # default='correct',
        choices=["correct", "incorrect", "all"],
        help="Which predictions to select quartiles from.",
    )

    # Sub-arguments for --thresholds=random-search
    p.add_argument(
        "--rs-max",  # default='f1_k,kept_total_perc',
        help="The performance metric(s) to maximise (comma sep).",
    )
    p.add_argument(
        "--rs-min",  # default='f1_r',
        help="The performance metric(s) to minimise (comma sep).",
    )
    p.add_argument(
        "--rs-ceiling",  # default='0.25',
        help="The maximum total rejections that is acceptable. "
        "Either a float (for `total_reject_perc` or comma "
        "separated key:value pairs "
        "(e.g., 'total_reject_perc:0.25,f1_r:0.8')",
    )
    p.add_argument(
        "--rs-samples",
        type=int,  # default=100,
        help="The number of sample selections to make.",
    )

    # Sub-arguments for --thresholds=constrained-search
    p.add_argument(
        "--cs-max",  # default='f1_k:0.99',
        help="The performance metric(s) to maximise. "
        'Comma separated key:value pairs (e.g., "f1_k:0.99")',
    )
    p.add_argument(
        "--cs-con",  # default='kept_total_perc:0.75',
        help="The performance metric(s) to constrain. "
        'Comma separated key:value pairs (e.g., "kept_total_perc:0.75")',
    )
    args = p.parse_args()

    try:
        args.rs_ceiling = float(args.rs_ceiling)
    except (TypeError, ValueError):
        pass  # Leave it as a string (e.g., 'total_reject_perc:0.25') or None

    # Resolve ncpu value (negative values are interpreted as
    # mp.cpu_count() - abs(args.ncpu)
    args.ncpu = args.ncpu if args.ncpu > 0 else mp.cpu_count() + args.ncpu
    if args.ncpu < 0:
        raise ValueError("Invalid ncpu value.")

    logging.warning("Running with configuration:\n" + pformat(vars(args)))
    return args


def print_clf_perf(y_true, y_pred):
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    # f1 = roc_auc_score(y_true, y_pred)
    return (f1, precision, recall)


def print_clf_perf_multiclass(y_true, y_pred):
    # Precision (macro, micro, weighted)
    precision_macro = precision_score(y_true, y_pred, average="macro")
    precision_micro = precision_score(y_true, y_pred, average="micro")
    precision_weighted = precision_score(y_true, y_pred, average="weighted")

    # Recall (macro, micro, weighted)
    recall_macro = recall_score(y_true, y_pred, average="macro")
    recall_micro = recall_score(y_true, y_pred, average="micro")
    recall_weighted = recall_score(y_true, y_pred, average="weighted")

    # F1-score (macro, micro, weighted)
    f1_macro = f1_score(y_true, y_pred, average="macro")
    f1_micro = f1_score(y_true, y_pred, average="micro")
    f1_weighted = f1_score(y_true, y_pred, average="weighted")

    # print("=== Precision ===")
    # print(f"Macro:    {precision_macro:.4f}")
    # print(f"Micro:    {precision_micro:.4f}")
    # print(f"Weighted: {precision_weighted:.4f}\n")

    # print("=== Recall ===")
    # print(f"Macro:    {recall_macro:.4f}")
    # print(f"Micro:    {recall_micro:.4f}")
    # print(f"Weighted: {recall_weighted:.4f}\n")

    # print("=== F1-score ===")
    # print(f"Macro:    {f1_macro:.4f}")
    # print(f"Micro:    {f1_micro:.4f}")
    # print(f"Weighted: {f1_weighted:.4f}")

    # print("=== Accuracy ===")
    # print(f"Accuracy: {accuracy_score(y_true, y_pred)}")
    return (
        (f1_macro, f1_micro, f1_weighted),
        (precision_macro, precision_micro, precision_weighted),
        (recall_macro, recall_micro, recall_weighted),
    )


def print_perf(perf):
    def flatten(l):
        return l  # [x for sub in l for x in sub]

    for model in perf.keys():
        print("MODEL PERF:", model)

        # ---------------------------------------------------
        # prop_train_perf = flatten(perf[model]["proper_train"])
        # perf_str = " & ".join(f"{x:.4f}" for x in prop_train_perf)

        # cal_perf = flatten(perf[model]["cal"])
        # perf_str = perf_str + " & " + " & ".join(f"{x:.4f}" for x in cal_perf)  + " \\\\"
        # print("Proper Train + Cal Perf:\n", perf_str)

        # ---------------------------------------------------
        train_perf = perf[model]["train"]
        perf_str = " & ".join(f"{x:.2f}" for x in train_perf)

        test_perf = perf[model]["test"]
        perf_str = (
            perf_str + " & " + " & ".join(f"{x:.2f}" for x in test_perf) + " \\\\"
        )
        print("Train + Test Perf:\n", perf_str)

        # ---------------------------------------------------
        # threshold_perf = perf[model]["cal_threshold"]
        # # perf_str = " & ".join(f"{np.avg(x):.2f} $\pm$ {np.std(x):.2f}" for x in threshold_perf)
        # perf_str = " & ".join(f"{x:.2}" for x in threshold_perf)

        # test_threshold_perf = perf[model]["test_threshold"]
        # perf_str = perf_str + " & " + " & ".join(f"{x:.2}" for x in test_threshold_perf) + " \\\\"
        # print("Threshold Perf:\n", perf_str)


def print_perf_multiclass(perf):
    def flatten(l):
        return [x for sub in l for x in sub]

    for model in perf.keys():
        print("MODEL PERF:", model)

        # ---------------------------------------------------
        prop_train_perf = flatten(perf[model]["proper_train"])
        perf_str = " & ".join(f"{x:.2f}" for x in prop_train_perf)

        cal_perf = flatten(perf[model]["cal"])
        perf_str = perf_str + " & " + " & ".join(f"{x:.2f}" for x in cal_perf) + " \\\\"
        print("Proper Train + Cal Perf:\n", perf_str)

        # ---------------------------------------------------
        train_perf = flatten(perf[model]["train"])
        perf_str = " & ".join(f"{x:.2f}" for x in train_perf)

        test_perf = flatten(perf[model]["test"])
        perf_str = (
            perf_str + " & " + " & ".join(f"{x:.2f}" for x in test_perf) + " \\\\"
        )
        print("Train + Test Perf:\n", perf_str)

        # ---------------------------------------------------
        threshold_perf = perf[model]["cal_threshold"]
        # perf_str = " & ".join(f"{np.avg(x):.2f} $\pm$ {np.std(x):.2f}" for x in threshold_perf)
        perf_str = " & ".join(f"{x:.2}" for x in threshold_perf)

        test_threshold_perf = perf[model]["test_threshold"]
        perf_str = (
            perf_str
            + " & "
            + " & ".join(f"{x:.2}" for x in test_threshold_perf)
            + " \\\\"
        )
        print("Threshold Perf:\n", perf_str)


def gb_gs_best_params(gs_results):
    param_grid = {
        "num_iterations": [50, 100, 200, 500],
        "learning_rate": [0.05, 0.1],  # Step size shrinkage
        "feature_fraction": [0.8, 1.0],  # Column subsampling
        "bagging_fraction": [0.8, 1.0],  # Row subsampling
    }
    keys = list(param_grid.keys())
    param_list = [dict(zip(keys, values)) for values in product(*param_grid.values())]
    multi_logloss_means = [res["valid multi_logloss-mean"] for res in gs_results]
    best_index = np.argmin(multi_logloss_means)
    return param_list[best_index]
