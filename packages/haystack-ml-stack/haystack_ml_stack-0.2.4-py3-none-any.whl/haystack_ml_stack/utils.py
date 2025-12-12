import pandas as pd
import numpy as np
import typing as _t


def stream_favorites_cleanup(
    stream,
    user_favorite_tags: list[str],
    user_favorite_authors: list[str],
    out: dict = None,
) -> dict:
    if out is None:
        out = {}
    stream_tags = stream.get("haystackTags", [])
    is_favorite_tag = (
        any(stream_tag in user_favorite_tags for stream_tag in stream_tags)
        if user_favorite_tags is not None
        else False
    )
    is_favorite_author = (
        stream.get("author", None) in user_favorite_authors
        if user_favorite_authors is not None
        else False
    )
    out["IS_FAVORITE_TAG"] = is_favorite_tag
    out["IS_FAVORITE_AUTHOR"] = is_favorite_author
    return out


def browsed_count_cleanups(
    stream,
    position_debiasing: _t.Literal["4_browsed", "all_browsed"] = "4_browsed",
    out: dict = None,
) -> dict:
    position_alias_mapping = {
        "0": "1ST_POS",
        "1": "2ND_POS",
        "2": "3RD_POS",
        "3+": "REST_POS",
    }
    if position_debiasing == "4_browsed":
        suffix = "_UP_TO_4_BROWSED"
    elif position_debiasing == "all_browsed":
        suffix = ""
    else:
        raise ValueError(f"Unexpected position debiasing '{position_debiasing}'.")
    browsed_count_obj = stream.get("PSELECT#24H", {}).get(position_debiasing, {})
    total_selects = 0
    total_browsed = 0
    total_selects_and_watched = 0
    if out is None:
        out = {}
    for position in position_alias_mapping.keys():
        pos_counts = browsed_count_obj.get(position, {})
        total_browsed += pos_counts.get("total_browsed", 0)
        total_selects += pos_counts.get("total_selects", 0)
        total_selects_and_watched += pos_counts.get("total_selects_and_watched", 0)
    if position_debiasing == "4_browsed":
        suffix = "_UP_TO_4_BROWSED"
    elif position_debiasing == "all_browsed":
        suffix = ""
    else:
        raise ValueError("Should not be here.")
    out[f"STREAM_24H_TOTAL_BROWSED{suffix}"] = total_browsed
    out[f"STREAM_24H_TOTAL_SELECTS{suffix}"] = total_selects
    out[f"STREAM_24H_TOTAL_SELECTS_AND_WATCHED{suffix}"] = total_selects_and_watched
    return out


def device_split_browsed_count_cleanups(
    stream,
    device_type: _t.Literal["TV", "MOBILE"],
    position_debiasing: _t.Literal["4_browsed", "all_browsed"] = "4_browsed",
    out: dict = None,
) -> dict:
    position_alias_mapping = {
        "0": "1ST_POS",
        "1": "2ND_POS",
        "2": "3RD_POS",
        "3+": "REST_POS",
    }
    if position_debiasing == "4_browsed":
        suffix = "_UP_TO_4_BROWSED"
    elif position_debiasing == "all_browsed":
        suffix = ""
    else:
        raise ValueError(f"Unexpected position debiasing '{position_debiasing}'.")

    _validate_device_type(device_type)

    browsed_count_obj = stream.get(f"PSELECT#24H#{device_type}", {}).get(
        position_debiasing, {}
    )
    total_selects = 0
    total_browsed = 0
    total_selects_and_watched = 0
    if out is None:
        out = {}
    for position, alias in position_alias_mapping.items():
        pos_counts = browsed_count_obj.get(position, {})
        total_browsed = pos_counts.get("total_browsed", 0)
        total_selects = pos_counts.get("total_selects", 0)
        total_selects_and_watched = pos_counts.get("total_selects_and_watched", 0)
        out[f"STREAM_{alias}_{device_type}_24H_TOTAL_BROWSED{suffix}"] = total_browsed
        out[f"STREAM_{alias}_{device_type}_24H_TOTAL_SELECTS{suffix}"] = total_selects
        out[f"STREAM_{alias}_{device_type}_24H_TOTAL_SELECTS_AND_WATCHED{suffix}"] = (
            total_selects_and_watched
        )
    return out


