'''
AVSEN_PLOT_CONFIG = {
    "logFilename" : "logfile.log",
    "subplotDims" : (2,2),
    "plotTitles" : {    #Maps location of plot on grid to its Heading, X-Axis title, Y-axis title, in that order
        (0,0) : ("SENSOR 1 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (0,1) : ("SENSOR 2 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (1,0) : ("SENSOR 3 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (1,1) : ("SENSOR 4 Readings over Time", "Time (secs)", "Sensor Reading (S)")
    },
    "identifiers" : {
        'SENSOR1' : (0, 0),
        'SENSOR2' : (0, 1),
        'SENSOR3' : (1, 0),
        'SENSOR4' : (1, 1)
    },
    "initAxesLims" : {  #Maps plot location to (lowerXLim, upperXLim, lowerYLim, upperYLim) - these are only initial values
        (0,0) : (0, 60, 0, 100),
        (0,1) : (0, 60, 0, 100),
        (1,0) : (0, 60, 0, 100),
        (1,1) : (0, 60, 0, 100)
    },
    "dots" : {
        (0,0) : False,
        (0,1) : False,
        (1,0) : False,
        (1,1) : False
    },
    "save_count" : 10,
    "interval" : 500, #animate() is called every 500ms
    "blit" : True
}

PROPSEN_PLOT_CONFIG = {
    "logFilename" : "logfile.log",
    "subplotDims" : (2,2),
    "plotTitles" : {    #Maps location of plot on grid to its Heading, X-Axis title, Y-axis title, in that order
        (0,0) : ("SENSOR 1 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (0,1) : ("SENSOR 2 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (1,0) : ("SENSOR 3 Readings over Time", "Time (secs)", "Sensor Reading (S)"),
        (1,1) : ("SENSOR 4 Readings over Time", "Time (secs)", "Sensor Reading (S)")
    },
    "identifiers" : {
        'SENSOR1' : (0, 0),
        'SENSOR2' : (0, 1),
        'SENSOR3' : (1, 0),
        'SENSOR4' : (1, 1)
    },
    "initAxesLims" : {  #Maps plot location to (lowerXLim, upperXLim, lowerYLim, upperYLim) - these are only initial values
        (0,0) : (0, 60, 0, 100),
        (0,1) : (0, 60, 0, 100),
        (1,0) : (0, 60, 0, 100),
        (1,1) : (0, 60, 0, 100)
    },
    "dots" : {
        (0,0) : False,
        (0,1) : False,
        (1,0) : False,
        (1,1) : False
    },
    "save_count" : 10,
    "interval" : 500, #animate() is called every 500ms
    "blit" : True
}
'''

