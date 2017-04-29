# -*- coding: utf-8 -*-
"""
fireReader.py
Takes a csv file from 
https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/text/VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv
and processes coordinates where fire is detected into clusters of points
that represent a possible larger fire.
Written for NASA Space Apps Challenge 2017
Lachlan Robinson 30/04/2017
"""

import pandas as pd
import math
import numpy as np
import time

startTime = time.clock()
   
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

def ClusterFunc(outer,Cluster,start):
    appended = False
    for j in outer:
        if j in Cluster:
            continue
        for i in range(len(CloseTotal[j])):
            if CloseTotal[j][i] > 0:
                if True==start:
                    Cluster.append(j)
                    start=False
                Cluster.append(i)
    if False==start and True==appended:
        ClusterFunc(Cluster,Cluster,start)
    return start
            
Clusters = []
Cluster = []
ClusterIndex = []
start = True
for j in range(len(CloseTotal)):
    #print(j, start)
    j = [j]
    if False==start:
        ClusterIndex.append(len(Cluster))
        Clusters.append(Cluster)
        Cluster = []
        start = True
        continue
    start = ClusterFunc(j,Cluster,start)

f = open('clusters.csv','w',newline='')
w = csv.writer(f)
w.writerows(Clusters)
f.close()

RealClusters = []
for j in range(len(ClusterIndex)):
    if ClusterIndex[j]>3:
        RealClusters.append(Clusters[j])

RealCoords = []
for j in RealClusters:
    RealCoord = []
    for i in j:
        #YYYY-MM-DDThh:mm:ssZ
        RealCoord.append((math.degrees(df[0][i+1]),math.degrees(df[1][i+1]),
                          (df[5][i+1] + 'T' + df[6][i+1][:2] + ':' + df[6][i+1][2:] + ':00Z'),
                          int(df[5][i+1][8:10] + df[6][i+1][:2] + df[6][i+1][2:])))
    RealCoords.append(RealCoord)
    
latestUpdate = df[5][len(df[0])-1] + 'T' + df[6][len(df[0])-1][:2] + ':' + df[6][len(df[0])-1][2:] + ':00Z'

things = []
#timeVecs = []
state = []
for i in range(len(RealCoords)):
    #timeVec = []
    thing = []
    RealCoords[i] = sorted(RealCoords[i], key=lambda time: time[3])
    for j in range(len(RealCoords[i])):
        thing.append(RealCoords[i][j][3])
        thingy = np.histogram(thing)
    things.append(thingy)
#    for j in range(1,len(RealCoords[i])):
#        timeVec.append(RealCoords[i][j][3] - RealCoords[i][j-1][3])
#    timeVecs.append(timeVec)    
#    for k in reversed(range(len(timeVec))):
#        if timeVec[k]>500 and k>(len(timeVec)/2):
#            print(i,k,'greater')
#            state.append(-1)
#            break
#        elif timeVec[k]>500 and k<(len(timeVec)/2):
#            print(i,k,'lesser')
#            state.append(1)
#            break
#        elif k == 0:
#            state.append(0)
#            print(i,k)

for i in things:
    last = 0
    first = -1
    for j in reversed(i[0]):
        if j and not last:
            last = j
            continue
        if j and last:
            first = j
    #print(last,first)
    if first >-1:
        if last>first:
            state.append(1)
        elif first>last:
            state.append(-1)
        else:
            state.append(0)
    else:
        state.append(0)

endTime = time.clock()
print('Processing time: %f' %(endTime-startTime))