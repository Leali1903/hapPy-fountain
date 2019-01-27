import math
import numpy as np

# def extract_samples(data):
#     eye_movement_samples = []
#     for sample in data:
#         if sample[0] >= TIME_MOVEMENT_START:
#             if sample[0] <= TIME_MOVEMENT_END:
#                 eye_movement_samples.append(sample)
#             else:
#                 break
#     return eye_movement_samples


def gui_movement():
    for i in range(1,391):
        gui_x_happy.append(810-2*i)
        gui_y_happy.append(390-i)
        gui_x_party.append(810 - 2 * i)
        gui_y_party.append(540 + i)
        gui_x_chillen.append(960 + 2 * i)
        gui_y_chillen.append(540 + i)
        gui_x_sad.append(960 + 2 * i)
        gui_y_sad.append(390 - i)
    return gui_x_happy, gui_y_happy, gui_x_party, gui_y_party, gui_x_chillen, gui_y_chillen, gui_x_sad, gui_y_sad


def correlation(x, y):
    sd_x = np.sqrt(np.var(x))
    sd_y = np.sqrt(np.var(y))
    return np.cov(x,y)/(sd_x * sd_y)


def data_comparison(data_x, data_y):
    gui_movement()

    eye_movement_x = data_x[0] - data_x[-1]
    eye_movement_y = data_y[0] - data_y[-1]

    if correlation(data_x, gui_x_happy) >= 0.7 and correlation(data_y, gui_y_happy) >= 0.7 and eye_movement_x > 0 and eye_movement_y > 0:
        eye_input = 'happy'
    elif correlation(data_x, gui_x_sad) >= 0.7 and correlation(data_y, gui_y_sad) >= 0.7 and eye_movement_x < 0 and eye_movement_y > 0:
        eye_input = 'sad'
    elif correlation(data_x, gui_x_chillen)  and  correlation(data_y, gui_y_chillen) >= 0.7 and eye_movement_x < 0 and eye_movement_y < 0:
        eye_input = 'chillen'
    elif correlation(data_x, gui_x_party) >= 0.7 and correlation(data_y, gui_y_party) >= 0.7 and eye_movement_x > 0 and eye_movement_y < 0:
        eye_input = 'party'

    return eye_input





