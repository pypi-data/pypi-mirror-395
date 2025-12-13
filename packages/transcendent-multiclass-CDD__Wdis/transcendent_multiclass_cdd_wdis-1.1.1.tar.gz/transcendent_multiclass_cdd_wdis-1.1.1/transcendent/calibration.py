# -*- coding: utf-8 -*-

"""
calibration.py
~~~~~~~~~~~~~~

Functions for partitioning and training proper training and calibration sets.

"""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd


import transcendent.data as data
import transcendent.scores as scores


def train_calibration_ice(
    model, X_proper_train, X_cal, y_proper_train, y_cal, saved_data_folder="."
):
    """Train calibration set (for a single fold).

    Quite a bit of information is needed here for the later p-value
    computation and probability comparison. The returned dictionary has
    the following structure:

        'cred_p_val_cal_fold'  -->  # Calibration credibility p values
        'conf_p_val_cal_fold'  -->  # Calibration confidence p values
        'ncms_cal_fold'        -->  # Calibration NCMs
        'pred_cal_fold'        -->  # Calibration predictions
        'groundtruth_cal_fold' -->  # Calibration groundtruth
        'probas_cal_fold'      -->  # Calibration probabilities
        'pred_proba_cal_fold'  -->  # Calibration predictions

    Args:
        X_proper_train (np.ndarray): Features for the 'proper training
            set' partition.
        X_cal (np.ndarray): Features for a single calibration set
            partition.
        y_proper_train (np.ndarray): Ground truths for the 'proper
            training set' partition.
        y_cal (np.ndarray): Ground truths for a single calibration set
            partition.
        fold_index: An index to identify the current fold (used for caching).

    Returns:
        dict: Fold results, structure as in the docstring above.

    """
    # assert sum(y_cal.isin(y_proper_train)) == len(y_cal)
    # assert max(y_proper_train) >= max(y_cal)

    # print("UNIQUE YTRAIN", len(y_proper_train.unique()))
    # print("UNIQUE YCAL", len(y_cal.unique()))
    # print("MAX YCAL", max(y_cal))

    # Replacing the above code with Random Forest model
    # model_name = "model_cal.pkl"
    # model_name = os.path.join(saved_data_folder, model_name)

    model.fit(X_proper_train, y_proper_train)
    # data.cache_data(model, model_name)

    # Get ncms for calibration fold
    logging.debug("Getting calibration ncms")
    pred_cal_fold = model.predict(X_cal)

    # Compute p values for calibration fold
    logging.debug("Computing calibration p-values")

    saved_ncms_name = "ncms_cal.pkl"
    saved_ncms_name = os.path.join(saved_data_folder, saved_ncms_name)

    ncms_cal_fold = model.ncm(X_cal, y_cal)
    data.cache_data(ncms_cal_fold, saved_ncms_name)

    saved_pvals_name = "p_vals_cal.pkl"
    saved_pvals_name = os.path.join(saved_data_folder, saved_pvals_name)

    print("NCM", ncms_cal_fold)
    # df = pd.DataFrame({"NCM": ncms_cal_fold, "Seen family": y_cal}),
    # import seaborn as sns

    # plt.figure(figsize=(8, 6))
    # sns.violinplot(x="Seen family", y="NCM", data=df)
    # plt.ylabel("NCM")
    # # plt.title(f"NCM Distribution ({pe_set}, {criteria}, {split})")
    # plt.savefig(os.path.join(saved_data_folder, "NCM_OK.png"))
    # plt.close()

    p_val_cal_fold_dict = scores.compute_p_values_cred_and_conf(
        clf=model,
        train_ncms=ncms_cal_fold,
        y_train=y_cal,
        test_ncms=ncms_cal_fold,
        y_test=y_cal,
        X_test=X_cal,
    )
    data.cache_data(p_val_cal_fold_dict, saved_pvals_name)

    return {
        "cred_p_val_cal": p_val_cal_fold_dict["cred"],
        "conf_p_val_cal": p_val_cal_fold_dict["conf"],
        "ncms_cal": ncms_cal_fold,
        "pred_cal": pred_cal_fold,
        "groundtruth_cal": y_cal,
        # "best_knn": best_k,
        # "model": model.model,
    }
