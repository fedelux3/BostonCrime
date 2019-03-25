# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:53:20 2019

@author: fede9
"""

import csv
import datetime
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
   
   assert(dist >= 0)
   return round(dist, 2)
#end distanceLocation
   
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
#end distanceTime
   
#input event
#output neigborhood event
def neighborhood(event, typeF) :
   #raggio spaziale della location (km)
   r = 2.5
   #raggio temporale di 7 giorni
   t = 2
   #neighbothood with respect to event type
   nfe = []
   
   with open("test2018.csv", newline="", encoding="ISO-8859-1") as filecsv:
      
      readData = csv.reader(filecsv,  dialect = 'excel', delimiter= ";")
   
      #lettore = next(lettore)
      #print(header)
      
      recordData = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in readData]
      
      for crime in recordData[1:]:
         #print(event)
         #print(crime[5])
         [late, longe] = parserLocation(event[4], event[5])
         [latp, longp] = parserLocation(crime[4], crime[5])
         #timee = event[2]
         #timep = crime[2]
         #print(timee)
         #print(timep)
         
         #se di tipo specificato
         if crime[1] == typeF:
            #se è entro il raggio spaziale
            if distanceLocation(late, longe, latp, longp) <= r:
               timee = event[2]
               timep = crime[2]
               diffDays = distanceTime(timee, timep)
               #se è entro il raggio temporale
               #escludo se stesso
               if diffDays <= t and event != crime:
                  nfe.append(crime)
      #end for
      
   return nfe
#end neighborhood
   
#input sequenza di m tipi di eventi
#output insieme di istanze associate
def setInstances(seqTypes):
   set_init = set()
   
   with open("test2018.csv", newline="", encoding="ISO-8859-1") as fileread:
      
      reader = csv.reader(fileread, dialect = 'excel', delimiter= ';')
   
      recordRead = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in reader]
   
      firstType = seqTypes[0]
      
      for record in recordRead[1:]:
         if record[1] == firstType:
            set_init.add(record[0])
      
      #insieme del elemento di sequenza precedente
      set_prev = set_init
      for i in range(1,len(seqTypes)):
         current = seqTypes[i]
         set_return = set()
         for event in set_prev:
            
            ev = None
            #ricerco la tupla che mi interessa
            for tupla in recordRead[1:]:
               if record[0] == event:
                  ev = tupla
                  exit
            #################################
            #QUA DEVI CAPIRE COME CONCATENARE I NEIGHBORHOOD 
            #e nel caso fare l'unione dei neighborhood validi
            #ne = neighborhood(ev, current)
            #################################
   #end with      
   
   return set_return
#end setInstance

#MAIN

seq = ["Aggravated Assault"]

ins = setInstances(seq)
print(len(ins))

#TEST Neighboorhood
#nei = []
#with open("test2018.csv", newline= "", encoding="ISO-8859-1") as fileread:
#
#   lettore = csv.reader(fileread, dialect = 'excel', delimiter= ';')
#   
#   recordTest = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in lettore]
#   
#   
#   for record in recordTest[1:]:
#      nei.append(neighborhood(record))

#TEST UCR=Part One
#types = ["Aggravated Assault", "Auto Theft", "Larceny", "Robbery", "Residential Burglary",
#         "Larceny From Motor Vehicle", "Homicide", "Commercial Burglary", "Other Burglary"]
#ev = []
#with open("test2018.csv", newline="", encoding="ISO-8859-1") as fileread:
#   
#   reader = csv.reader(fileread, dialect = 'excel', delimiter= ';')
#   
#   recordRead = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in reader]
#   
#   for record in recordRead[1:]:
#      if record[1] == types[0]:
#         ev.append(record)  

   
   
   
   
   
   
   