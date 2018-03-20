# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 18:43:38 2018

@author: Matteo
"""
import pandas
file = pandas.read_csv('all_meas_peruserandroom.csv',sep=',')

rooms = file['allrooms_id'].drop_duplicates()

for r in rooms:
    temp = file.loc[(file['allrooms_id']==r)]
    temp = temp[['allrooms_id','speedInternet']]
    print (r,temp['speedInternet'].median())