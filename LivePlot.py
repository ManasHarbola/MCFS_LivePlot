import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import base64
from random import randint
import numpy as np
import re
import sys
import os
import time
import sensorDicts

class LivePlot:
    def __init__(self, logFilename, plotcode, configDict):
        #Check parameter type
        if not(isinstance(configDict, dict)):
            raise TypeError("parameter 'configDict' of invalid type")
        
        #self.plotIDs contains the record of which sensors to plot, each id being unique being between 0 and 52
        self.plotIDs = LivePlot.getIndices(plotcode)

        if len(self.plotIDs) == 0:
            raise ValueError("no sensors selected to plot")
        
        columnSize = int(np.log(len(self.plotIDs)) / np.log(2))
        rowSize = int(np.ceil(len(self.plotIDs) / columnSize))
        
        self.save_count = configDict["save_count"]
        self.interval = configDict["interval"]
        self.blit = configDict["blit"]
        self.subplotDims = (rowSize, columnSize)
        self.logFilename = logFilename

        #self.epoch is the reference unix timestamp of t=0s
        self.epoch = 0

        #self.xlsts = [[[] for i in range(self.subplotDims[1])] for j in range(self.subplotDims[0])]
        #self.ylsts = [[[] for i in range(self.subplotDims[1])] for j in range(self.subplotDims[0])]
        self.xlsts = {plotID : [] for plotID in self.plotIDs}
        self.ylsts = {plotID : [] for plotID in self.plotIDs}


        self.xlims = {plotID : configDict[plotID][3:5] for plotID in self.plotIDs}
        self.ylims = {plotID : configDict[plotID][5:7] for plotID in self.plotIDs}


        self.fig, self.axs = plt.subplots(*self.subplotDims, figsize=(14, 10), squeeze=False)
        plt.subplots_adjust(hspace=0.60)
        plt.style.use('fivethirtyeight')
        colors = plt.rcParams['axes.prop_cycle']()
        self.fig.tight_layout()

        self.lines = []

        #self.plotIDMap is a dictionary that maps sensor ID to a particular axs
        self.plotIDMap = {}
        #self.lineMap is a dictionary mapping sensor ID to line
        self.lineMap = {}

        idx = 0
        for i in range(self.subplotDims[0]):
            for j in range(self.subplotDims[1]):
                currPlotID = self.plotIDs[idx]                
                self.plotIDMap[currPlotID] = self.axs[i][j]

                self.axs[i][j].set_xlim(self.xlims[currPlotID])
                self.axs[i][j].set_ylim(self.ylims[currPlotID])
                self.axs[i][j].set_title(configDict[currPlotID][0], fontdict=configDict['title_font'])
                self.axs[i][j].set_xlabel(configDict[currPlotID][1])
                self.axs[i][j].set_ylabel(configDict[currPlotID][2])
                self.axs[i][j].grid()
                
                c = next(colors)['color']

                #Check if sensor must be plotted with dotted lines
                if configDict[currPlotID][7] == True:
                    line, = self.axs[i][j].plot(self.xlsts[currPlotID], self.ylsts[currPlotID], marker='o', color=c)
                    self.lineMap[currPlotID] = line
                else:
                    line, = self.axs[i][j].plot(self.xlsts[currPlotID], self.ylsts[currPlotID], color=c)
                    self.lineMap[currPlotID] = line

                self.lines.append(line)
                idx += 1
        
        self.ani =  animation.FuncAnimation(self.fig,
                self.animate,
                fargs=(LivePlot.tail(self.logFilename),),
                save_count=self.save_count,
                interval=self.interval,
                blit=self.blit)

    #Generator for returning new points written to file
    def tail(filename):
        PAUSE_DURATION = 0.1    #Duration before tail continues
        RECONNECT_PERIOD_SECS = 5 #Duration tail will try to continue listening if no new data exists
        ATTEMPTED_TRIES = RECONNECT_PERIOD_SECS / PAUSE_DURATION    #Number of tries tail will continue checking for new line
        with open(filename) as f:
            f.seek(0, os.SEEK_END)
            while True:
                fileLine = f.readline()
                if not fileLine:    #line was None
                    ATTEMPTED_TRIES -= 1
                    time.sleep(PAUSE_DURATION)
                    if ATTEMPTED_TRIES < 1:
                        raise StopIteration
                    continue
                else:
                    ATTEMPTED_TRIES = RECONNECT_PERIOD_SECS / PAUSE_DURATION    #Reset value
                yield fileLine

    #Helper function for parsing log lines one by one
    #TODO: return special list for EOF line
    def parseLogLine(line):
        lst = re.split(" |\|", line)
        if len(lst) < 2 or (lst[1] not in ['DB00', 'DB01']):
            return None
        #Check bytecode DB00 -> AVSEN, DB01 -> PROPSEN
        if lst[1] == 'DB00':
            return [float(lst[0]), 'DB00', *[float(value[2:]) for value in lst[2:]]]
        elif lst[1] == 'DB01':
            return [float(lst[0]), 'DB01', *[float(value[3:]) for value in lst[2:]]]

    def getIndices(s):
        b = bin(int.from_bytes(base64.b64decode(s), "big"))[2:]
        #return [len(b) - i - 1 for i in range(len(b)) if b[i] == '1']
        return [len(b) - 1 - i for i in range(len(b)) if b[i] == '1']

    #Method for starting animation
    def initAnimation(self):
        plt.show()

    def animate(self, i, listener):
        starttime = time.time()
        try:
            sensorReadings = LivePlot.parseLogLine(next(listener))
        except StopIteration:
            print("Log File hasn't been updated for 5 seconds...Stopping Plotter")
            self.ani.event_source.stop()
            return self.lines

        #print(sensorReadings)

        if sensorReadings == None:
            print('no operation')
            return self.lines

        needReplot = False
        #Determine if sensorReadings are AVSEN or PROPSEN
        if sensorReadings[1] == 'DB00':
            #Append time stamp and sensor readings
            for plotID in self.plotIDs:
                if self.epoch == 0:
                    self.epoch = sensorReadings[0]
                if plotID in range(0, 20):
                    self.xlsts[plotID].append(sensorReadings[0] - self.epoch)
                    self.ylsts[plotID].append(sensorReadings[-plotID + 21])
                    self.lineMap[plotID].set_xdata(self.xlsts[plotID])
                    self.lineMap[plotID].set_ydata(self.ylsts[plotID])

        elif sensorReadings[1] == 'DB01':
            #Append time stamp and sensor readings
            for plotID in self.plotIDs:
                if self.epoch == 0:
                    self.epoch = sensorReadings[0]
                if plotID in range(20, 53):
                    self.xlsts[plotID].append(sensorReadings[0] - self.epoch)
                    self.ylsts[plotID].append(sensorReadings[-plotID + 54])
                    self.lineMap[plotID].set_xdata(self.xlsts[plotID])
                    self.lineMap[plotID].set_ydata(self.ylsts[plotID])

        for plotID in self.plotIDs:
            #self.lineMap[plotID].set_xdata(self.xlsts[plotID])
            #self.lineMap[plotID].set_ydata(self.ylsts[plotID])

            #print(plotID, self.xlsts[plotID], self.ylsts[plotID])

            #Rescale x-axis
            if len(self.xlsts[plotID]) > 0 and self.xlsts[plotID][-1] > self.plotIDMap[plotID].get_xlim()[1]:
                self.plotIDMap[plotID].set_xlim([self.plotIDMap[plotID].get_xlim()[0], 2.0 * self.plotIDMap[plotID].get_xlim()[1]])
                needReplot = True

            #Rescale y-axis
            if len(self.ylsts[plotID]) > 0 and self.ylsts[plotID][-1] > self.plotIDMap[plotID].get_ylim()[1]:
                self.plotIDMap[plotID].set_ylim([self.plotIDMap[plotID].get_ylim()[0], self.ylsts[plotID][-1]])
                needReplot = True
            elif len(self.ylsts[plotID]) > 0 and self.ylsts[plotID][-1] < self.plotIDMap[plotID].get_ylim()[0]:
                self.plotIDMap[plotID].set_ylim([self.ylsts[plotID][-1], self.plotIDMap[plotID].get_ylim()[1]])
                needReplot = True

        if needReplot:
            print('replot needed')
            plt.draw()

        print(time.time() - starttime)
        return self.lines

        



