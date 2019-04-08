# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:53:20 2019

@author: fede9
"""

import datetime
import math
import mysql.connector

#input coordinate stringhe
#output coordinate intere 
def parserLocation(lat, long):
   assert(len(lat) == 13) #se non è un valore corretto di latitudine
   strlat = lat[0] + lat[2] + lat[3:5] + lat[6:9] + lat[10:13]
   
   long = long.strip() #elimino tabulazioni
   assert(len(long) == 14) #se non è un valore corretto di lognitudine
   strlong = long[0:2] + long[3] + long[4:6] + long[7:10] + long[11:14]
   #print(str)
   return [int(strlat)/100000000, int(strlong)/100000000]
#end parserLocation
   
def distanceLocation(lat1, long1, lat2, long2) :
   #conversione in radianti
   lat1 = round(lat1*(2*math.pi)/360, 2)
   long1 = round(long1*(2*math.pi)/360, 2)
   lat2 = round(lat2*(2*math.pi)/360, 2)
   long2 = round(long2*(2*math.pi)/360, 2)
   
   
   dist = math.acos( math.sin(lat1) * math.sin(lat2) 
      + math.cos(lat1) * math.cos(lat2) * math.cos(long1-long2)) * 6371
   
   assert(dist >= 0)
   return dist
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
   
   return abs((dE - dP).days)
#end distanceTime
   
#input event, type evet
#output neigborhood event
def neighborhood(event, typeF) :
   #raggio spaziale della location (km)
   r = 0.1
   #raggio temporale di 7 giorni
   t = 3
   #neighbothood with respect to event type
   nfe = set()
   
   sql = "SELECT * FROM crimedata2018small"
   
   mycursor.execute(sql)
   
   for crime in mycursor:
      #print(event)
      #print(crime[5])
      
      [late, longe] = parserLocation(event[4], event[5])
      [latp, longp] = parserLocation(crime[4], crime[5])
     
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
               nfe.add(crime[0])
   #end for
      
   return nfe
#end neighborhood

#input tipo di evento
#output insieme ti tutti gli eventi di quel tipo
def setD(typeD) :
   setReturn = set()
   
   sql = "SELECT * FROM crimedata2018small WHERE offence_code_group = \"" + typeD + "\""   
   
   mycursor.execute(sql)
   
   for record in mycursor:
      setReturn.add(record[0])
   return setReturn
#end setD
   
#input sequenza di m tipi di eventi
#output insieme di istanze associate
def setInstances(seqTypes):
   
   set_return = set()
   
   #insieme del elemento di sequenza precedente
   set_prev = setD(seqTypes[0])
   
   if len(seqTypes) < 2:
      return set_prev
   
   set_return = set()
   
   for i in range(1,len(seqTypes)):
      currentType = seqTypes[i]
      
      for event in set_prev:
        
         sql = "SELECT * FROM crimedata2018small WHERE incident_num = \"" + event + "\""
         
         mycursor.execute(sql)
         #la tupla che mi interessa
         ev = mycursor.fetchone()
         #print(ev)
         neig = neighborhood(ev, currentType)
         #print(neig)
         set_return = set_return.union(neig)
         
   
   return set_return
#end setInstance

#input sequenza di 2 tipi
#output valore di partitipation rateo della sequenza
def computePR(seqTypes):
   assert(len(seqTypes) == 2) #lunghezza sequenza deve essere di 2
   ins = setInstances(seqTypes)
   n_el = len(seqTypes)
   #print("Ins " + seqTypes[n_el-2] + ": "+ str(len(ins)))
   d_ins = setD(seqTypes[n_el-1])
   #print("D " + seqTypes[n_el-1] + ": " + str(len(d_ins)))
   pr = len(ins)/len(d_ins)
   
   return pr
#end computePR

#input sequenza di tipi
#output valore del participation index
def computePI(seqTypes):
   m = len(seqTypes)
   if m <= 2:
      return computePR(seqTypes)
   else:
      pr = computePR([seqTypes[m-2], seqTypes[m-1]])
      pi = computePI(seqTypes[:m-1])
      print(pr)
      print(pi)
      return min(pi, pr)
#end computePI
      
#MAIN

#TEST mySQL
mydb = mysql.connector.connect(
      host = "localhost",
      user = "root",
      passwd = "fedeServer33",
      database = "bostoncrime"
      )

mycursor = mydb.cursor()


#TEST computePI
seq = ["Commercial Burglary", "Robbery", "Auto Theft"]
pi = computePI(seq)
print("valore pi finale: " + str(pi))

#TEST computePR
#seq = ["Commercial Burglary", "Auto Theft"]
#pr = computePR(seq)
#print(pr)
#TEST setInstances
#seq = ["Commercial Burglary", "Auto Theft"]
#ins = setInstances(seq)
#print(ins)
#for i in ins:
#   sql = "SELECT * FROM crimedata2018 WHERE incident_num = \"" + i + "\""
#   mycursor.execute(sql)
#   row = mycursor.fetchone()
#   print(row)

#TEST setD
#typeE = "Aggravated Assault"
#s = setD(typeE)
#print(s)

#TEST neighborhood
#sql = "SELECT * FROM crimedata2018 WHERE incident_num = \"I182002757\""
#mycursor.execute(sql)
#
#for x in mycursor:
#   ev = x
#
#n = neighborhood(ev, "Aggravated Assault")
#print(n)
mycursor.close()

#TEST PR
#seq = ["Homicide", "Residential Burglary"]
#pr = computePR(seq)
#print(pr)

#TEST set instance
#seq = ["Larceny", "Homicide"]
#
#ins = setInstances(seq)
#
#evento = []
#with open("test2018.csv", newline="", encoding="ISO-8859-1") as fileread:
#      
#   reader = csv.reader(fileread, dialect = 'excel', delimiter= ';')
#   recordRead = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in reader]
#   
#   for tupla in recordRead[1:]:
#      for ev in ins:
#         if tupla[0] == ev:
#            evento.append(tupla)
#
#print(evento)
#print(len(ins))

#TEST Neighboorhood
#n = None
#with open("test2018.csv", newline= "", encoding="ISO-8859-1") as fileread:
#
#   lettore = csv.reader(fileread, dialect = 'excel', delimiter= ';')
#   
#   recordTest = [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in lettore]
#   
#   
#   for record in recordTest[1:]:
#      if record[0] == 'I182011110':
#         n = neighborhood(record, "Larceny")
#   
#   print(len(n))

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

   
   
   
   
   
   
   