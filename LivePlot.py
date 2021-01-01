'''
LivePlot Graphing Software
Designed and Implemented by: Manas Harbola
Designed for the YJSP MCFS_V2 software
Email: mharbola3@gatech.edu
'''
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import base64
import numpy as np
import re
import sys
import socket
import os
import time
import sensorDicts

#Agreed upon port through which mcfs will communicate with LivePlot.py
PORT = 18000
#Standardized buffer size for receiving sensor data from mcfs
SOCKET_BUFFER_SIZE = 512

'''
Objectives:
    -Create realtime graphs of 20+ sensors simulataneously and EFFICIENTLY
    -Provide flexibility and intuitive controls to PROPSEN and AVSEN teams for visualizing telemetry data
    -Create a configurable script for customizing plots, dynamic rescaling, titles, line colors, etc.
'''

class LivePlot:
    line_colors = sensorDicts.SENSOR_CONFIGS["line_colors"]
    #def __init__(self, plotcode, configDict):
    def __init__(self, plotcode, slidingcode, lockedcode, minMaxVals, configDict):
        #Check parameter type
        if not(isinstance(configDict, dict)):
            raise TypeError("parameter 'configDict' of invalid type")
        
        #Get plotIDs for graphing
        self.plotIDs = LivePlot.getIndices(plotcode)
        
        #Get which plots need to be moving plots
        self.movingPlotIDs = set(LivePlot.getIndices(slidingcode))
        self.lockedPlotIDs = set(LivePlot.getIndices(lockedcode))
        
        #self.movingPlotIDs = {}
        #self.lockedPlotIDs = {}
        #Get which plots need to have min/max locked y-range
        #self.lockedPlotIDs = set(LivePlot.getIndices(plotcode))
        #self.lockedPlotIDs = set(LivePlot.getIndices(lockedcode))

        if len(self.plotIDs) == 0:
            raise ValueError("no sensors selected to plot...closing plotter")
            #sys.exit(1)
        
        #Subplot grid dimension calculations
        if len(self.plotIDs) == 1:
            columnSize = 1
            rowSize = 1
        else:
            columnSize = int(np.log(len(self.plotIDs)) / np.log(2))
            rowSize = int(np.ceil(len(self.plotIDs) / columnSize))
        
        self.interval = configDict["interval"]
        self.subplotDims = (rowSize, columnSize)

        #self.epoch is the reference unix timestamp of t=0s
        self.epoch = 0

        #Dictionaries for accessing x and y lists for plots
        '''
        self.xlsts = {plotID : [] for plotID in self.plotIDs}
        self.ylsts = {plotID : [] for plotID in self.plotIDs}
        '''
        self.xlsts = {plotID : [np.zeros(120, dtype=np.uint32), 0] for plotID in self.plotIDs}
        self.ylsts = {plotID : [np.zeros(120, dtype=np.float64), 0] for plotID in self.plotIDs}

        #Initial x and y ranges for plots
        self.xlims = {plotID : configDict[plotID][3:5] for plotID in self.plotIDs}
        self.ylims = {plotID : configDict[plotID][5:7] for plotID in self.plotIDs}
        
        #self.lines = []

        #pyqtgraph initialization
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', configDict['background'])
        pg.setConfigOption('foreground', configDict['foreground'])

        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='MCFS LivePlot')
        self.win.setWindowTitle('MCFS LivePlot')
        self.win.setGeometry(5, 115, 1280, 720)
        
        #self.plotIDMap is a dictionary that maps sensor ID to a particular plot
        self.plotIDMap = dict()
        #self.lineMap is a dictionary that maps sensor ID to a particular line
        self.lineMap = dict()

        #Create colorWheelIterator
        self.colorWheelIterator = iter(LivePlot.pickColor())

        idx = 0
        lockedIdx = 0
        self.started = False
        for i in range(self.subplotDims[0]):
            if idx >= len(self.plotIDs):
                break
            for j in range(self.subplotDims[1]):
                if idx >= len(self.plotIDs):
                    break
                
                plotID = self.plotIDs[idx]

                #Create subplot 
                self.plotIDMap[plotID] = self.win.addPlot(row=i, col=j,)

                #Set title, x, y labels
                self.plotIDMap[plotID].setTitle(title=configDict[plotID][0], **configDict['title'])
                self.plotIDMap[plotID].setLabel(axis='bottom', text=configDict[plotID][1], units=None, unitPrefix=None, **configDict['xlabel'])
                self.plotIDMap[plotID].setLabel(axis='left', text=configDict[plotID][2], units=None, unitPrefix=None, **configDict['ylabel'])
                #Set textPens
                self.plotIDMap[plotID].getAxis('bottom').setTextPen(configDict['xlabel']['color'])
                self.plotIDMap[plotID].getAxis('left').setTextPen(configDict['ylabel']['color'])

                #Turn on grid
                self.plotIDMap[plotID].showGrid(x=True, y=True, alpha=0.5)
                
                #Configure border color
                self.plotIDMap[plotID].getViewBox().setBorder((0, 0, 0))

                #self.lineMap[plotID] = self.plotIDMap[plotID].plot(pen='c', width=8)
                
                #self.lineMap[plotID] = self.plotIDMap[plotID].plot(pen=next(self.colorWheelIterator), width=20.0)
                self.lineMap[plotID] = self.plotIDMap[plotID].plot(pen=pg.mkPen(next(self.colorWheelIterator), width=2.0))

                #TODO: Add option to change AutoRange or Moving graph style for particular data

                #Check if plot was selected to be moving
                if plotID not in self.movingPlotIDs:
                    self.plotIDMap[plotID].enableAutoRange(axis=self.plotIDMap[plotID].getViewBox().XAxis)
                    self.plotIDMap[plotID].setXRange(min=self.xlims[plotID][0], max=self.xlims[plotID][1])
                else:
                    self.plotIDMap[plotID].setXRange(min=-self.xlims[plotID][1], max=0)

                #Check if plot has restricted min and max y-vals
                if plotID not in self.lockedPlotIDs:
                    self.plotIDMap[plotID].enableAutoRange(axis=self.plotIDMap[plotID].getViewBox().YAxis)
                    self.plotIDMap[plotID].setYRange(min=self.ylims[plotID][0], max=self.ylims[plotID][1])
                else:
                    #TODO: NEED TO CHANGE THIS TO FROM THE SPECIFIED Ymin and Ymax
                    #self.plotIDMap[plotID].setYRange(min=self.ylims[plotID][0], max=self.ylims[plotID][1])
                    self.plotIDMap[plotID].setYRange(min=minMaxVals[lockedIdx][0], max=minMaxVals[lockedIdx][1])
                    lockedIdx += 1
                
                idx += 1

        #Used for setting up socket communication with mcfs
        self.sock = None
        self.clientsocket = None
        self.address = None

        #Flags for checking which type of data will be received next
        self.receiveMsgSizeNext = True
        self.msgSizeBytes = 0
        self.msg = None

    #Helper function for parsing log lines one by one
    def parseLogLine(line):
        lst = re.split(" |\|", line)
        if len(lst) < 2 or (lst[1] not in {'DB00', 'DB01'}):
            return None
        #Check bytecode DB00 -> AVSEN, DB01 -> PROPSEN
        if lst[1] == 'DB00':
            #return [float(lst[0]), 'DB00', *[float(value[2:]) for value in lst[2:]]]
            return [int(lst[0]), 'DB00', *[float(value[2:]) for value in lst[2:]]]

        elif lst[1] == 'DB01':
            #return [float(lst[0]), 'DB01', *[float(value[3:]) for value in lst[2:]]]
            return [int(lst[0]), 'DB01', *[float(value[3:]) for value in lst[2:]]]

    #Decodes Base64 string and determines which plots to display
    def getIndices(s):
        b = bin(int.from_bytes(base64.b64decode(s), "big"))[2:]
        return [len(b) - 1 - i for i in range(len(b)) if b[i] == '1']
    
    def pickColor():
        idx = 0
        while True:
            yield LivePlot.line_colors[idx]
            idx = (idx + 1) % len(LivePlot.line_colors)
    
    #Method for updating graph data
    def update(self):
        #starttime = time.time()
        
        #Clear self.msg of any garbage value
        self.msg = None
        #Check if server needs to receive next size of message
        if self.receiveMsgSizeNext:
            self.msg = self.clientsocket.recv(4)
            self.msgSizeBytes = int.from_bytes(bytes=self.msg, byteorder=sys.byteorder)
            if self.msgSizeBytes <= 0:
                print('Received negative or zero integer value from client...Ignoring..')
                self.msgSizeBytes = 0
            else:
                self.receiveMsgSizeNext = False
            return

        else:
            self.msg = self.clientsocket.recv(self.msgSizeBytes)
        
        #print(self.msg, int.from_bytes(bytes=self.msg, byteorder=sys.byteorder))
         
        if self.msg == None:
            print('no operation...client may have left...')
            return

        sensorReadings = self.msg.decode("utf-8")
        #Reset flag for receiving next message size
        self.receiveMsgSizeNext = True

        #Check for QUIT message, and stop self.timer and close self.sock if encountered
        if sensorReadings == "QUIT":
            #Stop timer - prevents update from being run multiple times
            print('Quit string received...plotter has been stopped')
            self.timer.stop()
            #Close self.sock for graceful exit
            self.sock.close()
            self.win.close()
            sys.exit(1)
        
        #Convert message into list of sensor data
        sensorReadings = LivePlot.parseLogLine(sensorReadings)

        if sensorReadings == None:
            print('no operation...doing nothing this update() iteration')
            return
        
        #print(len(sensorReadings), sensorReadings)
        #Determine if sensorReadings are AVSEN or PROPSEN
        if sensorReadings[1] == 'DB00':
            #Append time stamp and sensor readings
            for plotID in self.plotIDs:
                if self.epoch == 0:
                    self.epoch = sensorReadings[0]
                if plotID in range(0, 23):
                    '''
                    self.xlsts[plotID].append(sensorReadings[0] - self.epoch)
                    self.ylsts[plotID].append(sensorReadings[-plotID + 24])
                    '''
                    self.xlsts[plotID][0][self.xlsts[plotID][1]] = sensorReadings[0] - self.epoch
                    self.ylsts[plotID][0][self.ylsts[plotID][1]] = sensorReadings[-plotID + 24]

                    self.xlsts[plotID][1] += 1
                    self.ylsts[plotID][1] += 1

                    if self.xlsts[plotID][1] >= self.xlsts[plotID][0].shape[0]:
                        self.xlsts[plotID][0].resize(int(1.5 * self.xlsts[plotID][0].shape[0]), refcheck=False)
                    if self.ylsts[plotID][1] >= self.ylsts[plotID][0].shape[0]:
                        self.ylsts[plotID][0].resize(int(1.5 * self.ylsts[plotID][0].shape[0]), refcheck=False)
                    
                    if plotID not in self.movingPlotIDs:
                        #self.lineMap[plotID].setData(self.xlsts[plotID], self.ylsts[plotID])
                        self.lineMap[plotID].setData(self.xlsts[plotID][0][:self.xlsts[plotID][1]], self.ylsts[plotID][0][:self.ylsts[plotID][1]])
                    else:
                        '''
                        self.lineMap[plotID].setData(self.ylsts[plotID])
                        self.lineMap[plotID].setPos(-len(self.ylsts[plotID]), 0)
                        '''
                        self.lineMap[plotID].setData(self.ylsts[plotID][0][:self.ylsts[plotID][1]])
                        self.lineMap[plotID].setPos(-self.ylsts[plotID][1], 0)
                        

        elif sensorReadings[1] == 'DB01':
            #Append time stamp and sensor readings
            for plotID in self.plotIDs:
                if self.epoch == 0:
                    self.epoch = sensorReadings[0]
                if plotID in range(23, 56):
                    '''
                    self.xlsts[plotID].append(sensorReadings[0] - self.epoch)
                    self.ylsts[plotID].append(sensorReadings[-plotID + 57])
                    '''

                    self.xlsts[plotID][0][self.xlsts[plotID][1]] = sensorReadings[0] - self.epoch
                    self.ylsts[plotID][0][self.ylsts[plotID][1]] = sensorReadings[-plotID + 57]

                    self.xlsts[plotID][1] += 1
                    self.ylsts[plotID][1] += 1

                    if self.xlsts[plotID][1] >= self.xlsts[plotID][0].shape[0]:
                        self.xlsts[plotID][0].resize(int(1.5 * self.xlsts[plotID][0].shape[0]), refcheck=False)
                    if self.ylsts[plotID][1] >= self.ylsts[plotID][0].shape[0]:
                        self.ylsts[plotID][0].resize(int(1.5 * self.ylsts[plotID][0].shape[0]), refcheck=False)

                    if plotID not in self.movingPlotIDs:
                        #self.lineMap[plotID].setData(self.xlsts[plotID], self.ylsts[plotID])
                        self.lineMap[plotID].setData(self.xlsts[plotID][0][:self.xlsts[plotID][1]], self.ylsts[plotID][0][:self.ylsts[plotID][1]])
                    else:
                        '''
                        self.lineMap[plotID].setData(self.ylsts[plotID])
                        self.lineMap[plotID].setPos(-len(self.ylsts[plotID]), 0)
                        '''

                        self.lineMap[plotID].setData(self.ylsts[plotID][0][:self.ylsts[plotID][1]])
                        self.lineMap[plotID].setPos(-self.ylsts[plotID][1], 0)

        #print(time.time() - starttime)
        return

    #Creates plotter window and opens socket for communication with MCFS
    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        #LivePlot.update() is called every self.interval milliseconds
        self.timer.start(self.interval)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), PORT))

        #LivePlot server can accept up to 5 connection requestions before cancelling connection requests
        self.sock.listen(5)

        print(socket.gethostbyname(socket.gethostname()) + " beginning connection process")
        self.clientsocket, self.address = self.sock.accept()
        if self.clientsocket:
            print(f"Connection with {self.address} has been established!")

        #Check for "STRT" message
        self.msg = self.clientsocket.recv(4)
        
        if self.msg and (self.msg.decode("utf-8") == "STRT"):
            print("STRT sequence acknowledged...Ready to receive sensor data!")
        else:
            raise ValueError("STRT sequence not received...invalid data from client")

        #Begin plotter application, now that "STRT" was received
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