def watched_count_cleanups(
    stream, entry_contexts: list[str] = None, out: dict = None
) -> dict:
    if entry_contexts is None:
        entry_contexts = [
            "autoplay",
            "choose next",
            "ch swtch",
            "sel thumb",
            "launch first in session",
        ]
    _validate_pwatched_entry_context(entry_contexts)

    counts_obj = stream.get(f"PWATCHED#24H", {})
    if out is None:
        out = {}
    for entry_context in entry_contexts:
        attempts = counts_obj.get(entry_context, {}).get("attempts", 0)
        watched = counts_obj.get(entry_context, {}).get("watched", 0)
        context_key = entry_context if "launch" not in entry_context else "launch"
        context_key = context_key.upper().replace(" ", "_")
        out[f"STREAM_{context_key}_24H_TOTAL_WATCHED"] = watched
        out[f"STREAM_{context_key}_24H_TOTAL_ATTEMPTS"] = attempts
    return out


def device_watched_count_cleanups(
    stream, device_type: str, entry_contexts: list[str] = None, out: dict = None
) -> dict:
    if entry_contexts is None:
        entry_contexts = [
            "autoplay",
            "choose next",
            "ch swtch",
            "sel thumb",
            "launch first in session",
        ]

    _validate_pwatched_entry_context(entry_contexts)
    _validate_device_type(device_type)

    counts_obj = stream.get(f"PWATCHED#24H#{device_type}", {})
    if out is None:
        out = {}
    for entry_context in entry_contexts:
        attempts = counts_obj.get(entry_context, {}).get("attempts", 0)
        watched = counts_obj.get(entry_context, {}).get("watched", 0)
        context_key = entry_context if "launch" not in entry_context else "launch"
        context_key = context_key.upper().replace(" ", "_")
        out[f"STREAM_{context_key}_{device_type}_24H_TOTAL_WATCHED"] = watched
        out[f"STREAM_{context_key}_{device_type}_24H_TOTAL_ATTEMPTS"] = attempts
    return out


