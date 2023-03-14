#This program is for creating a figure that has the following:
#1. top panel: phase micrographs of each strain grown in LB planktonic, showing cell morphology
#2. middle panel: cell width profiles for each strain, showing the % of cells with width devations exceeding certain thresholds
#3. bottom panel: box plot (or other distribution plot type) of max cell widths for each strain
#
#strains for this figure are: WT, mptA KO, mptA KO + L5::mptA-dendra2-flag, mptC OE, mptC KO, embC KD

#import micrographs for each strains

#import data from csv files for cell width profile data

#plot cell width profiles for each strain

#calculate the max cell width of each cell for each strain

#plot max cell widths of each cell for each strain

################################################################################
from matplotlib import pyplot as plt
import math # 'math' needed for 'sqrt'
import csv
import os
import random


#fig, ax = plt.subplots(nrows=3, ncols=1)
fig = plt.figure(figsize=(11.3,11))
ax01 = plt.subplot2grid((15, 6), (0, 0), rowspan=2, colspan=1)
ax02 = plt.subplot2grid((15, 6), (0, 1), rowspan=2, colspan=1)
ax03 = plt.subplot2grid((15, 6), (0, 2), rowspan=2, colspan=1)
ax04 = plt.subplot2grid((15, 6), (0, 3), rowspan=2, colspan=1)
ax05 = plt.subplot2grid((15, 6), (0, 4), rowspan=2, colspan=1)
ax06 = plt.subplot2grid((15, 6), (0, 5), rowspan=2, colspan=1)
ax1 = plt.subplot2grid((15, 6), (2, 0), rowspan=4, colspan=6)
ax2 = plt.subplot2grid((15, 6), (7, 0), rowspan=7, colspan=6)

ax01.set(ylabel='Phase')


fig.patch.set_facecolor('w')
afont = {'fontname':'Bitstream Vera Sans'}

ax01.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)
ax02.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)
ax03.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)
ax04.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)
ax05.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)
ax06.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False,labelleft=False,left=False,right=False)


#Distance function
def distance(xi,xii,yi,yii):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return math.sqrt(sq1 + sq2)

# Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)
###############################################################################
your_directory = os.getcwd()
#WT:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('WT.csv', "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)

    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+0)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)
        #ax1.plot(x,y, c='tomato', alpha=0.1)


        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()

percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+0, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+0, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+0, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+0, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)
ax1.set(xlabel='Normalized cell length', ylabel='Cell width (' + u"\u03BCm" + ')') #changed 'cell profile' to 'normalized cell length'
ax1.xaxis.set_label_coords(0.105, -0.11)
ax1.plot([-0.15,7.05],[1.2,1.2], 'y--', linewidth=2)
ax1.plot([-0.15,7.05],[1.4,1.4], c='#fc8400', linestyle ='--', linewidth=2)
ax1.plot([-0.15,7.05],[1.6,1.6], 'r--', linewidth=2)
ax1.tick_params(direction='out', axis='both')
ax1.set_ylim([0,2])
ax1.set_xlim([-0.15,7.05])
ax1.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
ax1.set_xticks([0, 0.5, 1, 1.2, 1.7, 2.2, 2.4, 2.9, 3.4, 3.6, 4.1, 4.6, 4.8, 5.3, 5.8])
ax1.set_xticklabels(['pole', 'midcell', 'pole','', '', '','', '', '','', '', '','', '', ''])
ax1.tick_params(axis='x', which='major', pad=-2)
ax1.tick_params(axis='both', which='major', labelsize=12,top=False,right=False)

Max_widths_WT = Max_widths


ax1.vlines(x=[1.05, 2.25, 3.45, 4.65, 5.85], ymin=0, ymax=2, colors='k')

#########################################################################
#mptA KO:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('mptA_KO.csv', "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)

    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+1.2)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)

        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()


percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+1.2, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+1.2, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+1.2, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+1.2, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)

Max_widths_mptA_KO = Max_widths