'''
New command line protocol for calling LivePlot.py:
python3 LivePlot.py [plotcode]
-plotcode is a base64 string representing all the AVSEN and PROPSEN sensors to plot
-when converted to binary, the first 56 bits of plotcode tell which sensor must be plotted (0 = don't plot, 1 = plot)
-Most significant bit is leftmost bit (aka bit 55), least significant bit is rightmost bit (aka bit 0)
-plotcode 56-bit diagram (assignment is from left to right, MSB to LSB):
--PROPSEN SENSORS (bits 55-23):
bits 55-40: pt01 -> pt16
bits 39-24: tc01 -> tc16
bit 23: load cell
--AVSEN SENSORS (bits 22-0):
bits 22-20: accelx1, accely1, accelz1
bits 19-17: gyrox1, gyroy1, gyroz1
bits 16-14: accelx2, accely2, accelz2
bits 13-11: gyrox2, gyroy2, gyroz2
bits 10-8: magx, magy, magz
bit 7: altitude
bit 6: pressure
bits 5-3: gps_lat, gps_long, gps_alt
bits 2-0: adxl_x, adxl_y, adxl_z
For example, a plotcode of 'AIAEAADwAgc=' tells LivePlot to plot the following sensors:
PT_01, PT_14, Load Cell, ACCEL_X_1, ACCEL_Y_1, ACCEL_Z_1, MAG_Y, ADXL_X, ADXL_Y, ADXL_Z
'''
#plots = LivePlot('logfile.log', 'AIAEAADwAgc=', sensorDicts.SENSOR_CONFIGS)
#plots = LivePlot('logfile.log', 'AP////////8=', sensorDicts.SENSOR_CONFIGS)


if len(sys.argv[1:]) != 1:
    print("Invalid command line args...closing plotter")
    sys.exit(1)

'''
#Check if there are at least 3 Base64 strings
if len(sys.argv[:4]) < 4:
    print("Invalid command line args...closing plotter")
    sys.exit(1)
'''

#Base64 strings deciding which symbols to plot, make sliding, and lock y range, respectively
plotting_b64str = sys.argv[1]
sliding_b64str = sys.argv[2]
locked_b64str = sys.argv[3]

minMaxValues = [(float(sys.argv[i]), float(sys.argv[i + 1])) for i in range(4, len(sys.argv), 2)]

#Create object
#plots = LivePlot('logfile.log', 'AIAEAADwAgc=', sensorDicts.SENSOR_CONFIGS)
#plots = LivePlot(logFilePath, b64str, sensorDicts.SENSOR_CONFIGS)
#plots = LivePlot('logfile.log', b64str, sensorDicts.SENSOR_CONFIGS)

#plots = LivePlot(plotting_b64str, sensorDicts.SENSOR_CONFIGS)
plots = LivePlot(plotting_b64str, sliding_b64str, locked_b64str, minMaxValues, sensorDicts.SENSOR_CONFIGS)

#Run window
plots.start()