#sensorMappings = {'SENSOR1': (0, 0), 'SENSOR2' : (0, 1), 'SENSOR3' : (1, 0), 'SENSOR4' : (1, 1)}
#plot = LivePlot('logfile.log', subplotDims=(2, 2), identifiers=sensorMappings, interval=200)

#TODO: replace identifiers with something like ['Sensor1', 2, 'Sensor2', 3, ...], where idenitifer is followed by number of sensor values to read from line


'''
New command line protocol for calling LivePlot.py:
python3 LivePlot.py [plotcode]

-plotcode is a base64 string representing all the AVSEN and PROPSEN sensors to plot
-when converted to binary, the first 53 bits of plotcode tell which sensor must be plotted (0 = don't plot, 1 = plot)
-Most significant bit is leftmost bit (aka bit 52), least significant bit is rightmost bit (aka bit 0)
-plotcode 53-bit diagram (assignment is from left to right, MSB to LSB)

PROPSEN SENSORS (bits 52-20):
bits 52-37: pt01 -> pt16
bits 36-21: tc01 -> tc16
bit 20: load cell
AVSEN SENSORS (bits 19-0):
bits 19-17: accelx1, accely1, accelz1
bits 16-14: gyrox1, gyroy1, gyroz1
bits 13-11: accelx2, accely2, accelz2
bits 10-8: gyrox2, gyroy2, gyroz2
bits 7-5: magx, magy, magz
bit 4: altitude
bit 3: pressure
bits 2-0: gps_lat, gps_long, gps_alt

For example, a plotcode of 
'''


'''
#Program now uses command line arguments
if sys.argv[1:] not in [['-plotAVSEN'], ['-plotPROPSEN']]:
    print("Invalid command line arguments")
elif sys.argv[1] == '-plotAVSEN':
    plots = LivePlot(sensorConfigs.AVSEN_PLOT_CONFIG)
    plots.initAnimation()
else:
    plots = LivePlot(sensorConfigs.PROPSEN_PLOT_CONFIG)
    plots.initAnimation()
'''

'''
if len(sys.argv[1:]) != 1:
    print("Invalid command line args")
'''

#plots = LivePlot('logfile.log', 'AAAAAA4AAA==', sensorDicts.SENSOR_CONFIGS)
plots = LivePlot('logfile.log', 'AAAAAA///w==', sensorDicts.SENSOR_CONFIGS)
plots.initAnimation()