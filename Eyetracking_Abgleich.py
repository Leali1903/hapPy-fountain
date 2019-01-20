import math
import numpy as np

# data_sample = [[x, y, z], [x, y, z], [x, y, z]]
# TIME_MOVEMENT_START = 0 # = Startzeitpunkt der Bewegung
# TIME_MOVEMENT_END = 1 # = Endzeitpunkt der Bewegung


def extract_samples(data):
    eye_movement_samples = []
    for sample in data:
        if sample[0] >= TIME_MOVEMENT_START:
            if sample[0] <= TIME_MOVEMENT_END:
                eye_movement_samples.append(sample)
            else:
                break
    return eye_movement_samples


def correlation(x, y):
    sd_x = np.sqrt(np.var(x))
    sd_y = np.sqrt(np.var(y))
    return np.cov(x,y)/(sd_x * sd_y)


while GUI == 'on':
    extract_samples(data_sample)
    eye_movement_x = eye_movement_sample[0][1] - eye_movement_sample[-1][1]
    eye_movement_y = eye_movement_sample[0][2] - eye_movement_sample[-1][2]
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





