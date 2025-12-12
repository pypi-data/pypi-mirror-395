import numpy as np
import pandas as pd

import asteroid_spinprops.ssolib.utils as utils
import asteroid_spinprops.ssolib.periodest as periodest

from fink_utils.sso.spins import (
    estimate_sso_params,
    func_hg1g2_with_spin,
)
from asteroid_spinprops.ssolib.periodest import (
    get_multiterm_period_estimate,
)


def get_fit_params(
    data,
    flavor,
    shg1g2_constrained=True,
    period_blind=True,
    pole_blind=True,
    p0=None,
    alt_spin=False,
    period_in=None,
    period_quality_flag=False,
    terminator=False,
):
    """
    Fit a small solar system object's photometric data using SHG1G2 or SOCCA models.

    This function can perform either a standard SHG1G2 fit or a spin- and
    shape-constrained SOCCA fit, optionally including blind scans over
    initial pole positions and periods. It supports filtering data by survey.

    Parameters
    ----------
    data : pandas.DataFrame single-row
        Input dataset containing photometry and geometry with columns:
        - 'cmred': reduced magnitudes
        - 'csigmapsf': uncertainties
        - 'Phase': solar phase angles (deg)
        - 'cfid': filter IDs
        - 'ra', 'dec': coordinates (deg)
        - 'cjd': observation times (light-time corrected)
        Optional (for terminator fits):
        - 'ra_s', 'dec_s': sub-solar point coordinates (deg)
    flavor : str
        Model type to fit. Must be 'SHG1G2' or 'SOCCA'.
    shg1g2_constrained : bool, optional
        Whether to constrain the SOCCA fit using a prior SHG1G2 solution. Default True.
    period_blind : bool, optional
        If True, perform a small grid search over initial periods. Default True.
    pole_blind : bool, optional
        If True, perform a grid search over 12 initial poles all over a sphere. Default True.
        If False, produce the sHG1G2 rms error landscape and initialize SOCCA poles on its local minima     
    p0 : list, optional
        Initial guess parameters for the fit. Required if `shg1g2_constrained=False`.
    alt_spin : bool, optional
        For SOCCA constrained fits, use the antipodal spin solution. Default False.
    period_in : float, optional
        Input synodic period (days) to override automatic estimation. Default None.
    period_quality_flag : bool, optional
        Provide bootstrap score, alias/true (0/1) flags and period fit rms for the period estimates
    terminator : bool, optional
        If True, include self-shading in the fit. Default False.

    Returns
    -------
    dict or tuple
        If `flavor='SHG1G2'`:
            dict
                Best-fit SHG1G2 parameters.
        If `flavor='SOCCA'`:
            dict
                Best-fit SOCCA parameters.

    Notes
    -----
    - For SOCCA fits with `shg1g2_constrained=True`, the function first performs
      a SHG1G2 fit to constrain H, G1, G2, and shape parameters.
    - Blind scans systematically vary initial pole positions and period to find
      the optimal fit when `blind_scan=True`.

    Raises
    ------
    ValueError
        If `flavor` is not 'SHG1G2' or 'SOCCA'.
    """

    if flavor == "SHG1G2":
        if p0 is None:
            Afit = estimate_sso_params(
                magpsf_red=data["cmred"].values[0],
                sigmapsf=data["csigmapsf"].values[0],
                phase=np.radians(data["Phase"].values[0]),
                filters=data["cfid"].values[0],
                ra=np.radians(data["ra"].values[0]),
                dec=np.radians(data["dec"].values[0]),
                model="SHG1G2",
            )

        if p0 is not None:
            Afit = estimate_sso_params(
                magpsf_red=data["cmred"].values[0],
                sigmapsf=data["csigmapsf"].values[0],
                phase=np.radians(data["Phase"].values[0]),
                filters=data["cfid"].values[0],
                ra=np.radians(data["ra"].values[0]),
                dec=np.radians(data["dec"].values[0]),
                model="SHG1G2",
                p0=p0,
            )

        return Afit
    if flavor == "SOCCA":
        if shg1g2_constrained is True:
            shg1g2_params = get_fit_params(
                data=data, flavor="SHG1G2"
            )
            try:
                residuals_dataframe = make_residuals_df(
                    data, model_parameters=shg1g2_params
                )
            except Exception:
                SOCCA_opt = {"Failed at period search preliminary steps": 1}
                return SOCCA_opt
            if period_in is None:
                # Period search boundaries (in days)
                pmin, pmax = 5e-2, 1e4
                try:
                    p_in, k_val, p_rms, signal_peaks, window_peaks = (
                        get_multiterm_period_estimate(
                            residuals_dataframe, p_min=pmin, p_max=pmax, k_free=True
                        )
                    )
                    if period_quality_flag:
                        _, Nbs = periodest.perform_residual_resampling(
                            resid_df=residuals_dataframe, p_min=pmin, p_max=pmax, k=int(k_val)
                            )
                except KeyError:
                    # If more than 10 terms are required switch to fast rotator:
                    pmin, pmax = 5e-3, 5e-2
                    try:
                        p_in, k_val, p_rms, signal_peaks, window_peaks = (
                            get_multiterm_period_estimate(
                                residuals_dataframe, p_min=pmin, p_max=pmax, k_free=True
                            )
                        )
                        if period_quality_flag:
                            _, Nbs = periodest.perform_residual_resampling(
                                resid_df=residuals_dataframe, p_min=pmin, p_max=pmax, k=int(k_val)
                                )
                    except Exception:
                        SOCCA_opt = {"Failed at period search after": 1}
                        return SOCCA_opt
                except IndexError:
                    SOCCA_opt = {"Failed at bootsrap sampling": 1}
                    return SOCCA_opt
                period_sy = p_in
            else:
                period_sy = period_in

            if period_blind is True:
                rms = []
                model = []

                period_scan = np.linspace(
                    period_sy - 20 / (24 * 60 * 60), period_sy + 20 / (24 * 60 * 60), 20
                )

                ra0, dec0 = shg1g2_params["alpha0"], shg1g2_params["delta0"]

                if pole_blind is True:
                    ra_init, dec_init = utils.generate_initial_points(
                        ra0, dec0, dec_shift=45
                    )

                else:
                    rarange = np.arange(0, 360, 10)
                    decrange = np.arange(-90, 90, 5)
                    rms_landscape = np.ones(shape=(len(rarange), len(decrange)))

                    for i, ra0 in enumerate(rarange):
                        for j, dec0 in enumerate(decrange):

                            all_residuals = []

                            for ff in np.unique(data["cfid"].values[0]):
                                cond_ff  = data["cfid"].values[0] == ff

                                pha = [np.radians(data["Phase"].values[0][cond_ff]),
                                    np.radians(data["ra"].values[0][cond_ff]),
                                    np.radians(data["dec"].values[0][cond_ff])]

                                H  = shg1g2_params[f"H_{ff}"]
                                G1 = shg1g2_params[f"G1_{ff}"]
                                G2 = shg1g2_params[f"G2_{ff}"]
                                R  = shg1g2_params["R"]

                                C = func_hg1g2_with_spin(pha, H, G1, G2, R,
                                                        np.radians(ra0), np.radians(dec0))

                                Obs = data["cmred"].values[0][cond_ff]

                                all_residuals.append(Obs - C)

                            all_residuals = np.concatenate(all_residuals)
                            rms_landscape[j, i] = np.sqrt(np.mean(all_residuals**2))

                    interp_vals = utils.gaussian_interpolate(rms_landscape, factor=4, sigma=1.0)
                    ny, nx = interp_vals.shape
                    [rarange[0], rarange[-1], decrange[0], decrange[-1]]
                    ra_vals  = np.linspace(rarange.min(),  rarange.max(),  nx)
                    dec_vals = np.linspace(decrange.min(), decrange.max(), ny)
                    ys, xs = utils.detect_local_minima(interp_vals)
                    ra_minima  = ra_vals[xs]
                    dec_minima = dec_vals[ys]

                    ra_init = ra_minima
                    dec_init = dec_minima

                H_key = next(
                    (f"H_{i}" for i in range(1, 7) if f"H_{i}" in shg1g2_params),
                    None,
                )

                for ra, dec in zip(ra_init, dec_init):
                    for period_in in period_scan:
                        p_in = [
                            shg1g2_params[H_key],
                            0.15,
                            0.15,  # G1,2
                            np.radians(ra),
                            np.radians(dec),
                            period_in,  # in days
                            shg1g2_params["a_b"],
                            shg1g2_params["a_c"],
                            0.1,
                        ]  # phi 0

                        SOCCA = get_fit_params(
                            data,
                            "SOCCA",
                            shg1g2_constrained=False,
                            p0=p_in,
                            terminator=terminator,
                        )
                        try:
                            rms.append(SOCCA["rms"])
                            model.append(SOCCA)
                        except Exception:
                            continue
                try:
                    rms = np.array(rms)
                    SOCCA_opt = model[rms.argmin()]
                    if period_quality_flag:
                        try:
                            DeltaF1 = signal_peaks[1] - signal_peaks[2]
                            f_obs = 2 / period_sy
                            y_trumpet = utils.trumpet(
                                DeltaF1, 1, f_obs
                            )
                            alias_flag = (DeltaF1 - y_trumpet) * 100
                            if alias_flag < 1:
                                SOCCA_opt["Period_class"] = 1 # True
                            else:
                                SOCCA_opt["Period_class"] = 0 # Alias
                            SOCCA_opt["Nbs"] = Nbs
                        except Exception:
                            SOCCA_opt["Period_class"] = -1 # Classification error
                    SOCCA_opt["prms"] = p_rms
                    SOCCA_opt["k_terms"] = k_val
                except Exception:
                    SOCCA_opt = {"Failed at SOCCA inversion": 1}
                return SOCCA_opt
            else:
                period_si_t, alt_period_si_t, _ = utils.estimate_sidereal_period(
                    data=data, model_parameters=shg1g2_params, synodic_period=period_sy
                )
                period_si = np.median(period_si_t)
                alt_period_si = np.median(alt_period_si_t)

                if alt_spin is True:
                    period = alt_period_si
                    ra0, de0 = utils.flip_spin(
                        shg1g2_params["alpha0"],
                        shg1g2_params["delta0"],
                    )
                    ra0, de0 = np.radians(ra0), np.radians(de0)
                else:
                    period = period_si
                    ra0, de0 = (
                        np.radians(shg1g2_params["alpha0"]),
                        np.radians(shg1g2_params["delta0"]),
                    )
                #
                H = next(
                    (
                        shg1g2_params.get(f"H_{i}")
                        for i in range(1, 5)
                        if f"H_{i}" in shg1g2_params
                    ),
                    None,
                )
                G1 = next(
                    (
                        shg1g2_params.get(f"G1_{i}")
                        for i in range(1, 5)
                        if f"G1_{i}" in shg1g2_params
                    ),
                    None,
                )
                G2 = next(
                    (
                        shg1g2_params.get(f"G2_{i}")
                        for i in range(1, 5)
                        if f"G2_{i}" in shg1g2_params
                    ),
                    None,
                )

                p0 = [
                    H,
                    G1,
                    G2,
                    ra0,
                    de0,
                    period,
                    shg1g2_params["a_b"],
                    shg1g2_params["a_c"],
                    0.1,
                ]

                # Constrained Fit
                Afit = estimate_sso_params(
                    data["cmred"].values[0],
                    data["csigmapsf"].values[0],
                    np.radians(data["Phase"].values[0]),
                    data["cfid"].values[0],
                    ra=np.radians(data["ra"].values[0]),
                    dec=np.radians(data["dec"].values[0]),
                    jd=data["cjd"].values[0],
                    model="SSHG1G2",  # We should call this SOCCA
                    p0=p0,
                )
                return Afit

        if shg1g2_constrained is False:
            if p0 is None:
                print("Initialize SOCCA first!")
            if p0 is not None:
                if terminator:
                    Afit = estimate_sso_params(
                        data["cmred"].values[0],
                        data["csigmapsf"].values[0],
                        np.radians(data["Phase"].values[0]),
                        data["cfid"].values[0],
                        ra=np.radians(data["ra"].values[0]),
                        dec=np.radians(data["dec"].values[0]),
                        jd=data["cjd"].values[0],
                        model="SSHG1G2",
                        p0=p0,
                        terminator=terminator,
                        ra_s=np.radians(data["ra_s"].values[0]),
                        dec_s=np.radians(data["dec_s"].values[0]),
                    )
                else:
                    Afit = estimate_sso_params(
                        data["cmred"].values[0],
                        data["csigmapsf"].values[0],
                        np.radians(data["Phase"].values[0]),
                        data["cfid"].values[0],
                        ra=np.radians(data["ra"].values[0]),
                        dec=np.radians(data["dec"].values[0]),
                        jd=data["cjd"].values[0],
                        model="SSHG1G2",
                        p0=p0,
                        terminator=terminator,
                    )
                return Afit
    if flavor not in ["SHG1G2", "SOCCA"]:
        print("Model must either be SHG1G2 or SOCCA, not {}".format(flavor))


