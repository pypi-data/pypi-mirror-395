import pytest
import pandas as pd
from haystack_ml_stack import utils
import numpy as np


def test_sigmoid():
    values_to_test = np.array([-1, 0, 1])
    expected = np.array([0.26894142136992605, 0.5, 0.731058578630074])
    actual = utils.sigmoid(values_to_test)
    assert np.isclose(actual, expected).all()


def test_prob_to_logodds():
    values_to_test = np.array([0.25, 0.5, 0.75])
    expected = np.array([-1.0986122886681096, 0, 1.0986122886681096])
    actual = utils.prob_to_logodds(values_to_test)
    assert np.isclose(actual, expected).all(), print(actual - expected)


def test_generic_beta_adjust_features():
    data_to_test = pd.DataFrame(
        {
            "STREAM_AUTOPLAY_24H_TOTAL_ATTEMPTS": [1, 2],
            "STREAM_AUTOPLAY_24H_TOTAL_WATCHED": [0, 1],
            "STREAM_24H_TOTAL_SELECTS_UP_TO_4_BROWSED": [1, 1],
            "STREAM_24H_TOTAL_SELECTS_AND_WATCHED_UP_TO_4_BROWSED": [0, 1],
            "STREAM_24H_TOTAL_BROWSED_UP_TO_4_BROWSED": [2, 0],
        },
        dtype=float,
    )
    actual = utils.generic_beta_adjust_features(
        data=data_to_test,
        prefix="STREAM",
        pwatched_beta_params={"AUTOPLAY_24H": (2, 1)},
        pselect_beta_params={"24H": (1, 1)},
        pslw_beta_params={"24H": (0.5, 1)},
        use_low_sample_flags=True,
    )
    # print(actual)
    expected = pd.DataFrame(
        {
            "STREAM_AUTOPLAY_24H_ADJ_PWATCHED": [
                (0 + 2) / (1 + 2 + 1),
                (1 + 2) / (2 + 2 + 1),
            ],
            "STREAM_24H_ADJ_PSELECT_UP_TO_4_BROWSED": [
                (1 + 1) / (1 + 2 + 1 + 1),
                (1 + 1) / (1 + 0 + 1 + 1),
            ],
            "STREAM_24H_ADJ_PSLW_UP_TO_4_BROWSED": [
                (0 + 0.5) / (1 + 2 + 0.5 + 1),
                (1 + 0.5) / (1 + 0 + 0.5 + 1),
            ],
            "STREAM_24H_PSelNotW_UP_TO_4_BROWSED": [
                (1 + 1) / (1 + 2 + 1 + 1) - (0 + 0.5) / (1 + 2 + 0.5 + 1),
                (1 + 1) / (1 + 0 + 1 + 1) - (1 + 0.5) / (1 + 0 + 0.5 + 1),
            ],
            "STREAM_AUTOPLAY_24H_LOW_SAMPLE": [1, 1],
            "STREAM_24H_PSELECT_LOW_SAMPLE_UP_TO_4_BROWSED": [1, 1],
        }
    )
    assert (actual[expected.columns] == expected).all(axis=None), actual - expected


def test_generic_logistic_predict():
    features = pd.DataFrame({"feat1": [0, 1, 2], "feat2": [3, 3, 5]}, dtype=float)
    coeffs = pd.Series({"feat1": 1, "feat2": 2})
    intercept = 1
    expected = utils.sigmoid(
        pd.Series([0 * 1 + 2 * 3, 1 * 1 + 2 * 3, 2 * 1 + 5 * 2]) + 1
    )
    actual = utils.generic_logistic_predict(
        data=features, coeffs=coeffs, intercept=intercept
    )
    assert (expected == actual).all(), actual - expected
