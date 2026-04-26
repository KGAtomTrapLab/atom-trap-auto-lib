import numpy as np
from scipy.signal import savgol_filter

def filter(input_array):
        np_target = np.array(input_array)
        #smooth out
        smoothed = savgol(np_target)

        return z_normalize(smoothed)

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

    return savgol_filter(input_array, 40, 3)