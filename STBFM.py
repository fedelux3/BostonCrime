# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:55:14 2019

@author: fede9
"""

import datetime
import math
import mysql.connector
from SPTree2 import SPTree

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
   
   sql = "SELECT * FROM " + table
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
   #print(typeD)
   sql = "SELECT * FROM " + table + " WHERE offence_code_group LIKE \"" + typeD + "\""   
   #print(sql)
   mycursor.execute(sql)
   
   for record in mycursor:
      setReturn.add(record[0])
   return setReturn
#end setD

#input insiemeSet precedente e tipo corrente
#output insieme di istanze associate
def setInstances(prevSet, currentType):
   set_return = set()
   #insieme del elemento di sequenza precedente
   #set_prev = setD(seqTypes[0])

   for event in prevSet:
      sql = "SELECT * FROM " + table + " WHERE incident_num = \"" + event + "\""
      mycursor.execute(sql)
      #la tupla che mi interessa
      ev = mycursor.fetchone()
      #print(ev)
      neig = neighborhood(ev, currentType)
      #print(neig)
      set_return = set_return.union(neig)
   return set_return
#end setInstance
   
#QUA FORSE SERVE ALTRO
   
#candidate generation
#input un insieme di sequenze significative
#assumo che l'input sia di una lista di sequenze (che a loro volta sono liste)
#output albero con set di candidati 
def candidateGen(setSeq, tree) :
   
   for seq in setSeq :
      #se la sequenza precedente esiste
      node = tree.searchNode(seq[:len(seq)-1])
      if node != 0 :
         #calcolo nuovo setInstances tra node e tipo di seq[len(seq)-1]
         newSet = setInstances(node.set, seq[len(seq)-1])
         print(str(seq) + " inserita")
         #creo un set che è l'union tra set di node e neighborhood trovato
         tree.insertNode(seq, newSet) #gli aggiungo l'insieme del nodo
      else:
         print("error candidate Gen - node non trovato")
   #print(tree)
#end caditateGen

#calcola il valore di Partitipation rateo di questo nodo
def computePR(n1, tree):
   typeD = n1.value
   nSet = tree.searchNode([typeD])
   if (nSet is None):
      print("tipo non trovato")
      return
   
   #print("esito searchPR: " + str(nSet))
   ins = len(n1.set)
   d_set = len(nSet.set)
   #print(ins)
   #print(d_set)
   pr = ins / d_set
   return pr
#end computePR
   
##############################################################
   #TEST

def testTree() :
   t = SPTree(["A", "B", "C"])
   #inserisco i sets
   sA = set()
   sA.add("10")
   sB = set()
   sB.add('IT01R003')
   sC = set()
   sC.add('30')
   
   nA = t.searchNode(["A"])
   nB = t.searchNode(["B"])
   nC = t.searchNode(["C"])  
   
   nA.insertSet(sA)
   nB.insertSet(sB)
   nC.insertSet(sC)
   print(nA)
   print(nB)
   print(nC)
#end testTree

def testCrimeTree() :
   
   seq2 = [["Aggravated Assault", "Auto Theft"], ["Commercial Burglary", "Homicide"], 
           ["Other Burglary", "Robbery"], ["Homicide", "Auto Theft"], 
           ["Larceny", "Residential Burglary"], ["Aggravated Assault", "Robbery"],
           ["Larceny From Motor Vehicle", "Homicide"],["Commercial Burglary", "Auto Theft"],
           ["Robbery", "Larceny"], ["Larceny From Motor Vehicle", "Commercial Burglary"],
           ["Auto Theft", "Residential Burglary"], ["Auto Theft", "Aggravated Assault"]]
   
   seq3 = [["Commercial Burglary", "Homicide", "Auto Theft"], 
           ["Larceny From Motor Vehicle", "Homicide", "Auto Theft"],
           ["Aggravated Assault", "Auto Theft", "Residential Burglary"],
           ["Aggravated Assault", "Robbery", "Larceny"], 
           ["Larceny From Motor Vehicle", "Commercial Burglary", "Auto Theft"]]
   
   sql = "SELECT DISTINCT offence_code_group FROM " + table
   mycursor.execute(sql)
   
   types = []
   setTypes = []
   #inizializzo i tipi di eventi e i setD a loro legati
   for tipo in mycursor:
      types.append(tipo[0])
   
   for el in types:
      s = setD(el)
      setTypes.append(s)

   tree = SPTree()
#   i = 0
#   for tipo in tree.root.children:
#      tipo.insertSet(setTypes[i])
#      i += 1
   i = 0
   for el in types:
      tree.insertNode(el, setTypes[i])
      i += 1
      
#   for elem in types:
#         n = Node(self.root,self.root,elem,None,None)
#         #print(elem)
#         self.root.insertChild(n)
      
   #print(tree)
   
   candidateGen(seq2, tree)
   candidateGen(seq3, tree)
   
   print(tree)
   
   for tipo in tree.root.children:
      print(tipo.value + ": " + str(len(tipo.set)))
#end testCrimeTree
      
def testPR() :
   seq2 = [["Aggravated Assault", "Auto Theft"], ["Commercial Burglary", "Homicide"], 
           ["Other Burglary", "Robbery"], ["Homicide", "Auto Theft"], 
           ["Larceny", "Residential Burglary"], ["Aggravated Assault", "Robbery"],
           ["Larceny From Motor Vehicle", "Homicide"],["Commercial Burglary", "Auto Theft"],
           ["Robbery", "Larceny"], ["Larceny From Motor Vehicle", "Commercial Burglary"],
           ["Auto Theft", "Residential Burglary"], ["Auto Theft", "Aggravated Assault"]]
   
   sql = "SELECT DISTINCT offence_code_group FROM " + table
   mycursor.execute(sql)
   
   types = []
   setTypes = []
   #inizializzo i tipi di eventi e i setD a loro legati
   for tipo in mycursor:
      types.append(tipo[0])
   
   for el in types:
      s = setD(el)
      setTypes.append(s)

   tree = SPTree()
   i = 0
   for el in types:
      tree.insertNode(el, setTypes[i])
      i += 1
   
   candidateGen(seq2, tree) #inserisco sequenze di 2 elementi
   
   for seq in seq2:
      n = tree.searchNode(seq)
      pr1 = computePR(n, tree)
      print("seq: " + str(seq) + " - pr: " + str(pr1))
   
#end testPR
#############################
   #MAIN
if __name__ == "__main__":
   mydb = mysql.connector.connect(
         host = "localhost",
         user = "root",
         passwd = "fedeServer33",
         database = "bostoncrime"
         )
   table = "crimedata2018small"
   mycursor = mydb.cursor()
   
#   print("Testing testTree :")
#   testTree()
   
#   print("Testing testCrimeTree :")
#   testCrimeTree()
   
   print("Testing testPR :")
   testPR()
   mycursor.close()