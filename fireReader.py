# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import math
import numpy as np
import time
   
def cheapDist(lat1,lon1,lat2,lon2):
    R = 6371e3 # metres
    x = (lon2-lon1) * math.cos((lat1+lat2)/2)
    y = (lat2-lat1)
    d = math.sqrt(x*x + y*y) * R
    return d

def goodDist(lat1,lon1,lat2,lon2):
    R = 6371e3; # metres
    phi1 = lat1
    phi2 = lat2
    dphi = lat2-lat1
    dlamb = lon2-lon1

    a = math.sin(dphi/2) * math.sin(dphi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(dlamb/2) * math.sin(dlamb/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

    d = R * c
    return d

# read data
df=pd.read_csv('VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv', sep=',',header=None)
FireTotal = []
CloseTotal = []
FireDist = []
Close = []
print('data read')

# convert lat lon coordinates to radians
for line in range(1,len(df)):
    df[0][line] = math.radians(float(df[0][line]))
    df[1][line] = math.radians(float(df[1][line]))
print('radian conversion complete')

print('data has %i rows, starting distance calculation loop' %len(df))
    
#c = []
for j in range(1,len(df)):
    FireDist = []
    Close = []
    #a = time.clock()
    for i in range(1,j):
        dist = cheapDist(df[0][j],df[1][j],df[0][i],df[1][i])
        FireDist.append(dist)
        Close.append((dist<400)*1)
        
    FireTotal.append(FireDist)
    CloseTotal.append(Close)
    print(j)
    #b = time.clock()
    #c.append(b-a)
    #print(j, c[-1])
    
print('finished, saving...')
    
import csv
f = open('distances.csv','w',newline='')
w = csv.writer(f)
w.writerows(FireTotal)
f.close()
f = open('close.csv','w',newline='')
w = csv.writer(f)
w.writerows(CloseTotal)
f.close()

#print('starting distance check loop')
#
#wd =pd.read_csv('results.csv', sep=',',header=None)
#
#del j, i
#
#for j in range(0,len(wd)):
#    for i in range(0,len(wd)):
#        wd[j][i] = wd[j][i]<np.float64(400)
#    print(j)
#    
#wd.to_csv('closest.csv',sep=',',header=None)