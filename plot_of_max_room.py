# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:17:38 2018

@author: Matteo
"""
import pandas 
from matplotlib import pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
max_room = pandas.read_csv('http://wemapserver.sytes.net/Utility%20WEMAP/meas_of_2t.csv',sep=',') 
fig1 = plt.figure(figsize=(30,15))
max_s = np.max(max_room['speedInternet'])
min_s = np.min(max_room['speedInternet'])
med = np.median(max_room['speedInternet'])
plt.hist(max_room['speedInternet'])
plt.title('Distribution of Speed in Room 2t max='+str(max_s)+' min='+str(min_s) + 'median='+str(med),fontsize = 40)
plt.ylabel('Occurences',fontsize=30)
plt.grid()
plt.xlabel('Speed [Mbit/s]',fontsize = 30)
fig1.savefig('histo.png')

#%%
import matplotlib.dates as dates
from datetime import datetime, date, time
from sklearn import preprocessing
import matplotlib as mpl

one_day = pandas.read_csv('http://wemapserver.sytes.net/Utility%20WEMAP/meas_of_2t.csv',sep=',',skiprows=15)
one_day.columns = max_room.columns
new_x = [d.split(' ')[1][0:5] for d in one_day['time']]

mean_speed = np.mean(one_day['speedInternet'])
max_speed = np.max(one_day['speedInternet'])
norm_speed = [(value-mean_speed)/np.linalg.norm(one_day['speedInternet']) for value in one_day['speedInternet']]


mean_rssi = np.mean(one_day['RSSI'])
norm_rssi = [(value-mean_rssi)/np.linalg.norm(one_day['RSSI']) for value in one_day['RSSI']]

mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20

fig = plt.figure(figsize=(30,15))
plt.plot(new_x, norm_speed,label='Speed',linewidth = 3.0)
plt.plot(norm_rssi,label = 'RSSI',linewidth = 3.0)
plt.xticks(rotation=90)
plt.title('Monitoring Wifi Speed and Signal Strength Before-During-After a Lecture',fontsize = 40)
plt.ylabel('Normalized values',fontsize = 25)
plt.xlabel('Hour and Time of the Measurement - 09/03',fontsize = 25)
plt.legend(prop={'size': 30})
plt.grid()
fig.savefig('result.png')
plt.show()
