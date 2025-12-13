import os
from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
)
import seaborn as sns


# def find_best_threshold(p_value_cal_dist, model_name, saved_data_folder):
#     thresholds = np.linspace(0, 1, 1000)

#     unique_cal_families = np.unique(p_value_cal_dist["y_cal"])

#     f1s, best_pvalue_t, precisions, recalls = [], {}, [], []
#     for family in unique_cal_families:
#         f1_f = []
#         precision_s, recall_s = [], []

#         mask = p_value_cal_dist["y_cal"] == family
#         y_true_f = (~p_value_cal_dist["Correct prediction"])[mask]
#         cal_cred_f = (p_value_cal_dist["cal_cred"])[mask]

#         # Compute F1 scores for each threshold
#         for threshold in thresholds:
#             # Predicted drift: 1 if p-value is below threshold
#             y_pred = cal_cred_f <= threshold
#             if any(y_pred):
#                 f1 = f1_score(y_true_f, y_pred)
#                 f1_f.append(f1)
#                 tn, fp, fn, tp = confusion_matrix(y_true_f, y_pred, labels=[0, 1]).ravel()

#                 p = tp / (tp + fp) if (tp + fp) > 0 else 0
#                 r = tp / (tp + fn) if (tp + fn) > 0 else 0
#                 precision_s.append(p)
#                 recall_s.append(r)

#         max_f1 = max(f1_f)
#         best_pvalue_t[family] = thresholds[np.argmax(f1_f)]
#         f1s.append(max_f1)
#         precisions.append(precision_s[np.argmax(f1_f)])
#         recalls.append(recall_s[np.argmax(f1_f)])

#     #print("Precision", precision, "Recall", recall)
#     plot_alpha_assessment(p_value_cal_dist, model_name, saved_data_folder)
#     return best_pvalue_t, max_f1, 0, 0, precisions, recalls


def find_best_threshold(p_value_cal_dist, model_name, saved_data_folder):
    thresholds = np.linspace(0, 1, 1000)

    f1_s, fpr_s, fnr_s = [], [], []
    precision_s, recall_s = [], []
    y_true = ~p_value_cal_dist["Correct prediction"]

    # Compute F1 scores for each threshold
    for threshold in thresholds:
        # Predicted drift: 1 if p-value is below threshold
        y_pred = p_value_cal_dist["cal_cred"] <= threshold
        if any(y_pred):
            f1 = f1_score(y_true, y_pred)
            f1_s.append(f1)
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
            fpr = fp / (fp + tn)
            fnr = fn / (fn + tp)
            fpr_s.append(fpr)
            fnr_s.append(fnr)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            precision_s.append(precision)
            recall_s.append(recall)

    max_f1 = max(f1_s)
    best_pvalue_t = thresholds[np.argmax(f1_s)]
    fpr = fpr_s[np.argmax(f1_s)]
    fnr = fnr_s[np.argmax(f1_s)]
    # print("F1", max_f1, "FPR", fpr, "FNR", fnr, "P-val T", best_pvalue_t)
    precision = precision_s[np.argmax(f1_s)]
    recall = recall_s[np.argmax(f1_s)]
    plot_alpha_assessment(p_value_cal_dist, model_name, saved_data_folder)
    return best_pvalue_t, max_f1, fpr, fnr, precision, recall


def plot_alpha_assessment(p_value_cal_dist, model_name, saved_data_folder):
    plt.figure()
    sns.boxplot(
        p_value_cal_dist,
        y="cal_cred",
        x="Correct prediction",
        orient="v",
    )
    plt.ylabel("p-value", fontsize=20)
    plt.xlabel("Correct prediction", fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.savefig(
        os.path.join(saved_data_folder, f"cred_dist_cal_{model_name}.png"),
        dpi=300,
        bbox_inches="tight",
    )


# def print_pval_threshold_perf(save_dict, pval, fig_name):

#     unique_cal_families = np.unique(save_dict["y_test_pred"])


#     f1s, precisions, recalls = {}, [], []
#     for family in unique_cal_families:
#         mask = save_dict["y_test_pred"] == family
#         y_true_f = (~save_dict["Correct prediction"])[mask]

#         pval_t = pval[family] if family in pval.keys() else 0.05
#         y_pred_f = np.array(save_dict["cred"])[mask] <= pval_t

#         # save_dict["Drifting"] = y_pred_f

#         if any(y_pred_f):
#             f1 = f1_score(y_true_f, y_pred_f)
#             tn, fp, fn, tp = confusion_matrix(y_true_f, y_pred_f, labels=[0, 1]).ravel()

#             precision = tp / (tp + fp) if (tp + fp) > 0 else 0
#             recall = tp / (tp + fn) if (tp + fn) > 0 else 0
#             #print("Precision", precision, "Recall", recall)
#             f1s[family] = f1
#             precisions.append(precision)
#             recalls.append(recall)


#     # plt.figure()
#     # sns.violinplot(
#     #     data=save_dict,
#     #     y="cred",
#     #     x="Drifting",
#     #     hue="Correct prediction",
#     #     orient="v",
#     # )
#     # plt.ylabel("p-value")
#     # plt.savefig(fig_name)
#     return f1s, 0, 0, precisions, recalls


def print_pval_threshold_perf(save_dict, pval, fig_name):
    y_true = ~save_dict["Correct prediction"]
    # pval = pval_t[model_name]
    y_pred = np.array(save_dict["cred"]) <= pval
    save_dict["Drifting"] = y_pred

    f1 = f1_score(y_true, y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    plt.figure()
    sns.violinplot(
        data=save_dict,
        y="cred",
        x="Drifting",
        hue="Correct prediction",
        orient="v",
    )
    plt.ylabel("p-value", fontsize=20)
    plt.xlabel("Drifting", fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=18)
    plt.ylim(0, 1)  # clip the violin visually at 1
    plt.tight_layout()
    plt.savefig(fig_name, dpi=300, bbox_inches="tight")
    return f1, fpr, fnr, precision, recall
