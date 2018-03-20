# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:43:12 2018

@author: Matteo
"""

import pandas
import time
#from shapely.geometry.polygon import LinearRing, Polygon
from shapely import geometry
from math import sin, cos, sqrt,radians,asin
import numpy as np

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



#file = pandas.read_csv('C:\\Users\\Matteo\\Desktop\\Utility WEMAP\\allrooms_id_wkt.csv',sep=',') 
file = pandas.read_csv('http://wemapserver.sytes.net/Utility%20WEMAP/allrooms_id_wkt.csv',sep=',') 

#measurements = pandas.read_csv('C:\\Users\\Matteo\\Desktop\\Utility WEMAP\\allresults_qrandgrid.csv',sep=',')
measurements = pandas.read_csv('http://wemapserver.sytes.net/Utility%20WEMAP/allresults_qrandgrid.csv',sep=',')
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
        
            if (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) < 20 and measurements['gps_accuracy'][x]<25:                
                print (True,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
    
            #print(polygons[measurements['allrooms_id'][x]].distance(point))
            elif (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) > 20 and measurements['gps_accuracy'][x]<25:
                trust_GNSS = True
                #print (False,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                if measurements['gps_accuracy'][x] <= 8.0:
                    trust_GNSS = False
                    #since i get different position from the stated, checking if I can trust the GPS
                    sat_in_view = {}
                    
                    if measurements['satellite_in_view'][x] > 3:
                        splitted = measurements['pseudorange'][x].split('\n')
                        splitted.pop()                        
                        for string in splitted:
                            string_splitted = string.split(' ')
                            string_splitted = string_splitted[0].split(':')
                            string_splitted = string_splitted[1][0:3]
                            if string_splitted in sat_in_view:
                                sat_in_view[string_splitted] = sat_in_view[string_splitted] + 1
                            else:
                                sat_in_view[string_splitted] = 1
                        for sat in sat_in_view:
                            if sat_in_view[sat] >= 4: #if I have more than 4 satellites for a constellation I trust the GNSS
                                trust_GNSS = True
                                contained = False
                                for y in polygons:
                                    if polygons[y].contains(point):
                                        contained = True
                                        print ('It\'s in',y)
                                        #measurements.set_value(x,'allrooms_id',y)
                                        measurements.loc[x,('allrooms_id')] = y
                                        break
                                if (contained == False):
                                    print ('Point taken outside')
                                    #measurements.set_value(x,'allrooms_id',696)            
                                    measurements.loc[x,('allrooms_id')] = 696
                                    break;
                    if (trust_GNSS == False):
                        print (True,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                    if (trust_GNSS == True):
                        print (False,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                        measurements = measurements.drop(index = x, axis = 0)


                     
                else:
                    contained = False
                    for y in polygons:
                        if polygons[y].contains(point):
                            contained = True
                            print ('It\'s in',y)
                            #measurements.set_value(x,'allrooms_id',y)
                            measurements.loc[x,('allrooms_id')] = y
                            break
                        if (contained == False):
                            print ('Point taken outside')
                            #measurements.set_value(x,'allrooms_id',696)            
                            measurements.loc[x,('allrooms_id')] = 696
                            break
                 
                    
            elif (getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000) > 20 and measurements['gps_accuracy'][x]>25:
                print (True,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
    else:
        
        if (np.isnan(measurements['qr_id'][x])):        
            print ('General Point',measurements['id'][x])
        else:
            lat1 = radians(measurements['latitude'][x])
            lon1 = radians(measurements['longitude'][x])
            lat_qr = radians(measurements.loc[x,('lat_stated')])
            lon_qr = radians(measurements.loc[x,('lon_stated')])
            if (getDistanceFromLatLonInKm(lat1,lon1,lat_qr,lon_qr)*1000> 25 and measurements.loc[x,('gps_accuracy')] <= 25):
                trust_GNSS = True
                #print (False,measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                if measurements['gps_accuracy'][x] <= 8.0:
                    trust_GNSS = False
                    #since i get different position from the stated, checking if I can trust the GPS
                    sat_in_view = {}                    
                    if measurements['satellite_in_view'][x] > 3:
                        splitted = measurements['pseudorange'][x].split('\n')
                        splitted.pop()                        
                        for string in splitted:
                            string_splitted = string.split(' ')
                            string_splitted = string_splitted[0].split(':')
                            string_splitted = string_splitted[1][0:3]
                            if string_splitted in sat_in_view:
                                sat_in_view[string_splitted] = sat_in_view[string_splitted] + 1
                            else:
                                sat_in_view[string_splitted] = 1
                        for sat in sat_in_view:
                            if sat_in_view[sat] >= 4: #if I have more than 4 satellites for a constellation I trust the GNSS
                                trust_GNSS = True
                                measurements.loc[x,('qr_id')] = np.nan
                                measurements.loc[x,('lat_stated')] = measurements['latitude'][x]
                                measurements.loc[x,('lon_stated')] = measurements['longitude'][x]
                                break
                    if (trust_GNSS == False):
                        print (True,'QR',measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                    if (trust_GNSS == True):
                        print (False,'QR',measurements['id'][x],measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]),getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)*1000)
                        measurements = measurements.drop(index = x, axis = 0)

            elif (getDistanceFromLatLonInKm(lat1,lon1,lat_qr,lon_qr)*1000> 25 and measurements.loc[x,('gps_accuracy')] > 25):
                print (True,'QR','For Low Accuracy',str(measurements['qr_id'][x]),str(getDistanceFromLatLonInKm(lat1,lon1,lat_qr,lon_qr)*1000),measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]))
            else:
                print (True,'QR',measurements['id'][x],str(measurements['qr_id'][x]),str(getDistanceFromLatLonInKm(lat1,lon1,lat_qr,lon_qr)*1000),measurements['phone_mac'][x],str(measurements['gps_accuracy'][x]))

            


                
            

#measurements.to_csv('filtered'+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+'_'+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)+'.csv')
            
#%%
rooms = pandas.read_csv('http://wemapserver.sytes.net/Utility%20WEMAP/all_rooms.csv',sep=',') 
centers = rooms.loc[rooms['grid'] == 5]

for r in centers['id']:
    temp = measurements.loc[(measurements['allrooms_id']==r)]
    temp = temp[['allrooms_id','speedInternet']]
    print (r,',',centers.loc[(centers['id']==r),('room')].any(),',',temp['speedInternet'].median())
    
#%%
names = ['id','room','grid','speed','accuracy','rssi','lat','lon','lat_user','lon_user']
median_per_grid = pandas.DataFrame(columns = names)


for r in range(len(rooms)):
    temp = measurements.loc[(measurements['allrooms_id']==rooms['id'][r])]
    #print(temp['grid_cell'])
    temp = temp.loc[(temp['grid_cell'] == (rooms['grid'][r]+1))]
    #temp = temp[['allrooms_id','grid_cell','speedInternet']]
    
    if (len(temp) == 1):
        median = temp['speedInternet'].values[0]
        rssi = temp['RSSI'].values[0]
        accuracy = temp['gps_accuracy'].values[0]
        lat_user = temp['latitude'].values[0]
        lon_user = temp['longitude'].values[0]
    elif (len(temp) > 1):
        median = temp['speedInternet'].median()
        rssi = temp['RSSI'].median()
        accuracy = temp['gps_accuracy'].median()
        lat_user = temp['latitude'].median()
        lon_user = temp['longitude'].median()
    else:
        median = 0
        rssi = 0
        accuracy = 0
        lat_user = 0
        lon_user = 0
    
    for n in names:
        median_per_grid.loc[r,names] = rooms['id'][r],rooms['room'][r],rooms['grid'][r],median,accuracy,rssi,rooms['lat'][r],rooms['long'][r]

median_per_grid = median_per_grid.fillna(0)      
median_per_grid.to_csv('median_per_grid2.csv',sep=',')
    


            
            

