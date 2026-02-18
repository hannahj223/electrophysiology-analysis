import numpy as np
from itertools import groupby

sampling_rate_treadmill = 50
win_size = 0.5*sampling_rate_treadmill

#this function removes small runs of 1 or 0s that are shorter than the win size assigned by assigning them to the previous run 
def binary_hysteresis(movement):
    movement = np.array(movement)
    rep_elem = []
    idx = []
    start = 0

    for val,group in groupby(movement):
        length = len(list(group))
        rep_elem.append(length)
        idx.append(start)
        start+= length

    rep_elem = np.array(rep_elem)
    idx = np.array(idx)
    vals = np.array([movement[i] for i in idx]) 

    long_runs = rep_elem >= win_size
    long_idx = idx[long_runs]
    long_vals = vals[long_runs]

    x_filt = np.empty_like(movement)
    x_filt[:long_idx[0]] = long_vals[0]

    for i in range(len(long_idx)-1):
        x_filt[long_idx[i]: long_idx[i+1]] = long_vals[i]
    
    x_filt[long_idx[-1]:] = long_vals[-1]

    return x_filt.astype(int) # convert back to 0 or 1


    






