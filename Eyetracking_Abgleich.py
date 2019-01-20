import math
import numpy as np

# data_sample = [[x, y, z], [x, y, z], [x, y, z]]
# time_movement_start = 0 # = Startzeitpunkt der Bewegung
# time_movement_end = 1 # = Endzeitpunkt der Bewegung


def extract_samples(data):
    eye_movement_samples = []
    for sample in data_sample:
        if sample[0] == time_movement_start:
            while sample[0] != time_movement_end:
                eye_movement_samples = eye_movement_samples.append(sample)
    return eye_movement_samples


def correlation(x, y):
    sd_x = np.sqrt(np.var(x))
    sd_y = np.sqrt(np.var(y))
    r = np.cov(x,y)/(sd_x * sd_y)
    return r


while GUI == 'on':
    extract_samples(data_sample)
    eye_movement_x = eye_movement_sample[0][0] - eye_movement_sample[-1][0]
    eye_movement_y = eye_movement_sample[0][1] - eye_movement_sample[-1][1]
    movement_xy = math.sqrt(eye_movement_x**2 + eye_movement_y**2)

    eye_x = eye_movement_samples[:][0]
    eye_y = eye_movement_samples[:][1]

    if correlation(eye_x, gui_x_happy) >= 0.7 & eye_movement_x > 0 & eye_movement_y > 0:
        eye_input == 'happy'
    elif correlation(eye_x, gui_x_sad) >= 0.7 & eye_movement_x < 0 & eye_movement_y > 0:
        eye_input == 'sad'
    elif correlation(eye_x, gui_x_chillen) >= 0.7 & eye_movement_x > 0 & eye_movement_y < 0:
        eye_input == 'chillen'
    elif correlation(eye_x, gui_x_party) >= 0.7 & eye_movement_x < 0 & eye_movement_y < 0:
        eye_input == 'party'





