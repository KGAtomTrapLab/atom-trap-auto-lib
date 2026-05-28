import numpy as np
from scipy.signal import savgol_filter, resample
from scipy.stats import zscore

def filter(input_array):
        np_target = np.array(input_array, dtype=float)
        #smooth out
        smoothed = savgol(np_target)

        normalized = z_normalize(smoothed)

        return smoothed

def reduce_min(input_array):
    min = np.min(input_array)
    input_array -= min
    return input_array

def z_normalize(input_array):
    mean = np.mean(input_array)
    std_dev = np.std(input_array)
    z_scores = (input_array - mean) / std_dev

    return z_scores

def savgol(input_array):

    return savgol_filter(input_array, 60, 3)

def sliding_window_view_1d(x, w):
    n = len(x) - w + 1
    return np.lib.stride_tricks.as_strided(
        x,
        shape=(n, w),
        strides=(x.strides[0], x.strides[0])
    )

def resize_to_match(y, n):
    return resample(y, n)

def template_match(signal, template):

    w = len(template)
    windows = sliding_window_view_1d(signal, w)

    t = zscore(template)
    win_mean = windows.mean(axis=1, keepdims=True)
    win_std = windows.std(axis=1, keepdims=True)
    win_std[win_std == 0] = 1.0
    windows_z = (windows - win_mean) / win_std

    scores = windows_z @ t / w
    return scores