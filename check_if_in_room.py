# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:43:12 2018

@author: Matteo
"""


import pandas
from shapely.geometry.polygon import LinearRing, Polygon
from shapely import geometry
from math import sin, cos, sqrt, atan2, radians,asin

#harvesine
def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
  R = 6373 # Radius of the earth in km
  dLat = (lat2-lat1)  # deg2rad below
  dLon = (lon2-lon1)
  a = sin(dLat/2) * sin(dLat/2) + cos(lat1) * cos(lat2) * sin(dLon/2) * sin(dLon/2) 
  #c = 2 * atan2(sqrt(a), sqrt(1-a)) 
  c = 2*asin(sqrt(a))
  d = R * c; # Distance in km
  return d;



file = pandas.read_csv('C:\\Users\\Matteo\\Desktop\\Utility WEMAP\\allrooms_id_wkt.csv',sep=',') 
measurements = pandas.read_csv('C:\\Users\\Matteo\\Desktop\\Utility WEMAP\\measurements_to_check.csv',sep=',')
p = geometry.Point (7.65853890365347123,45.06520600188714809)

polygons = {}
for x in range(0,len(file)-1):
        str_polygon = file['wkt_geom'][x][9:-1]
        list_polygon = str_polygon.split(',')
        tuple_polygon = []
        for y in list_polygon:
            temp = y.split(' ')
            if temp[0] == '':
                if temp[1][0] == '(':
                    tuple_polygon.append((float(temp[0][1:]),float(temp[1])))
                elif temp[2][-1] == ')':
                    tuple_polygon.append((float(temp[1]),float(temp[2][:-2])))
                else:
                    tuple_polygon.append((float(temp[1]),float(temp[2])))
                

            else:
                if temp[0][0] == '(':
                    tuple_polygon.append((float(temp[0][1:]),float(temp[1])))
                elif temp[1][-1] == ')':
                    tuple_polygon.append((float(temp[0]),float(temp[1][:-2])))
                else:
                    tuple_polygon.append((float(temp[0]),float(temp[1])))
        polygons[file['_id'][x]] = geometry.Polygon(tuple_polygon)

         
for x in range(len(measurements)):
    if measurements['allrooms_id'][x] != 696:
        point = geometry.Point(measurements['longitude'][x],measurements['latitude'][x])
        #controlla che i meas non siano in 696 e poi controlla la accuratezza della misurazione
        
        if polygons[measurements['allrooms_id'][x]].contains(point):
            print (True,measurements['id'][x])
        else:
    #        R = 6373.0
            lon1 = radians(measurements['longitude'][x])
            lon2 = radians(polygons[measurements['allrooms_id'][x]].representative_point().bounds[0])
            lat1 = radians(measurements['latitude'][x])
            lat2 = radians(polygons[measurements['allrooms_id'][x]].representative_point().bounds[1])
    #        
    #        dlon = lon2 - lon1
    #        dlat = lat2 - lat1
    #        
    #        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    #        c = 2 * atan2(sqrt(a), sqrt(1 - a))        
    #        distance = R * c 
    #        print (distance)
            if (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) < 20 and measurements['gps_accuracy'][x]<25:
                print (True,measurements['id'][x])
    
            #print(polygons[measurements['allrooms_id'][x]].distance(point))
            elif (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) > 20 and measurements['gps_accuracy'][x]<25:
                print (False,measurements['id'][x])
                contained = False
                for y in polygons:
                    if polygons[y].contains(point):
                        contained = True
                        print ('It\'s in',y)
                        break
                if (contained == False):
                    print ('Point taken outside')
                
            elif (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) > 20 and measurements['gps_accuracy'][x]>25:
                print (True,measurements['id'][x])
    else:
        print ('General Point',measurements['id'][x])

            

            
            

