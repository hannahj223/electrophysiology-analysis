import numpy as np
from itertools import groupby

sampling_rate_treadmill = 50
win_size = int(0.2*sampling_rate_treadmill)


def binary_replace(movement):
    
    movement = np.array(movement) #ensures movement is a numpy array 
    rep_elem = []
    idx = []
    start = 0

    for val, group in groupby(movement): # groups consecutive identical elements in movement and returns pairs: val (repeated value), group (interator over consec elements = val)
        length = len(list(group)) #converts to a list to count how many consec elements are in this run 
        rep_elem.append(val) #stores the values of the run 
        idx.append(start) #stores the indexing of the run 
        start += length #updates start to the index of the next run

    rep_elem = np.array(rep_elem)
    idx = np.array(idx)

    #fill short gaps of zeros <= win size
    for i, val in enumerate(rep_elem):
        if val == 0 and rep_elem[i] <= win_size:
            movement[idx[i]: idx[i] + int(rep_elem[i])] = 1

    return movement