##########################################################################
#mptA comp:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('comp.csv', "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)
    # randomly sample cells from total cells
    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+2.4)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)

        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()


percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+2.4, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+2.4, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+2.4, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+2.4, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)

Max_widths_mptA_comp = Max_widths

##########################################################################
#mptC KO:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('mptC_KO.csv', "rb") as inFile:
#with open(file, "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)

    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+3.6)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)

        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()


percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+3.6, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+3.6, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+3.6, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+3.6, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)

Max_widths_mptC_KO = Max_widths


##########################################################################
#mptC OE:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('WT_mptC_OE.csv', "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)

    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+4.8)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)

        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()


percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+4.8, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+4.8, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+4.8, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+4.8, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)

Max_widths_mptC_OE = Max_widths


##########################################################################
#embC KD:
x = []
y = []
Thresh_080 = 0
Thresh_120 = 0
Thresh_140 = 0
Thresh_160 = 0
files_name = "test"


with open('embC_KD_ATC.csv', "rb") as inFile:
    csv_reader = csv.reader(inFile, delimiter=',')
    MeshCells = []
    Max_widths = []
    for row in csv_reader:
        if len(row) < 7:
            continue
        if len(row[6]) < 10:
            continue
        MeshCells.append(row[6])

    # This makes sure that the sample size reverts to the max number of cells if there aren't enough cells in the csv file
    Sample_Size = 100
    if len(MeshCells) < Sample_Size:
        Sample_Size = len(MeshCells)

    MeshCells = random.sample(MeshCells, k=Sample_Size)

    for i in MeshCells:
        x = []
        y = []
        CellWidths = []
        mod_i = str(i)
        mod_i = mod_i.translate(None, "['")
        mod_i = mod_i.translate(None, "']")
        CoordinateList = mod_i.split(";")
        x1List = CoordinateList[0].split(" ")
        while ("" in x1List):
            x1List.remove("")
        y1List = CoordinateList[1].split(" ")
        while ("" in y1List):
            y1List.remove("")
        x2List = CoordinateList[2].split(" ")
        while ("" in x2List):
            x2List.remove("")
        y2List = CoordinateList[3].split(" ")
        while ("" in y2List):
            y2List.remove("")
        for e in range(len(x1List)):
            CellWidths.append(distance(float(x1List[e]),float(
            x2List[e]),float(y1List[e]),float(y2List[e])))

        count = 0
        for e in range(len(CellWidths)):
            x.append(((float(count))/(float(len(CellWidths)-1)))+6)
            count = count + 1
            y.append(CellWidths[e]/13.5135)

        if max(y) > 0.8:
            Thresh_080 += 1
        if max(y) > 1.2:
            Thresh_120 += 1
        if max(y) > 1.4:
            Thresh_140 += 1
        if max(y) > 1.6:
            Thresh_160 += 1
        ax1.plot(x,y, c='k', alpha=0.2)

        Max_widths.append((max(CellWidths))/13.5135)

    inFile.close()

percentThresh_080 = int(100*float(Thresh_080)/float((len(MeshCells))))
percentThresh_120 = int(100*float(Thresh_120)/float((len(MeshCells))))
percentThresh_140 = int(100*float(Thresh_140)/float((len(MeshCells))))
percentThresh_160 = int(100*float(Thresh_160)/float((len(MeshCells))))


ax1.text((0.003-0.14)+6, 1.25, str(percentThresh_120) + '%', fontsize=12, color ='y', **afont)
ax1.text((0.003-0.14)+6, 1.45, str(percentThresh_140) + '%', fontsize=12, color ='#fc8400', **afont)
ax1.text((0.003-0.14)+6, 1.65, str(percentThresh_160) + '%', fontsize=12, color ='r')
ax1.text((0.015-0.14)+6, 1.815, 'n = ' + str(len(MeshCells)) + ' cells', fontsize=12, color ='k', **afont)

Max_widths_embC_KD = Max_widths

