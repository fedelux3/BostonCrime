# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:53:20 2019

@author: fede9
"""

import csv
import datetime
#input coordinate stringhe
#output coordinate intere 
def parserLocation(lat, long):
   assert(len(lat) == 13) #se non è un valore corretto di latitudine
   strlat = lat[0] + lat[2:5] + lat[6:9] + lat[10:13]
   
   assert(len(long) == 14) #se non è un valore corretto di latitudine
   strlong = long[1] + long[3:6] + long[7:10] + long[11:14]
   #print(str)
   return [int(strlat), int(strlong)]

#input data e ora stringa
#output giorni (intero)
def distanceTime(timeE, timeP) :
   assert(len(timeE) == 16)
   assert(len(timeP) == 16)
   
   daysE = int(timeE[0:2])
   monthsE = int(timeE[3:5])
   yearsE = int(timeE[6:10])
   
   daysP = int(timeP[0:2])
   monthsP = int(timeP[3:5])
   yearsP = int(timeP[6:10])
   
   dE = datetime.date(yearsE, monthsE, daysE)
   dP = datetime.date(yearsP, monthsP, daysP)
   
   return abs(dE - dP).days

#input due coordinate intere
#output max distanza tra le due coppie
def distanceLocation(lat1, long1, lat2, long2) :
   dlat = abs(lat1 - lat2)
   dlong = abs(long1 - long2)
   return max(dlat, dlong)

def neighborhood(event) :
   #raggio spaziale della location
   #coordinate hanno 10 cifre
   r = 1000000
   #raggio temporale di 7 giorni
   t = 3.5
   #neighbothood with respect to event type
   nfe = []
   
   with open("dataset.csv", newline="", encoding="ISO-8859-1") as filecsv:
      
      lettore = csv.reader(filecsv,  dialect = 'excel', delimiter= ";")
      
      #lettore = next(lettore)
      #print(header)
      
      recordData = [(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7]) for col in lettore]
      
      for crime in recordData[1:]:
         #print(event)
         #print(crime[5])
         [late, longe] = parserLocation(event[5], event[6])
         [latp, longp] = parserLocation(crime[5], crime[6])
         timee = event[3]
         timep = crime[3]
         #print(timee)
         #print(timep)
         
         #se è entro il raggio spaziale
         if distanceLocation(late, longe, latp, longp) <= r:
            timee = event[3]
            timep = crime[3]
            diffDays = distanceTime(timee, timep)
            #se è entro il raggio temporale
            #escludo se stesso
            if diffDays <= t and event != crime:
               nfe.append(crime)

   return nfe

#MAIN

nei = []
with open("test2.csv", newline= "", encoding="ISO-8859-1") as fileread:

   lettore = csv.reader(fileread, dialect = 'excel', delimiter= ',')
   
   recordTest = [(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7]) for col in lettore]
   
   
   for record in recordTest:
      nei.append(neighborhood(record))


