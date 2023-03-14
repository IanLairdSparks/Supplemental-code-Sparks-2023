# this script takes fluorescence profile data from csv file in which each cell_list fluorescence profile
# taken from Oufti's output Matlab file is a column


#import itertools
#import sys
#import matplotlib
from matplotlib import pyplot as plt
#import math # 'math' needed for 'sqrt'
import csv
import numpy as np
#import re
#import os
#from scipy.stats import kde
#from scipy.interpolate import spline
#import matplotlib.colors as colors
#from scipy.optimize import curve_fit
#from scipy.interpolate import spline
#import matplotlib.colors as colors
#import matplotlib.gridspec as gridspec
#import random
#from matplotlib.colors import LogNorm
################################################################################

################################################################################
# first strain's fluorescence profile population data
file = 'KO_FL.csv'
#open csv file
with open(file, "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    #next(csv_reader) # read first line to skip it
    ncol = len(next(csv_reader)) # Read first line and count columns at the same time
    #initialize list of cells
    cell_list = []
    #add an empty list for each cell to the cell list
    for i in range(ncol):
        cell_list.append([])
    #add FL signal values for each cell
    for row in csv_reader:
        for i in range(len(cell_list)):
            if row[i] != "":
                cell_list[i].append(float(row[i]))
    inFile.close()



#initialize the x and y variables
x = []
y = []
y2 = []
for cell in cell_list:
    for i in range(len(cell)):
        normalized_lateral_position = (float(i+1))/(float(len(cell)))
        x.append(normalized_lateral_position)
        y.append(float(cell[i]))
        normalized_FL = (float(cell[i]))/(float(max(cell)))
        y2.append(normalized_FL)

#set order of polynomial regression
degree = 700
#plot points
fig, ax = plt.subplots(1, 1, squeeze=False)
#make a high-order polynomial regression of the scatter data
Xfit = np.array(x)
#Yfit = np.array(y) #for absolute Fluorescence
Yfit = np.array(y2) #for normalized Fluorescence
fittedParameters = np.polyfit(Xfit, Yfit, degree)
# create data for the fitted equation plot
xModel = np.linspace(min(Xfit), 1)
yModel = np.polyval(fittedParameters, xModel)
# now the model as a line plot
ax[0,0].plot(xModel, yModel, c='r', linewidth=2)
################################################################################

################################################################################
# second strain's fluorescence profile population data
file = 'WT_FL.csv'
#open csv file
with open(file, "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    #next(csv_reader) # read first line to skip it
    ncol = len(next(csv_reader)) # Read first line and count columns at the same time
    #initialize list of cells
    cell_list = []
    #add an empty list for each cell to the cell list
    for i in range(ncol):
        cell_list.append([])
    #add FL signal values for each cell
    for row in csv_reader:
        for i in range(len(cell_list)):
            if row[i] != "":
                cell_list[i].append(float(row[i]))
    inFile.close()



#initialize the x and y variables
x = []##
y = []##
y2 = []##
for cell in cell_list:
    for i in range(len(cell)):
        normalized_lateral_position = (float(i+1))/(float(len(cell)))
        x.append(normalized_lateral_position)
        y.append(float(cell[i]))
        normalized_FL = (float(cell[i]))/(float(max(cell)))
        y2.append(normalized_FL)
    #ax[0,0].plot(x, y2, c='b', linewidth=2)
#set order of polynomial regression
degree = 700
#plot points
#make a high-order polynomial regression of the scatter data
Xfit = np.array(x)
#Yfit = np.array(y) #for absolute Fluorescence
Yfit = np.array(y2) #for normalized Fluorescence
fittedParameters = np.polyfit(Xfit, Yfit, degree)
# create data for the fitted equation plot
xModel = np.linspace(min(Xfit), 1)
yModel = np.polyval(fittedParameters, xModel)
# now the model as a line plot
ax[0,0].plot(xModel, yModel, c='b', linewidth=2)
################################################################################

################################################################################
ax[0,0].set_xlim([-0.01, 1.01])
ax[0,0].set_ylim([0, 1])
fig.patch.set_facecolor('w')
ax[0,0].set(xlabel='Normalized cell length', ylabel='Fluorescence intensity')
ax[0,0].set_title("20hr LB log phase + 15min 10 " + u"\u03bcM" + " RADA")
ax[0,0].set_xticks([0, 0.5, 1])
ax[0,0].set_xticklabels(['new pole', 'midcell', 'old pole'])
ax[0,0].plot([0.05,0.1],[0.8,0.8], c='b', linewidth=2)
ax[0,0].text(0.11, 0.79, "WT, n = 78", fontsize=15, color ='b')
ax[0,0].plot([0.05,0.1],[0.7,0.7], c='r', linewidth=2)
ax[0,0].text(0.11, 0.69, "mptA KO, n = 71", fontsize=15, color ='r')

plt.show()
