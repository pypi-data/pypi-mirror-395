# -*- coding: utf-8 -*-
import time

from transcendent.utils import alloc_shm, load_existing_shm

"""
scores.py
~~~~~~~~~

Functions for producing the various scores used during conformal evaluation,
such as non-conformity measures, credibility and confidence p-values and
probabilities for comparison.

Note that the functions in this module currently only apply to producing
scores for a binary classification task and an SVM classifier. Different
settings and different classifiers will require their own functions for
generating non-conformity measures based on different intuitions.

"""

import logging

import numpy as np
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool


def compute_p_values_cred_and_conf(clf, train_ncms, y_train, test_ncms, y_test, X_test):
    return {
        "conf": len(X_test) * [0.0],  # Placeholder for confidence scores
        # "conf": compute_confidence_scores(clf, train_ncms, y_train, y_test, X_test),
        "cred": compute_credibility_scores(train_ncms, y_train, test_ncms, y_test),
    }


def creds(args):
    (shm_t, (i, n, m, op_y_labels)) = args
    (train_ncms_t, groundtruth_train_shm_t, ncms_shm_t) = shm_t

    train_ncms_shm, train_ncms = load_existing_shm(*train_ncms_t)
    groundtruth_train_shm, groundtruth_train = load_existing_shm(
        *groundtruth_train_shm_t
    )
    ncms_X_test_op_y_label_shm, ncms_X_test_op_y_label = load_existing_shm(*ncms_shm_t)

    def partial_f(single_ncm_test, single_y_test):
        return compute_single_cred_p_value(
            train_ncms=train_ncms,
            y_train=groundtruth_train,
            single_y_test=single_y_test,
            single_test_ncm=single_ncm_test,
        )

    res = 1 - max(
        [
            partial_f(single_ncm_test=ncm, single_y_test=op_y)
            for ncm, op_y in zip(
                [ncms_X_test_op_y_label[i + k * m] for k in range(n)], op_y_labels
            )
        ]
    )

    train_ncms_shm.close()
    groundtruth_train_shm.close()
    ncms_X_test_op_y_label_shm.close()
    return res


def compute_credibility_scores(train_ncms, y_train, test_ncms, y_test):
    return [
        compute_single_cred_p_value(
            train_ncms=train_ncms,
            y_train=y_train,
            single_test_ncm=ncm,
            single_y_test=y,
        )
        for ncm, y in tqdm(zip(test_ncms, y_test), total=len(y_test), desc="cred pvals")
    ]


def compute_confidence_scores(clf, train_ncms, y_train, y_test, X_test):
    unique_y_test_labels = np.unique(y_test)
    y_test_series = pd.Series(y_test, index=X_test.index)

    train_ncms_shm, train_ncms_shm_t = alloc_shm(train_ncms)
    groundtruth_train_shm, groundtruth_train_shm_t = alloc_shm(y_train)

    conf_X_test = []
    for y in tqdm(
        unique_y_test_labels, total=len(unique_y_test_labels), desc="label conf"
    ):
        op_y_labels = unique_y_test_labels[unique_y_test_labels != y]
        X_test_y = X_test[y_test_series == y]

        m = X_test_y.shape[0]
        n = len(op_y_labels)

        M = pd.concat([X_test_y] * n, ignore_index=True)
        Y = np.concat([np.full(m, op_y_label) for op_y_label in op_y_labels])

        ncms_X_test_op_y_label = clf.ncm(M, Y)
        ncm_shm, ncm_shm_t = alloc_shm(ncms_X_test_op_y_label)

        shm_t = (train_ncms_shm_t, groundtruth_train_shm_t, ncm_shm_t)
        with Pool() as p:
            conf_X_test_y = p.map(
                creds, [(shm_t, (i, n, m, op_y_labels)) for i in range(m)]
            )

        ncm_shm.close()
        ncm_shm.unlink()

        conf_X_test_y = pd.DataFrame(conf_X_test_y, index=X_test_y.index)
        conf_X_test.append(conf_X_test_y)

    train_ncms_shm.close()
    train_ncms_shm.unlink()
    groundtruth_train_shm.close()
    groundtruth_train_shm.unlink()

    _, conf_X_test = X_test.align(pd.concat(conf_X_test, axis=0), axis=0)
    return conf_X_test


def compute_single_cred_p_value(train_ncms, y_train, single_test_ncm, single_y_test):
    """Compute a single credibility p-value.

    Credibility p-values describe how 'conformal' a point is with respect to
    the other objects of that class. They're computed as the proportion of
    points with greater NCMs (the number of points _less conforming_ than the
    reference point) over the total number of points.

    Intuitively, a point predicted as malware which is the further away from
    the decision boundary than any other point will have the highest p-value
    out of all other malware points. It will have the smallest NCM (as it is
    the least _non-conforming_) and thus no other points will have a greater
    NCM and it will have a credibility p-value of 1.
    """

    mask = y_train == single_y_test
    single_cred_p_value = sum((train_ncms >= single_test_ncm) & (mask)) / sum(mask)
    return single_cred_p_value
