#!/usr/bin/python2
import csv
import sys
import numpy as np
Sr=list([])
O=list([])
Ti=list([])
Ge=list([])
reader = csv.reader(sys.stdin)
for row in reader:
    if (row[0]) == "Ge":
        Ge.append(float(row[1]))
    elif (row[0]) == "O":
        O.append(float(row[1]))
    elif (row[0]) == "Ti" :
        Ti.append(float(row[1]))
    elif (row[0]) == "Sr" :
        Sr.append(float(row[1]))

        
print(Sr,O,Ti,Ge)
print(Sr[-1]-Sr[-2], Sr[-2]-Sr[-3], O[0]-Ge[-1])
