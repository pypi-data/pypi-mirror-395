import numpy as np
import pandas as pd
from asteroid_spinprops.ssolib.modelfit import (
    get_fit_params,
    get_residuals,
)

import asteroid_spinprops.ssolib.utils as utils


def errorbar_filtering(data, mlimit):
    """
    Filter out data points with large photometric uncertainties.

    Parameters
    -----------
    data : pd.DataFrame
        A single-row DataFrame where each column contains an array of values
        for a solar system object.
    mlimit : float
        Threshold value to filter out points with uncertainties greater than mlimit / 2.

    Returns
    -------
    data : pd.DataFrame
        Filtered DataFrame
    rejects : pd.DataFrame
        DataFrame containing the rejected measurements
    """
    errorbar_condition = data["csigmapsf"].values[0] <= mlimit / 2
    rejects = data.copy()

    for c in data.columns:
        if c not in ["index", "kast", "name"]:
            rejects.at[0, c] = data[c].values[0][~errorbar_condition]
            data.at[0, c] = data[c].values[0][errorbar_condition]

    return data, rejects


def projection_filtering(data):
    """
    Filters out photometric outliers in reduced magnitude space per filter using a 3 sigma criterion.

    Parameters
    -----------
    data : pd.DataFrame
        A single-row DataFrame where each column contains an array of values.
    Returns
    --------
    data : pd.DataFrame
        Filtered DataFrame
    rejects : pd.DataFrame
        DataFrame containing the rejected measurements
    """
    rejects = data.copy()
    valid_indices = []

    for f in np.unique(data["cfid"].values[0]):
        filter_mask = np.array(data["cfid"].values[0]) == f

        mean_val = np.mean(data["cmred"].values[0][filter_mask])
        std_val = np.std(data["cmred"].values[0][filter_mask])

        project_condition = (
            filter_mask
            & (data["cmred"].values[0] > mean_val - 3 * std_val)
            & (data["cmred"].values[0] < mean_val + 3 * std_val)
        )

        valid_indices.append(np.where(project_condition)[0])

    valid_indices = np.sort(
        np.concatenate([valid_indices[n] for n in range(len(valid_indices))])
    )

    dummy = np.ones(data["cfid"].values[0].shape, dtype=bool)
    dummy[valid_indices] = False

    for c in data.columns:
        if c not in ["index", "kast", "name"]:
            rejects.at[0, c] = data[c].values[0][dummy]
            data.at[0, c] = data[c].values[0][valid_indices]

    return data, rejects


def iterative_filtering(data, max_iter=10):
    """
    Iteratively removes outliers based on residuals from fitting the SHG1G2 mdoel until convergence.

    Parameters
    -----------
    data : pd.DataFrame
        A single-row DataFrame where each column contains an array of values.

    max_iter : int
        Maximum number of filtering iterations (default is 10).

    Returns
    --------
    data : pd.DataFrame
        Filtered DataFrame

    rejects : pd.DataFrame
        DataFrame containing the rejected measurements
    """
    rejects = data.copy()

    mask = np.ones_like(data["cfid"].values[0], dtype=bool)
    inloop_quants = {}
    reject_quants = {}

    for c in data.columns:
        if c not in ["index", "kast", "name"]:
            inloop_quants[c] = data[c].values[0]
            reject_quants[c] = np.array([])

    for niter in range(max_iter):
        prev_len = len(inloop_quants["cfid"])

        for k in inloop_quants.keys():
            reject_quants[k] = np.append(reject_quants[k], inloop_quants[k][~mask])
            inloop_quants[k] = inloop_quants[k][mask]

        mparams = get_fit_params(pd.DataFrame([inloop_quants]), "SHG1G2")
        try:
            residuals = get_residuals(pd.DataFrame([inloop_quants]), mparams)
        except KeyError:
            break
        mask = np.abs(residuals) < 3 * np.std(residuals)

        if prev_len == len(inloop_quants["Phase"][mask]):
            break

        for c in data.columns:
            if c not in ["index", "kast", "name"]:
                data.at[0, c] = inloop_quants[c]
                rejects.at[0, c] = reject_quants[c]
    return data, rejects