def get_model_points(data, params):
    """
    Compute modeled magnitudes for a dataset using SHG1G2.

    For each unique filter in the data, this function applies the SHG1G2 model
    to the corresponding subset of observations.

    Parameters
    ----------
    data : pandas.DataFrame
        Dataset containing at least the following columns:
        - 'Phase' : solar phase angles (deg)
        - 'ra' : right ascension (deg)
        - 'dec' : declination (deg)
        - 'cfid' : filter IDs (int)
    params : dict
        Model parameters containing keys:
        - 'H_i', 'G1_i', 'G2_i' for each filter i
        - 'R' : oblateness
        - 'alpha0', 'delta0' : pole coordinates in degrees

    Returns
    -------
    tuple of lists
        - model_points_stack : list of numpy.ndarray
            Modeled magnitudes for each filter.
        - index_points_stack : list of numpy.ndarray
            Indices of the original data points corresponding to each modeled subset.
    """

    model_points_stack = []
    index_points_stack = []
    index = np.array([ind for ind in range(len(data["cfid"].values[0]))])

    for i, f in enumerate(np.unique(data["cfid"].values[0])):
        filter_mask = data["cfid"].values[0] == f

        model_params = [
            params["H_{}".format(f)],
            params["G1_{}".format(f)],
            params["G2_{}".format(f)],
            params["R"],
            np.radians(params["alpha0"]),
            np.radians(params["delta0"]),
        ]

        model_points = func_hg1g2_with_spin(
            [
                np.radians(data["Phase"].values[0][filter_mask]),
                np.radians(data["ra"].values[0][filter_mask]),
                np.radians(data["dec"].values[0][filter_mask]),
            ],
            *model_params,
        )
        index_points_stack.append(index[filter_mask])
        model_points_stack.append(model_points)

    return model_points_stack, index_points_stack


