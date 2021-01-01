SENSOR_CONFIGS = {
    'background' : (255,255,255),
    'foreground' : (0,0,0),
    'xlabel' : {
        'color' : (0,0,0),
        'font-size' : '12pt'
    },
    'ylabel' : {
        'color' : (0,0,0),
        'font-size' : '12pt'
    },
    'title' : {
        'color' : (0,0,0),
        'size' : '16pt'
    },
    'border' : {
        'color' : (0,0,0)
    },
    'grid' : {
        'color' : (0,0,0)
    },

    "save_count" : 10,
    #Controls how many milliseconds update() waits for before repeating
    "interval" : 200,
    "line_colors" : [(0, 63, 92), (47, 75, 124), (102, 81, 145),
                     (160, 81, 149), (212, 80, 135), (249, 93, 106),
                     (255, 124, 67), (255, 166, 0), (78, 141, 124),
                     (194, 73, 20), (97, 177, 90)],
    
    #format is [plot_title, x_label, y_label, xlim0, xlim1, ylim0, ylim1, dotted_line]
    #AVSEN SENSORS
    0 :  ["ADXL_Z Reading over Time", "Time (secs)", "ADXL_Z Reading (gs)", 0, 60, -1.2, -0.8, False],
    1 :  ["ADXL_Y Reading over Time", "Time (secs)", "ADXL_Y Reading (gs)", 0, 60, 0, 0.04, False],
    2 :  ["ADXL_X Reading over Time", "Time (secs)", "ADXL_X Reading (gs)", 0, 60, 0, 0.04, False],
    3 :  ["GPS_ALT Reading over Time", "Time (secs)", "GPS_ALT Reading (meters)", 0, 60, 900, 1100, False],
    4 :  ["GPS_LONG Reading over Time", "Time (secs)", "GPS_LONG Reading (DMS)", 0, 60, -84, -85, False],
    5 :  ["GPS_LAT Reading over Time", "Time (secs)", "GPS_LAT Reading (DMS)", 0, 60, 33, 34, False],
    6 :  ["PRESSURE Reading over Time", "Time (secs)", "PRESSURE Reading (hPa)", 0, 60, 0.8, 1.2, False],
    7 :  ["ALTITUDE Reading over Time", "Time (secs)", "ALTITUDE Reading (meters)", 0, 60, 950, 1050, False],
    8 :  ["MAG_Z Reading over Time", "Time (secs)", "MAG_Z Reading (uT)", 0, 60, 14800, 15200, False],
    9 :  ["MAG_Y Reading over Time", "Time (secs)", "MAG_Y Reading (uT)", 0, 60, 14800, 15200, False],
    10 : ["MAG_X Reading over Time", "Time (secs)", "MAG_X Reading (uT)", 0, 60, 14800, 15200, False],
    11 : ["GYRO_Z_2 Reading over Time", "Time (secs)", "GYRO_Z_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    12 : ["GYRO_Y_2 Reading over Time", "Time (secs)", "GYRO_Y_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    13 : ["GYRO_X_2 Reading over Time", "Time (secs)", "GYRO_X_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    14 : ["ACCEL_Z_2 Reading over Time", "Time (secs)", "ACCEL_Z_2 Reading (gs)", 0, 60, -1.2, -0.8, False],
    15 : ["ACCEL_Y_2 Reading over Time", "Time (secs)", "ACCEL_Y_2 Reading (gs)", 0, 60, 0, 0.04, False],
    16 : ["ACCEL_X_2 Reading over Time", "Time (secs)", "ACCEL_X_2 Reading (gs)", 0, 60, 0, 0.04, False],
    17 : ["GYRO_Z_1 Reading over Time", "Time (secs)", "GYRO_Z_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    18 : ["GYRO_Y_1 Reading over Time", "Time (secs)", "GYRO_Y_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    19 : ["GYRO_X_1 Reading over Time", "Time (secs)", "GYRO_X_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    20 : ["ACCEL_Z_1 Reading over Time", "Time (secs)", "ACCEL_Z_1 Reading (gs)", 0, 60, -1.2, -0.8, False],
    21 : ["ACCEL_Y_1 Reading over Time", "Time (secs)", "ACCEL_Y_1 Reading (gs)", 0, 60, 0, 0.04, False],
    22 : ["ACCEL_X_1 Reading over Time", "Time (secs)", "ACCEL_X_1 Reading (gs)", 0, 60, 0, 0.04, False],
    #PROPSEN SENSORS
    23 : ["LOAD CELL Reading over Time", "Time (secs)", "LOAD CELL Reading (S)", 0, 60, 0, 100, False],
    24 : ["TC_16 Reading over Time", "Time (secs)", "TC_16 Reading (S)", 0, 60, 0, 100, False],
    25 : ["TC_15 Reading over Time", "Time (secs)", "TC_15 Reading (S)", 0, 60, 0, 100, False],
    26 : ["TC_14 Reading over Time", "Time (secs)", "TC_14 Reading (S)", 0, 60, 0, 100, False],
    27 : ["TC_13 Reading over Time", "Time (secs)", "TC_13 Reading (S)", 0, 60, 0, 100, False],
    28 : ["TC_12 Reading over Time", "Time (secs)", "TC_12 Reading (S)", 0, 60, 0, 100, False],
    29 : ["TC_11 Reading over Time", "Time (secs)", "TC_11 Reading (S)", 0, 60, 0, 100, False],
    30 : ["TC_10 Reading over Time", "Time (secs)", "TC_10 Reading (S)", 0, 60, 0, 100, False],
    31 : ["TC_09 Reading over Time", "Time (secs)", "TC_09 Reading (S)", 0, 60, 0, 100, False],
    32 : ["TC_08 Reading over Time", "Time (secs)", "TC_08 Reading (S)", 0, 60, 0, 100, False],
    33 : ["TC_07 Reading over Time", "Time (secs)", "TC_07 Reading (S)", 0, 60, 0, 100, False],
    34 : ["TC_06 Reading over Time", "Time (secs)", "TC_06 Reading (S)", 0, 60, 0, 100, False],
    35 : ["TC_05 Reading over Time", "Time (secs)", "TC_05 Reading (S)", 0, 60, 0, 100, False],
    36 : ["TC_04 Reading over Time", "Time (secs)", "TC_04 Reading (S)", 0, 60, 0, 100, False],
    37 : ["TC_03 Reading over Time", "Time (secs)", "TC_03 Reading (S)", 0, 60, 0, 100, False],
    38 : ["TC_02 Reading over Time", "Time (secs)", "TC_02 Reading (S)", 0, 60, 0, 100, False],
    39 : ["TC_01 Reading over Time", "Time (secs)", "TC_01 Reading (S)", 0, 60, 0, 100, False],
    40 : ["PT_16 Reading over Time", "Time (secs)", "PT_16 Reading (S)", 0, 60, 0, 100, False],
    41 : ["PT_15 Reading over Time", "Time (secs)", "PT_15 Reading (S)", 0, 60, 0, 100, False],
    42 : ["PT_14 Reading over Time", "Time (secs)", "PT_14 Reading (S)", 0, 60, 0, 100, False],
    43 : ["PT_13 Reading over Time", "Time (secs)", "PT_13 Reading (S)", 0, 60, 0, 100, False],
    44 : ["PT_12 Reading over Time", "Time (secs)", "PT_12 Reading (S)", 0, 60, 0, 100, False],
    45 : ["PT_11 Reading over Time", "Time (secs)", "PT_11 Reading (S)", 0, 60, 0, 100, False],
    46 : ["PT_10 Reading over Time", "Time (secs)", "PT_10 Reading (S)", 0, 60, 0, 100, False],
    47 : ["PT_09 Reading over Time", "Time (secs)", "PT_09 Reading (S)", 0, 60, 0, 100, False],
    48 : ["PT_08 Reading over Time", "Time (secs)", "PT_08 Reading (S)", 0, 60, 0, 100, False],
    49 : ["PT_07 Reading over Time", "Time (secs)", "PT_07 Reading (S)", 0, 60, 0, 100, False],
    50 : ["PT_06 Reading over Time", "Time (secs)", "PT_06 Reading (S)", 0, 60, 0, 100, False],
    51 : ["PT_05 Reading over Time", "Time (secs)", "PT_05 Reading (S)", 0, 60, 0, 100, False],
    52 : ["PT_04 Reading over Time", "Time (secs)", "PT_04 Reading (S)", 0, 60, 0, 100, False],
    53 : ["PT_03 Reading over Time", "Time (secs)", "PT_03 Reading (S)", 0, 60, 0, 100, False],
    54 : ["PT_02 Reading over Time", "Time (secs)", "PT_02 Reading (S)", 0, 60, 0, 100, False],
    55 : ["PT_01 Reading over Time", "Time (secs)", "PT_01 Reading (S)", 0, 60, 0, 100, False]
}

#PT01, PT06, PT10, TC07, TC14, TC16, Load Cell, Accelx1, Gyroz1, Gyroy2, Altitude, 