SENSOR_CONFIGS = {
    "title_font" : {
        'family' : 'verdana',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : '14'
    },

    "save_count" : 10,
    "interval" : 100, #animate() is called every 100ms
    "blit" : True,
    
    #format is [plot_title, x_label, y_label, xlim0, xlim1, ylim0, ylim1, dotted_line]
    #AVSEN SENSORS
    0 :  ["GPS_ALT Reading over Time", "Time (secs)", "GPS_ALT Reading (meters)", 0, 60, 900, 1100, False],
    1 :  ["GPS_LONG Reading over Time", "Time (secs)", "GPS_LONG Reading (DMS)", 0, 60, -84, -85, False],
    2 :  ["GPS_LAT Reading over Time", "Time (secs)", "GPS_LAT Reading (DMS)", 0, 60, 33, 34, False],
    3 :  ["PRESSURE Reading over Time", "Time (secs)", "PRESSURE Reading (hPa)", 0, 60, 0.8, 1.2, False],
    4 :  ["ALTITUDE Reading over Time", "Time (secs)", "ALTITUDE Reading (meters)", 0, 60, 950, 1050, False],
    5 :  ["MAG_Z Reading over Time", "Time (secs)", "MAG_Z Reading (uT)", 0, 60, 14800, 15200, False],
    6 :  ["MAG_Y Reading over Time", "Time (secs)", "MAG_Y Reading (uT)", 0, 60, 14800, 15200, False],
    7 :  ["MAG_X Reading over Time", "Time (secs)", "MAG_X Reading (uT)", 0, 60, 14800, 15200, False],
    8 :  ["GYRO_Z_2 Reading over Time", "Time (secs)", "GYRO_Z_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    9 :  ["GYRO_Y_2 Reading over Time", "Time (secs)", "GYRO_Y_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    10 : ["GYRO_X_2 Reading over Time", "Time (secs)", "GYRO_X_2 Reading (rad/s)", 0, 60, 0, 0.04, False],
    11 : ["ACCEL_Z_2 Reading over Time", "Time (secs)", "ACCEL_Z_2 Reading (gs)", 0, 60, -1.2, -0.8, False],
    12 : ["ACCEL_Y_2 Reading over Time", "Time (secs)", "ACCEL_Y_2 Reading (gs)", 0, 60, 0, 0.04, False],
    13 : ["ACCEL_X_2 Reading over Time", "Time (secs)", "ACCEL_X_2 Reading (gs)", 0, 60, 0, 0.04, False],
    14 : ["GYRO_Z_1 Reading over Time", "Time (secs)", "GYRO_Z_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    15 : ["GYRO_Y_1 Reading over Time", "Time (secs)", "GYRO_Y_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    16 : ["GYRO_X_1 Reading over Time", "Time (secs)", "GYRO_X_1 Reading (rad/s)", 0, 60, 0, 0.04, False],
    17 : ["ACCEL_Z_1 Reading over Time", "Time (secs)", "ACCEL_Z_1 Reading (gs)", 0, 60, -1.2, -0.8, False],
    18 : ["ACCEL_Y_1 Reading over Time", "Time (secs)", "ACCEL_Y_1 Reading (gs)", 0, 60, 0, 0.04, False],
    19 : ["ACCEL_X_1 Reading over Time", "Time (secs)", "ACCEL_X_1 Reading (gs)", 0, 60, 0, 0.04, False],

    #PROPSEN SENSORS
    20 : ["LOAD CELL Reading over Time", "Time (secs)", "LOAD CELL Reading (S)", 0, 60, 0, 100, False],
    21 : ["TC_16 Reading over Time", "Time (secs)", "TC_16 Reading (S)", 0, 60, 0, 100, False],
    22 : ["TC_15 Reading over Time", "Time (secs)", "TC_15 Reading (S)", 0, 60, 0, 100, False],
    23 : ["TC_14 Reading over Time", "Time (secs)", "TC_14 Reading (S)", 0, 60, 0, 100, False],
    24 : ["TC_13 Reading over Time", "Time (secs)", "TC_13 Reading (S)", 0, 60, 0, 100, False],
    25 : ["TC_12 Reading over Time", "Time (secs)", "TC_12 Reading (S)", 0, 60, 0, 100, False],
    26 : ["TC_11 Reading over Time", "Time (secs)", "TC_11 Reading (S)", 0, 60, 0, 100, False],
    27 : ["TC_10 Reading over Time", "Time (secs)", "TC_10 Reading (S)", 0, 60, 0, 100, False],
    28 : ["TC_09 Reading over Time", "Time (secs)", "TC_09 Reading (S)", 0, 60, 0, 100, False],
    29 : ["TC_08 Reading over Time", "Time (secs)", "TC_08 Reading (S)", 0, 60, 0, 100, False],
    30 : ["TC_07 Reading over Time", "Time (secs)", "TC_07 Reading (S)", 0, 60, 0, 100, False],
    31 : ["TC_06 Reading over Time", "Time (secs)", "TC_06 Reading (S)", 0, 60, 0, 100, False],
    32 : ["TC_05 Reading over Time", "Time (secs)", "TC_05 Reading (S)", 0, 60, 0, 100, False],
    33 : ["TC_04 Reading over Time", "Time (secs)", "TC_04 Reading (S)", 0, 60, 0, 100, False],
    34 : ["TC_03 Reading over Time", "Time (secs)", "TC_03 Reading (S)", 0, 60, 0, 100, False],
    35 : ["TC_02 Reading over Time", "Time (secs)", "TC_02 Reading (S)", 0, 60, 0, 100, False],
    36 : ["TC_01 Reading over Time", "Time (secs)", "TC_01 Reading (S)", 0, 60, 0, 100, False],
    37 : ["PT_16 Reading over Time", "Time (secs)", "PT_16 Reading (S)", 0, 60, 0, 100, False],
    38 : ["PT_15 Reading over Time", "Time (secs)", "PT_15 Reading (S)", 0, 60, 0, 100, False],
    39 : ["PT_14 Reading over Time", "Time (secs)", "PT_14 Reading (S)", 0, 60, 0, 100, False],
    40 : ["PT_13 Reading over Time", "Time (secs)", "PT_13 Reading (S)", 0, 60, 0, 100, False],
    41 : ["PT_12 Reading over Time", "Time (secs)", "PT_12 Reading (S)", 0, 60, 0, 100, False],
    42 : ["PT_11 Reading over Time", "Time (secs)", "PT_11 Reading (S)", 0, 60, 0, 100, False],
    43 : ["PT_10 Reading over Time", "Time (secs)", "PT_10 Reading (S)", 0, 60, 0, 100, False],
    44 : ["PT_09 Reading over Time", "Time (secs)", "PT_09 Reading (S)", 0, 60, 0, 100, False],
    45 : ["PT_08 Reading over Time", "Time (secs)", "PT_08 Reading (S)", 0, 60, 0, 100, False],
    46 : ["PT_07 Reading over Time", "Time (secs)", "PT_07 Reading (S)", 0, 60, 0, 100, False],
    47 : ["PT_06 Reading over Time", "Time (secs)", "PT_06 Reading (S)", 0, 60, 0, 100, False],
    48 : ["PT_05 Reading over Time", "Time (secs)", "PT_05 Reading (S)", 0, 60, 0, 100, False],
    49 : ["PT_04 Reading over Time", "Time (secs)", "PT_04 Reading (S)", 0, 60, 0, 100, False],
    50 : ["PT_03 Reading over Time", "Time (secs)", "PT_03 Reading (S)", 0, 60, 0, 100, False],
    51 : ["PT_02 Reading over Time", "Time (secs)", "PT_02 Reading (S)", 0, 60, 0, 100, False],
    52 : ["PT_01 Reading over Time", "Time (secs)", "PT_01 Reading (S)", 0, 60, 0, 100, False]
}