def lightcurve_filtering(data, window=10, maglim=0.6):
    """
    Filters out lightcurve points that deviate from the median by more than given mag limitation within time bins.

    Parameters
    ----------
    data : pd.DataFrame
        Single-row DataFrame
    window : float
        Time bin size (default is 10 days).
    maglim : float
        Magnitude deviation threshold from the median (default is 0.4 mag).

    Returns
    -------
    data : pd.DataFrame
        Filtered data
    rejects : pd.DataFrame
        DataFrame containing the rejected measurements
    """
    dummym, dummyt, dummyf, dummyi = [], [], [], []

    dates = data["cjd"].values[0]
    magnitudes = data["cmred"].values[0]
    filters = data["cfid"].values[0]
    indices = np.array([ind for ind in range(len(data["cfid"].values[0]))])

    ufilters = np.unique(filters)

    mag_pfilt = {}

    date0 = dates.min()
    date0_plus_step = date0 + window
    # TODO: Use np.digitize instead of this
    while date0 < dates.max():
        prev_ind = np.where(dates == utils.find_nearest(dates, date0))[0][0]
        plus_ten_index = np.where(dates == utils.find_nearest(dates, date0_plus_step))[
            0
        ][0]

        dummym.append(magnitudes[prev_ind:plus_ten_index])
        dummyt.append(dates[prev_ind:plus_ten_index])
        dummyf.append(filters[prev_ind:plus_ten_index])
        dummyi.append(indices[prev_ind:plus_ten_index])

        date0 = dates[plus_ten_index]
        date0_plus_step = date0_plus_step + window

    dummym.append(magnitudes[plus_ten_index:])
    dummyt.append(dates[plus_ten_index:])
    dummyf.append(filters[plus_ten_index:])
    dummyi.append(indices[plus_ten_index:])

    mag_binned, _, filt_binned, ind_binned = (
        np.asarray(dummym, dtype=object),
        np.asarray(dummyt, dtype=object),
        np.asarray(dummyf, dtype=object),
        np.asarray(dummyi, dtype=object),
    )

    for f in ufilters:
        dummymain, dummym, dummyt, dummydiff, dummyi = [], [], [], [], []
        for n in range(len(mag_binned)):
            fcond = filt_binned[n] == f
            dummymain.append(mag_binned[n][fcond])
            dummym.append(np.median(mag_binned[n][fcond]))
            dummydiff.append(
                np.max(mag_binned[n][fcond], initial=0)
                - np.min(mag_binned[n][fcond], initial=1e3)
            )
            dummyi.append(ind_binned[n][fcond])

        dummydiff = np.array(dummydiff)
        dummydiff[dummydiff == np.float64(-1000.0)] = 0

        mag_pfilt["medimag_{}".format(f)] = dummym
        mag_pfilt["mxmnmag_{}".format(f)] = dummydiff
        mag_pfilt["mag_{}".format(f)] = dummymain
        mag_pfilt["ind_{}".format(f)] = dummyi

    valid_indices = []
    reject_indices = []

    rejects = data.copy()

    for f in ufilters:
        for n in range(len(mag_binned)):
            bin_cond = (
                mag_pfilt["mag_{}".format(f)][n]
                > mag_pfilt["medimag_{}".format(f)][n] + maglim
            ) | (
                mag_pfilt["mag_{}".format(f)][n]
                < mag_pfilt["medimag_{}".format(f)][n] - maglim
            )
            valid_indices.append(mag_pfilt["ind_{}".format(f)][n][~bin_cond])
            reject_indices.append(mag_pfilt["ind_{}".format(f)][n][bin_cond])

    valid_indices = np.array(utils.flatten_list(valid_indices), dtype=int)
    reject_indices = np.array(utils.flatten_list(reject_indices), dtype=int)

    for c in data.columns:
        if c not in ["index", "kast", "name"]:
            rejects.at[0, c] = data[c].values[0][reject_indices]
            data.at[0, c] = data[c].values[0][valid_indices]

    data = utils.sort_by_cjd(data)

    return data, rejects
