# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:40:17 2019

@author: fede9
"""
import math

#input coordinate stringhe
#output coordinate intere 
def parserLocation(lat, long):
   assert(len(lat) == 13) #se non è un valore corretto di latitudine
   strlat = lat[0] + lat[2] + lat[3:5] + lat[6:9] + lat[10:13]
   
   assert(len(long) == 14) #se non è un valore corretto di latitudine
   strlong = long[0:2] + long[3] + long[4:6] + long[7:10] + long[11:14]
   #print(str)
   return [int(strlat)/100000000, int(strlong)/100000000]
#end parserLocation
   
def distanceLocation(lat1, long1, lat2, long2) :
   #conversione in radianti
   lat1 = lat1*(2*math.pi)/360
   long1 = long1*(2*math.pi)/360
   lat2 = lat2*(2*math.pi)/360
   long2 = long2*(2*math.pi)/360
   
   dist = math.acos( math.sin(lat1) * math.sin(lat2) 
      + math.cos(lat1) * math.cos(lat2) * math.cos(long1-long2)) * 6371
   
   return dist