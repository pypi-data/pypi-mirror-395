import numpy as np
import scipy.stats


def circmean(angles, weights=None, high=(2 * np.pi), low=0, axis=None, nan_policy='propagate'):
    if nan_policy.lower() == 'ignore':
        nan_policy = 'omit'

    if weights is None:
        mean = scipy.stats.circmean(angles, high=high, low=low, axis=axis, nan_policy=nan_policy)
        return np.mod(mean - low, high - low) + low

    # If weights present, mimic behavior of scipy.stats.circmean
    weights = np.asarray(weights)
    w_flat = weights.flatten()
    w_flat = w_flat[~np.isnan(w_flat)]
    if len(w_flat) == 0:
        return np.nan
    if np.all(weights == w_flat[0]):
        return circmean(angles, high=high, low=low, axis=axis, nan_policy=nan_policy)

    angles = np.mod(np.asarray(angles) - low, high - low) / (high - low) * 2 * np.pi
    vectors = weights * (np.cos(angles) + 1j * np.sin(angles))
    if nan_policy is None or nan_policy.lower() == 'propagate':
        mean_vector = np.mean(vectors, axis=axis)
    elif nan_policy.lower() == 'omit':
        mean_vector = np.nanmean(vectors, axis=axis)
    elif nan_policy.lower() == 'raise':
        if np.any(np.isnan(vectors)):
            raise ValueError("The input contains nan values")
        else:
            mean_vector = np.mean(vectors, axis=axis)
    else:
        raise ValueError("nan_policy must be one of {'propagate', 'raise', 'omit', 'ignore'}")
    mean_norm = np.angle(mean_vector) / (2 * np.pi)
    return mean_norm * (high - low) + low
