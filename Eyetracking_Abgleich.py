import math

x = 5
y = 2
z = 1


data_sample = [[x, y, z], [x, y, z], [x, y, z]]
time_movement_start = 0 # = Startzeitpunkt der Bewegung
time_movement_end = 1 # = Endzeitpunkt der Bewegung

while true:
    for sample in data_sample:
        if sample[2] == time_movement_start:
            while sample[2] != time_movement_end:
                movement_samples = []
                movement_samples = movement_samples.append(data_sample[sample])


    movement_x= data_sample[0][0] - data_sample[-1][0]
    movement_y = data_sample[0][1] - data_sample[-1][1]
    movement_xy = math.sqrt(movement_x**2 + movement_y**2)
    angle = math.acos(movement_y/movement_xy)


    if angle == angle_happy






