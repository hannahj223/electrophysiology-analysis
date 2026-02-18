import numpy as np
import pandas as pd

sampling_rate_ephys = 20000
sampling_rate_treadmill = 50
sampling_rate_camera = 150


def process_data(x_vel, y_vel, z_vel):
    #convert to mm/s and deg/s - this is specific to the RocketMan set up
    x_vel = x_vel*9.822
    y_vel = y_vel*9.6563
    z_vel = z_vel*211.9929

    #Downsample 

    factor = int(sampling_rate_ephys/sampling_rate_treadmill) #this says how many samples to skip
    x_vel_downsampled = x_vel[::factor] #this means start at 0 and go to the end each step by factor
    y_vel_downsampled = y_vel[::factor]
    z_vel_downsampled = z_vel[::factor]


    #filter out baseline noise
    filter_span = 0.3 #the length of the smoothing window in seconds
    window_length = int(filter_span*sampling_rate_treadmill) # convert seconds to samples

    #converts to a pd series and a moving window of size window_length samples. Each window has a mean computed for it (centered on the current sample)
    x_vel_smooth = pd.Series(x_vel_downsampled).rolling(window=window_length, center=True, min_periods=1).mean().to_numpy()
    y_vel_smooth = pd.Series(y_vel_downsampled).rolling(window=window_length, center=True, min_periods=1).mean().to_numpy()
    z_vel_smooth = pd.Series(z_vel_downsampled).rolling(window=window_length, center=True, min_periods=1).mean().to_numpy()

    #calculate translational speed 
    xy_speed = abs(x_vel_smooth) + abs(y_vel_smooth)
    z_speed = abs(z_vel_smooth)

    return xy_speed, z_speed