def generic_beta_adjust_features(
    data: pd.DataFrame,
    prefix: str,
    pwatched_beta_params: dict = None,
    pselect_beta_params: dict = None,
    pslw_beta_params: dict = None,
    use_low_sample_flags: bool = False,
    low_sample_threshold: int = 3,
    use_attempt_features: bool = False,
    max_attempt_cap: int = 100,
    debiased_pselect: bool = True,
    use_logodds: bool = False,
) -> pd.DataFrame:
    features = {}
    counting_feature_cols = [
        c
        for c in data.columns
        if "TOTAL_WATCHED" in c
        or "TOTAL_ATTEMPTS" in c
        or "SELECT" in c
        or "BROWSED" in c
    ]
    data_arr = data[counting_feature_cols].to_numpy(dtype=float)
    col_to_idx = {col: i for i, col in enumerate(counting_feature_cols)}
    if pwatched_beta_params is not None:
        for context, (alpha, beta) in pwatched_beta_params.items():
            total_watched = np.nan_to_num(
                data_arr[:, col_to_idx[f"{prefix}_{context}_TOTAL_WATCHED"]]
            )
            total_attempts = np.nan_to_num(
                data_arr[:, col_to_idx[f"{prefix}_{context}_TOTAL_ATTEMPTS"]]
            )
            features[f"{prefix}_{context}_ADJ_PWATCHED"] = (total_watched + alpha) / (
                total_attempts + alpha + beta
            )
            low_sample_arr = np.empty_like(total_attempts, dtype=float)
            if use_low_sample_flags:
                features[f"{prefix}_{context}_LOW_SAMPLE"] = np.less_equal(
                    total_attempts, low_sample_threshold, out=low_sample_arr
                )
            if use_attempt_features:
                features[f"{prefix}_{context}_ATTEMPTS"] = np.clip(
                    total_attempts, a_min=None, a_max=max_attempt_cap
                )

    debias_suffix = "_UP_TO_4_BROWSED" if debiased_pselect else ""
    if pselect_beta_params is not None or pslw_beta_params is not None:
        for key, (alpha, beta) in pselect_beta_params.items():
            total_selects_idx = col_to_idx[
                f"{prefix}_{key}_TOTAL_SELECTS{debias_suffix}"
            ]
            total_browsed_idx = col_to_idx[
                f"{prefix}_{key}_TOTAL_BROWSED{debias_suffix}"
            ]
            total_slw_idx = col_to_idx[
                f"{prefix}_{key}_TOTAL_SELECTS_AND_WATCHED{debias_suffix}"
            ]
            total_selects = np.nan_to_num(data_arr[:, total_selects_idx])
            total_browsed = np.nan_to_num(data_arr[:, total_browsed_idx])
            total_slw = np.nan_to_num(data_arr[:, total_slw_idx])
            if pselect_beta_params is not None:
                features[f"{prefix}_{key}_ADJ_PSELECT{debias_suffix}"] = (
                    total_selects + alpha
                ) / (total_selects + total_browsed + alpha + beta)
            if use_low_sample_flags:
                low_sample_arr = np.empty_like(total_selects, dtype=float)
                features[f"{prefix}_{key}_PSELECT_LOW_SAMPLE{debias_suffix}"] = (
                    np.less_equal(
                        total_selects + total_browsed,
                        low_sample_threshold,
                        out=low_sample_arr,
                    )
                )
            if use_attempt_features:
                features[f"{prefix}_{key}_PSELECT_ATTEMPTS{debias_suffix}"] = np.clip(
                    total_selects + total_browsed, a_min=0, a_max=max_attempt_cap
                )
            if pslw_beta_params is not None:
                pslw_alpha, pslw_beta = pslw_beta_params[key]
                features[f"{prefix}_{key}_ADJ_PSLW{debias_suffix}"] = (
                    total_slw + pslw_alpha
                ) / (total_selects + total_browsed + pslw_alpha + pslw_beta)
            if pslw_beta_params is not None and pselect_beta_params is not None:
                features[f"{prefix}_{key}_PSelNotW{debias_suffix}"] = (
                    features[f"{prefix}_{key}_ADJ_PSELECT{debias_suffix}"]
                    - features[f"{prefix}_{key}_ADJ_PSLW{debias_suffix}"]
                )

    adjusted_feats = pd.DataFrame(features, index=data.index)
    if use_logodds:
        arr = adjusted_feats.to_numpy()
        col_idxs = [
            i
            for i, c in enumerate(adjusted_feats.columns)
            if ("PSELECT" in c or "PSLW" in c or "PWATCHED" in c or "PSelNotW" in c)
            and ("LOW_SAMPLE" not in c and "ATTEMPTS" not in c)
        ]
        arr[:, col_idxs] = prob_to_logodds(
            np.clip(arr[:, col_idxs], a_min=0.001, a_max=None)
        )
    return adjusted_feats


def prob_to_logodds(prob: float) -> float:
    return np.log(prob) - np.log(1 - prob)


def scale_preds(
    preds: pd.Series,
    original_mean: float,
    original_std: float,
    target_mean: float,
    target_std: float,
) -> pd.Series:
    z_score = (preds - original_mean) / original_std
    return z_score * target_std + target_mean


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


def generic_logistic_predict(
    data: pd.DataFrame, coeffs: pd.Series, intercept: float
) -> pd.Series:
    scores = (data[coeffs.index] * coeffs).sum(axis=1) + intercept
    raw_arr = scores.to_numpy()
    raw_arr[:] = sigmoid(raw_arr)
    return scores


def _validate_device_type(device_type: str):
    if device_type not in ("TV", "MOBILE"):
        raise ValueError(f"Invalid device type '{device_type}")


def _validate_pwatched_entry_context(entry_contexts: list[str]):
    valid_contexts = [
        "autoplay",
        "choose next",
        "ch swtch",
        "sel thumb",
        "launch first in session",
    ]
    invalid_contexts = [c for c in entry_contexts if c not in valid_contexts]
    if invalid_contexts:
        raise ValueError(f"Invalid entry contexts found: {invalid_contexts}")