##########################################################################
bp = ax2.boxplot([Max_widths_WT,Max_widths_mptA_KO,Max_widths_mptA_comp,Max_widths_mptC_KO,Max_widths_mptC_OE,Max_widths_embC_KD], sym='', widths=0.75, patch_artist=True)
ax2.set_ylim([0.75,2.5])
ax2.set(ylabel='Maximum cell width (' + u"\u03BCm" + ')')
lab1='$\it{}$' +'WT'
lab2=r'$\Delta$'+'$\it{mptA}$'
lab3=r'$\Delta$'+'$\it{mptA}$'+' '+'$\it{L5}$'+'::'+'$\it{mptA}$'
lab4=r'$\Delta$'+'$\it{mptC}$'
lab5='$\it{mptC}$' + ' OE'
lab6='$\it{embC}$' + ' KD'
ax2.set_xticklabels([lab1, lab2, lab3, lab4, lab5, lab6], rotation = 45, ha='right')
ax2.tick_params(axis='both', which='major', labelsize=12,top=False,bottom=False)
ax2.tick_params(axis='x', which='major', pad=8, labelsize=15)
ax2.tick_params(axis='y', which='major', labelsize=12)
ax2.set_yticks([0.8,1.0,1.2,1.4,1.6, 1.8, 2.0])
ax2.yaxis.set_label_coords(-0.08, 0.38) #this is for just plotting the box plot

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='k', linewidth=2, ls = '-')

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='k', linewidth=2, ls = '-')

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='k', linewidth=2, ls = '-')

for box in bp['boxes']:
    # change outline color
    box.set( color='k', linewidth=2)
    # change fill color
    box.set( facecolor='r' )

bp['boxes'][0].set(facecolor='tomato')
bp['boxes'][1].set(facecolor='plum')
bp['boxes'][2].set(facecolor='palegreen')
bp['boxes'][3].set(facecolor='cornflowerblue')
bp['boxes'][4].set(facecolor='orange')
bp['boxes'][5].set(facecolor='yellow')
##########################################################################

plt.subplots_adjust(wspace=0,
                    hspace=0)


####################################
im1 = plt.imread("WT_200x300px.png")
im2 = plt.imread("mptA_KO_200x300px.png")
im3 = plt.imread("comp_200x300px.png")
im4 = plt.imread("mptC_KO_200x300px.png")
im5 = plt.imread("WT_mptC_OE_200x300px.png")
im6 = plt.imread("embC_KD_200x300px.png")

ax01.imshow(im1, cmap='gray', aspect='equal')
ax02.imshow(im2, cmap='gray', aspect='equal')
ax03.imshow(im3, cmap='gray', aspect='equal')
ax04.imshow(im4, cmap='gray', aspect='equal')
ax05.imshow(im5, cmap='gray', aspect='equal')
ax06.imshow(im6, cmap='gray', aspect='equal')


ax01.set_title('$\it{}$' +'WT', **afont)
ax02.set_title(r'$\Delta$'+'$\it{mptA}$', **afont)
ax03.set_title(r'$\Delta$'+'$\it{mptA}$'+' '+'$\it{L5}$'+'::'+'$\it{mptA}$', **afont)
ax04.set_title(r'$\Delta$'+'$\it{mptC}$', **afont)
ax05.set_title('$\it{mptC}$' + ' OE', **afont)
ax06.set_title('$\it{embC}$' + ' KD', **afont)

## add scale bars:
import matplotlib.patches as patches

# Create a Rectangle patch
rect1 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
rect2 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
rect3 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
rect4 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
rect5 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
rect6 = patches.Rectangle((6, 183), 13.5135*5, 10, linewidth=0, edgecolor='none', facecolor='w')
# Add the patch to the Axes
ax01.add_patch(rect1)
ax02.add_patch(rect2)
ax03.add_patch(rect3)
ax04.add_patch(rect4)
ax05.add_patch(rect5)
ax06.add_patch(rect6)

ax01.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
ax02.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
ax03.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
ax04.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
ax05.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
ax06.text(12, 176, '5 ' + u"\u03BCm", fontsize=10, color ='w', **afont)
####################################

plt.show()
