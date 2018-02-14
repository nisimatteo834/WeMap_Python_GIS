# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:24:47 2018

@author: Matteo
"""
import sys
from math import sin, cos, sqrt, atan2, radians
import numpy as np
import pandas
from matplotlib import pyplot
from shapely import geometry
from shapely.geometry.polygon import LinearRing, Polygon
import fiona
import utm

file = pandas.read_csv('C:\\Users\\Matteo\\Desktop\\aule_i_center.csv',sep='\t') 
print (file)


#%%I

txt = open('C:\\Users\\Matteo\\Desktop\\prova.txt','r')
lines = txt.readlines()




ax = fig.add_subplot(111)
ax.plot(x, y, color='#6699cc', alpha=0.7,
    linewidth=3, solid_capstyle='round', zorder=2)
ax.set_title('Polygon')
#%%

angolo = 26.42/180*3.14
angolo_comp = (90-26.42)/180*3.14
roomInPoints = {}
for x in range(0,len(file)):
    center_lat = file['lat'][x]
    center_long = file['long'][x]
    center_utm = utm.from_latlon(center_lat,center_long)
    nl = file['lunghezza'][x]/6*np.sin(angolo_comp)    
    ns = file['lunghezza'][x]/6*np.sin(angolo)
    el = file['larghezza'][x]/4*np.cos(angolo)
    es = file['larghezza'][x]/4*np.cos(angolo_comp)
#    nl = 27.19/5*np.sin(angolo_comp)    
#    ns = 27.19/5*np.sin(angolo)
#    el = 9.65/5*np.cos(angolo)
#    es = 9.65/5*np.cos(angolo_comp)
    center_lat = center_utm[1]
    center_long = center_utm[0]
    zones = []
    roomInPoints[file['name'][x]] = []
    zones.append(utm.to_latlon(center_long+ns-el,center_lat + nl + es,32,'T'))
    zones.append(utm.to_latlon(center_long+ns,center_lat+nl,32,'T'))
    zones.append(utm.to_latlon(center_long+ns+el,center_lat+nl-es,32,'T'))
    zones.append(utm.to_latlon(center_long-el,center_lat+es,32,'T'))
    zones.append(utm.to_latlon(center_long,center_lat,32,'T'))
    zones.append(utm.to_latlon(center_long+el,center_lat-es,32,'T'))
    zones.append(utm.to_latlon(center_long-ns-el,center_lat-nl+es,32,'T'))
    zones.append(utm.to_latlon(center_long-ns,center_lat-nl,32,'T'))
    zones.append(utm.to_latlon(center_long-ns+el,center_lat-nl-es,32,'T'))
    
    roomInPoints[file['name'][x]] = zones.copy()
        
df = pandas.DataFrame.from_dict(roomInPoints,orient='index')
df = df.stack()
df.to_csv('C:\\Users\\Matteo\\Desktop\\prova.csv')


   #%% 
    
    points = []
    points.append(geometry.Point( center_long+es-el,center_lat + nl + ns,))
    points.append(geometry.Point(center_long+es,center_lat+nl))
    points.append(geometry.Point(center_long+es+el,center_lat+nl-ns,))
    points.append(geometry.Point(center_long-el,center_lat+ns))
    points.append(geometry.Point(center_long,center_lat))
    points.append(geometry.Point(center_long+el,center_lat-ns))
    points.append(geometry.Point(center_long-el-es,center_lat-nl+ns))
    points.append(geometry.Point(center_long-es,center_lat-nl))
    points.append(geometry.Point(center_long-es+el,center_lat-nl-ns))
    
    poly = geometry.Polygon([[p.x, p.y] for p in points])
    x,y = poly.exterior.xy
    #pyplot.plot(x,y)
    #print (poly)
    
    latandlon = []
    for y in zones:
        latandlon.append(geometry.Point(y))
        
    poly2 = geometry.Polygon([[p.x, p.y] for p in points])
    x,y = poly2.exterior.xy
    pyplot.scatter(x,y)
    
    
        
    
            

#%%


    
coordinates = [[
              7.513275146484376,
              44.96917023288551
            ],
            [
              7.77557373046875,
              44.96917023288551
            ],
            [
              7.77557373046875,
              45.15008475740563
            ],
            [
              7.513275146484376,
              45.15008475740563
            ]]
            
R = 6373.0
lon1 = radians(coordinates[0][0])
lon2 = radians(coordinates[1][0])
lat1 = radians(coordinates[0][1])
lat2 = radians(coordinates[1][1])

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

hor_distance = R * c

lon1 = radians(coordinates[0][0])
lon2 = radians(coordinates[3][0])
lat1 = radians(coordinates[0][1])
lat2 = radians(coordinates[3][1])

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))
ver_distance = R * c


number_hor = hor_distance/0.5
number_ver = ver_distance/0.5
size = int(np.floor(min(number_hor,number_ver)))
dist_inlat = (coordinates[3][1]-coordinates[0][1])/number_ver
dist_inlong = (coordinates[1][0]-coordinates[0][0])/number_hor  

zones_of_500 = []
square = []
square.append(coordinates[0])
square.append([square[0][0]+dist_inlong,square[0][1]])
square.append([square[1][0],square[1][1]+dist_inlat])
square.append([square[0][0],square[0][1]+dist_inlat])
square.append(square[0])
zones_of_500.append(square)

for i in range(0,size):
    if (i!=0):
        row_up = zones_of_500[size*(i-1)]
        square = []
        square.append([row_up[0][0],row_up[0][1]+dist_inlat])
        square.append([row_up[1][0],row_up[1][1]+dist_inlat])
        square.append(row_up[1])
        square.append(row_up[0])
        square.append(square[0])
        zones_of_500.append(square)
    for j in range(1,size):
        square = []
        square.append(zones_of_500[40*i+j-1][1])
        square.append([square[0][0]+dist_inlong,square[0][1]])
        square.append([square[1][0],square[1][1]+dist_inlat])
        square.append([square[0][0],square[0][1]+dist_inlat])
        square.append(square[0])
        zones_of_500.append(square)

zones = "["    
for i in range(int(len(zones_of_500))):
    zones += "["
    zones += str(zones_of_500[i])
    zones += "]"

    if i<len(zones_of_500)-1:
        zones += ","
zones += "]"

file.write(zones)    


for i in range(len(zones_of_500)):
    stringa += '{\"type\": \"Feature\",\"properties\": {},\"geometry\": {\"type\": \"Polygon\",\"coordinates\":[';
    stringa += str(zones_of_500[i])
    stringa += ']}}'
    if i<len(zones_of_500)-1: stringa+=','
    
stringa += ']}'
#
#polys = []
#for x in zones_of_500:
#    poly = Polygon( ((x[0], x[0]), (x[0], x[1]), (x[1], x[1]), (x[0], x[0])) )
#    polys.append(poly)    

        
geojson = open('geojson.txt','w+')
geojson.write(stringa)

print (zones)

centroids = []
centroid = open('centroid.csv','w+')
centroid.write('number,long,lat\n')
for i in range(len(zones_of_500)):
    lat = (zones_of_500[i][1][1]-dist_inlong/2)
    lat = lat + dist_inlat/2;
    long = (zones_of_500[i][1][0]-dist_inlong/2)
    stringa = (str(i)+','+str(long)+','+str(lat)+'\n')
    centroids.append((long,lat))
    print (stringa)
    centroid.write(stringa)

    