def get_residuals(data, params):
    """
    Compute residuals between observed and modeled magnitudes for a dataset.

    Parameters
    ----------
    data : pandas.DataFrame
        Dataset containing at least the following columns:
        - 'cmred' : observed reduced magnitudes
        - 'Phase' : solar phase angles (deg)
        - 'ra' : right ascension (deg)
        - 'dec' : declination (deg)
        - 'cfid' : filter IDs (int)
    params : dict
        Model parameters including H, G1, G2 for each filter, pole coordinates,
        and oblateness. Keys should match those expected by `get_model_points`.

    Returns
    -------
    numpy.ndarray
        Residuals (observed - modeled magnitudes) for all data points,
        ordered according to the original dataset.
    """

    pstack, istack = get_model_points(data, params)
    fpstack, fistack = utils.flatten_list(pstack), utils.flatten_list(istack)
    df_to_sort = pd.DataFrame({"mpoints": fpstack}, index=fistack)
    df_to_sort = df_to_sort.sort_index()
    df_to_sort["observation"] = data["cmred"].values[0]
    return (df_to_sort["observation"] - df_to_sort["mpoints"]).values


def make_residuals_df(data, model_parameters):
    """
    Create a DataFrame of residuals between observed and modeled magnitudes.

    Parameters
    ----------
    data : pandas.DataFrame
        Dataset containing at least the following columns:
        - 'cmred' : observed reduced magnitudes
        - 'csigmapsf' : photometric uncertainties
        - 'Phase' : solar phase angles (deg)
        - 'ra' : right ascension (deg)
        - 'dec' : declination (deg)
        - 'cfid' : filter IDs (int)
        - 'cjd' : observation times
    model_parameters : dict
        Model parameters including H, G1, G2 for each filter, pole coordinates,
        and oblateness. Keys should match those expected by `get_model_points`.

    Returns
    -------
    pandas.DataFrame
        DataFrame indexed by observation index, with columns:
        - 'mpoints' : modeled magnitudes
        - 'mred' : observed reduced magnitudes
        - 'sigma' : observational uncertainties
        - 'filters' : filter IDs
        - 'jd' : observation times
        - 'residuals' : difference between observed and modeled magnitudes
          (mred - mpoints)
    """
    mpoints, indices = get_model_points(data=data, params=model_parameters)
    flat_mpoints, flat_index = utils.flatten_list(mpoints), utils.flatten_list(indices)

    residual_df = pd.DataFrame({"mpoints": flat_mpoints}, index=flat_index)
    residual_df = residual_df.sort_index()
    residual_df["mred"] = data["cmred"].values[0]
    residual_df["sigma"] = data["csigmapsf"].values[0]
    residual_df["filters"] = data["cfid"].values[0]
    residual_df["jd"] = data["cjd"].values[0]
    residual_df["residuals"] = residual_df["mred"] - residual_df["mpoints"]

    return residual_df
