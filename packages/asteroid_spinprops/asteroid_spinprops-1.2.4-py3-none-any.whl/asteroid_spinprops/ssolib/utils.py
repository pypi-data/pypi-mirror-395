import numpy as np
import astropy.constants as const


def is_sorted(a):
    """
    Check whether a 1D array is sorted in non-decreasing order.

    Parameters
    ----------
    a : array_like
        Input array to test.

    Returns
    -------
    bool
        True if `a` is sorted in non-decreasing order, False otherwise.
    """
    return np.all(a[:-1] <= a[1:])


def sigma_condition_func(data):
    """
    Used to wrap the condition to flag points within 3 sigma of a dataset.

    Parameters
    -----------
    data : array-like
        The data to be flagged.

    Returns
    --------
    array-like of bool
        A boolean mask indicating which data points lie **within** mu \pm 3 sigma,
    """
    mean_val = np.mean(data)
    std_val = np.std(data)
    return (data > mean_val - 3 * std_val) & (data < mean_val + 3 * std_val)


def find_nearest(array, value):
    """
    Find the nearest value of an array to a given value.

    Parameters
    ----------
    array : array-like
        Array from which to find the nearest value.
    value : float
        Value to compare with array

    Returns
    -------
    The value of the array which is nearest to the given value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def flatten_list(xss):
    """
    Flatten a list.

    Parameters
    ----------
    xss : list
        List of lists (or other iterrable) to flatten in a single array
    Returns
    -------
    Flattened list as a np.array
    """
    flat_list = [x for xs in xss for x in xs]
    return np.array(flat_list)


def calculate_reduced_magnitude(magnitude, D_observer, D_sun):
    """
    Calculate reduced magnitude

    Parameters
    -----------------------------
    magnitude : float/np.array
        Mangitude from obervation
    D_oberver : float/np.array
        Object-observer distance
    D_sun : float/np.array
        Object-sun distance

    Returns
    -----------------------------
    float/np.array, reduced magnitude
    """
    return magnitude - 5 * np.log10(D_observer * D_sun)


def sort_by_cjd(data):
    """
    Function to sort data containing a `cjd` column by this column.

    Parameters
    -----------
    data : pd.DataFrame
        A single-row DataFrame where each column contains an array of values.

    Returns
    -------
    data: pd.DataFrame
        Sorted dataframe
    """
    cjd_list = data["cjd"].values[0]

    sorted_indices = np.argsort(cjd_list)
    for col in data.columns:
        if col not in ["level_0", "index", "name"]:
            data[col].values[0] = np.array(data[col].values[0])[sorted_indices]
    return data


def get_apparition_indices(dates, threshold=100):
    """
    Identify indices where there is a significant time gap (>threshold days).

    Parameters
    -----------
    dates : np.array
        JDs of observations
    threshold : int
        Assumed threshold between apparitions, default is 100 days

    Returns
    --------
    np.array containing the indices of apparitions in the JD array,
    including 1st and last day (i.e. apparition 1: [0, 97] ...)
    """
    return np.concatenate(([0], np.where(np.diff(dates) > threshold)[0], [len(dates)]))


def flip_spin(ra0, dec0):
    """
    Compute the antipodal (spin-flip) direction for a given RA/Dec.

    Parameters
    ----------
    ra0 : float or array_like
        Right ascension in degrees.
    dec0 : float or array_like
        Declination in degrees.

    Returns
    -------
    tuple of float or array_like
        `(ra_alt, dec_alt)` giving the antipodal right ascension and
        declination in degrees.
    """
    ra0 = np.radians(ra0)
    dec0 = np.radians(dec0)
    ra_alt = (ra0 + np.pi) % (2 * np.pi)
    dec_alt = -dec0
    return np.rad2deg(ra_alt), np.rad2deg(dec_alt)


def calc_atan_parameter(ra, dec, ra0, dec0):
    """
    Compute the angular parameter used in great-circle or pole-separation geometry.

    Parameters
    ----------
    ra : float or array_like
        Right ascension of the target point, in degrees.
    dec : float or array_like
        Declination of the target point, in degrees.
    ra0 : float or array_like
        Reference right ascension, in degrees.
    dec0 : float or array_like
        Reference declination, in degrees.

    Returns
    -------
    float or array_like
        The atan2-based angle (in radians) describing the orientation of
        the target point relative to the reference direction.
    """
    ra, dec, ra0, dec0 = (
        np.radians(ra),
        np.radians(dec),
        np.radians(ra0),
        np.radians(dec0),
    )
    x = np.cos(dec0) * np.sin(dec) - np.sin(dec0) * np.cos(dec) * np.cos(ra - ra0)
    y = np.cos(dec) * np.sin(ra - ra0)
    return np.arctan2(x, y)


def compute_ltc(jd, d_obs, filt=None):
    """
    Compute the time with light travel corrected

    Parameters
    ----------
    jd: np.array
        Array of times (JD), in day
    d_obs: np.array
        Array of distance to the observer, in AU
    """
    c_speed = const.c.to("au/day").value
    jd_lt = jd.copy()
    if filt is not None:
        mask_filt = (filt == 1) | (filt == 2)
        jd_lt[mask_filt] -= d_obs[mask_filt] / c_speed
    else:
        jd_lt -= d_obs / c_speed

    return jd_lt


def angle_after_one_synodic_period(angle, synodic_period, rate):
    """
    Propagate an angle forward by one synodic period given a drift rate.

    Parameters
    ----------
    angle : float or array_like
        Initial angle in degrees.
    synodic_period : float
        Synodic period in days.
    rate : float or array_like
        Angular drift rate in arcseconds per minute.

    Returns
    -------
    float or array_like
        Angle after one synodic period, in degrees.
    """
    angle_t1 = (
        angle + synodic_period * (60 * 24) / 3600 * rate
    )  # dRA in arcsec/min, period in days, ra_t0|1 in degrees
    return angle_t1


def estimate_sidereal_period(data, model_parameters, synodic_period):
    """
    Estimate the sidereal period of an object from its astrometric drift
    over one synodic period, using both the nominal and spin-flipped
    pole solutions.

    Parameters
    ----------
    data : pandas.DataFrame
        Table containing at least the columns:
        - 'cjd' : float
            Corrected Julian dates.
        - 'ra' : float
            Right ascension in degrees.
        - 'dec' : float
            Declination in degrees.
        - 'dRA' : float
            RA drift rate in arcseconds per minute.
        - 'dDec' : float
            Dec drift rate in arcseconds per minute.
    model_parameters : dict
        Dictionary containing pole coordinates:
        - 'alpha0' : float
            Reference right ascension (degrees).
        - 'delta0' : float
            Reference declination (degrees).
    synodic_period : float
        Synodic period in days.

    Returns
    -------
    tuple
        (sidereal_period, sidereal_period_alt, epoch1) where:
        - sidereal_period : float
            Sidereal period corresponding to the nominal pole.
        - sidereal_period_alt : float
            Sidereal period corresponding to the antipodal pole.
        - epoch1 : float
            Epoch of the first observation (CJD).
    """
    ra0 = model_parameters["alpha0"]
    dec0 = model_parameters["delta0"]

    epoch1 = data["cjd"].values[0]

    ra_t0 = data["ra"].values[0]
    dec_t0 = data["dec"].values[0]
    dRA = data["dRA"].values[0]
    dDec = data["dDec"].values[0]

    ra_t1, dec_t1 = (
        angle_after_one_synodic_period(ra_t0, synodic_period, dRA),
        angle_after_one_synodic_period(dec_t0, synodic_period, dDec),
    )

    atan_param_1 = calc_atan_parameter(ra_t0, dec_t0, ra0, dec0)
    atan_param_2 = calc_atan_parameter(ra_t1, dec_t1, ra0, dec0)

    ra_alt, dec_alt = flip_spin(ra0, dec0)

    atan_param_1alt = calc_atan_parameter(ra_t0, dec_t0, ra_alt, dec_alt)
    atan_param_2alt = calc_atan_parameter(ra_t1, dec_t1, ra_alt, dec_alt)

    sidereal_period = (
        2 * np.pi * synodic_period / (atan_param_2 - atan_param_1 + 2 * np.pi)
    )
    sidereal_period_alt = (
        2 * np.pi * synodic_period / (atan_param_2alt - atan_param_1alt + 2 * np.pi)
    )

    return sidereal_period, sidereal_period_alt, epoch1


def oblateness(a_b, a_c):
    """
    Compute a simple oblateness proxy from axis ratios.

    Parameters
    ----------
    a_b : float or array_like
        Intermediate-to-long axis ratio (b/a).
    a_c : float or array_like
        Short-to-long axis ratio (c/a).

    Returns
    -------
    float or array_like
        Oblateness measure defined as 0.5 * (a_b / a_c + 1 / a_b).
    """
    return 1 / 2 * a_b / a_c + 1 / 2 * 1 / a_b


def wrap_longitude(long):
    """
    Wrap a longitude angle into the range [0, 360).

    Parameters
    ----------
    long : float or array_like
        Input longitude in degrees.

    Returns
    -------
    float or array_like
        Longitude wrapped to the interval [0, 360).
    """
    return long % 360


def wrap_latitude(lat):
    """
    Wrap a latitude angle into the range [-90, 90] by folding across the poles.

    Parameters
    ----------
    lat : float or array_like
        Input latitude in degrees.

    Returns
    -------
    float or array_like
        Latitude wrapped to the interval [-90, 90].
    """
    m = (lat + 90) % 360  # shift so -90 maps to 0
    if m > 180:
        m = 360 - m
    return m - 90


def generate_initial_points(ra, dec, dec_shift=45):
    """
    Generate a set of 12 initial (RA, Dec) sampling points by combining
    spin-flipped poles, RA sweeps, and latitude shifts.

    Parameters
    ----------
    ra : float
        Base right ascension in degrees.
    dec : float
        Base declination in degrees.
    dec_shift : float, optional
        Latitude shift (degrees) applied when generating the secondary
        sets of points. Defaults to 45 degrees.

    Returns
    -------
    tuple of list
        (ra_list, dec_list), where each list contains 18 elements
        representing the generated right ascensions and declinations
        in degrees.
    """
    if np.abs(2 * dec - dec_shift) < 10:
        dec_shift += 20

    ra_list = []
    dec_list = []

    base_coords = [(ra, dec), flip_spin(ra, dec)]

    ra_sweep = [0, 180]

    for base_ra, base_dec in base_coords:
        for offset in ra_sweep:
            ra_list.append(wrap_longitude(base_ra + offset))
            dec_list.append(base_dec)

    dec_sweep = [-dec_shift, dec_shift]
    for shift in dec_sweep:
        for base_ra, base_dec in base_coords:
            if (base_dec + shift > 90) | (base_dec - shift < 90):
                flag = 1
            else:
                flag = 0
            shifted_dec = wrap_latitude(base_dec + shift)

            for offset in ra_sweep:
                temp_ra = base_ra + (180 if flag == 1 else 0)
                ra_list.append(wrap_longitude(temp_ra + offset))
                dec_list.append(shifted_dec)
    return ra_list, dec_list

def gaussian_interpolate(data, factor=4, sigma=1.0):
    """
    Reproduce matplotlib's `interpolation="gaussian"` effect.
    factor : upsampling factor
    sigma  : Gaussian smoothing strength
    """
    from scipy.ndimage import zoom, gaussian_filter

    # Step 1: upsample (mimics interpolation grid)
    up = zoom(data, factor, order=1)  # bilinear before smoothing
    
    # Step 2: apply gaussian smoothing
    smoothed = gaussian_filter(up, sigma=sigma)
    
    return smoothed

def detect_local_minima(arr):
    import scipy.ndimage.filters as filters
    import scipy.ndimage.morphology as morphology

    # https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
    # https://stackoverflow.com/questions/3986345/how-to-find-the-local-minima-of-a-smooth-multidimensional-array-in-numpy
    """
    Takes an array and detects the troughs using the local maximum filter.
    Returns a boolean mask of the troughs (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    neighborhood = morphology.generate_binary_structure(len(arr.shape),2)
    
    footprint = np.ones((15, 15))
    local_min = filters.minimum_filter(arr, footprint=footprint) == arr

    background = (arr==0)
    eroded_background = morphology.binary_erosion(
        background, structure=neighborhood, border_value=1)

    detected_minima = local_min ^ eroded_background
    return np.where(detected_minima)       

def trumpet(peak_diff_1, f_feat, f_obs):
    """
    Implementation of the alias/true flagging algorithm.

    Parameters
    ----------
    peak_diff_1 : float
        The difference between the 2nd and 3rd highest peaks of the periodogram
    f_feat : float
        The feature frequency.
    f_obs : float
        The 1st highest peak if the periodogram
    Returns
    -------
    The assumed true frequency peak difference value if the peak is true,
    otherwise zero.
    """
    if peak_diff_1 > 0 and f_obs > f_feat:
        return 2 * f_feat

    elif peak_diff_1 < 0 and f_obs < f_feat:
        return -2 * f_obs

    elif peak_diff_1 > 0 and f_obs < f_feat:
        return 2 * f_obs

    elif peak_diff_1 < 0 and f_obs > f_feat:
        return -2 * f_feat

    return 0.0
