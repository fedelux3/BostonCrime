# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:55:14 2019

@author: fede9
"""

import time
import datetime
import math
import mysql.connector
from SPTree3 import SPTree

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
   #raggio temporale
   t = 2
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
   
#candidate generation
#input un insieme di sequenze significative di lunghezza uguale
#assumo che l'input sia di una lista di sequenze (che a loro volta sono liste)
#output albero con set di candidati 
def candidateGen(setSeq, tree) :
   ret = []
   
   for seq in setSeq :
      #se la sequenza precedente esiste
      node = tree.searchNode(seq[:len(seq)-1])
      if node != 0 :
         #calcolo nuovo setInstances tra node e tipo di seq[len(seq)-1]
         newSet = setInstances(node.set, seq[len(seq)-1])
         #creo un set che è l'union tra set di node e neighborhood trovato
         tree.insertNode(seq, newSet) #gli aggiungo l'insieme del nodo
         ret.append(seq)
         print("inserito: " + str(seq))
      else:
         print("error candidate Gen - node non trovato")
   
   return ret
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
   
def computePI(seq, tree):
   length = len(seq)
   n = tree.searchNode(seq)
   #se il nodo non esiste allora lo segnalo in output
   if n is None:
      return None
   if length <= 2: #caso base
      return computePR(n, tree)
   else:
      pr = computePR(n,tree)
      pi = computePI(seq[:length-1], tree)
      return min(pi, pr)
#end computePI

#verifica se all'interno di una sequenza (list) vi siano elementi doppi
#output true se non sono presenti due tipi uguali
#output false se sono presenti due tipi uguali
def checkDouble(seq):
   seqSet = set(seq)
   if len(seq) == len(seqSet):
      return True
   else:
      return False
#end checkDouble

def candidateGenTree(candidates, tree):
   ret = []
   
   for cand in candidates:
      nodeCand = tree.searchNode(cand)
      if nodeCand is None:
         #print("cand not found, seq: " + str(cand))
         continue
      #questo passaggio serve per generare in automatico le prox seq
      children = nodeCand.parent2.children
      #print(nodeCand)
      for child in children:
         newSeq = cand[:]
         newSeq.append(child.value)
#         print(newSeq)
         if checkDouble(newSeq):
#            print("cand: " + str(cand))
#            print("newSeq: " + str(newSeq))
#            print("cand: " + str(cand) + ", newSeq: " + str(newSeq) + " ...")
            newSet = setInstances(nodeCand.set, child.value)
            tree.insertNode(newSeq, newSet)
            ret.append(newSeq)
            print("inserito: " + str(newSeq))
   return ret
#end candidateGenTree

#input lista di [sequenza, pi]
#output coppia [sequenza, pi] con pi minore
def seqPIMin(seqList, num):
   teta = 1
   i = 0
   #verifico che vi siano n-1 elementi nella lista che superino il nuovo teta
   while i < num:
      #aggiorno il newteta se è il massimo dei minori di teta
      newteta = 0
      for el in seqList:
         if el[1] < teta and el[1] > newteta:
            newteta = el[1]
            #print(newteta)
      teta = newteta
      i = 0
      #verifico che vi siano n-1 elementi nella lista che superino il nuovo teta
      for el in seqList:
         if el[1] >= teta:
            i += 1
   return teta
#end seqPIMin

#verifyTopCandidates, si occupa del calcolo del pi di ciascun candidato
#estraendo solo i primi n elementi in base al valore di pi
#output lista di coppie [sequenza - pi] (n elementi)
def verifyTopCandidates(candidates, teta, top, num, tree):
   ret = []
   
   for seq in candidates:
      
      pi = computePI(seq, tree)
      #questo controllo mi permette di evitare sequenze non più presenti
      if pi is None:
         continue
      if pi >= teta:
         #se ho ancora spazio nel top
         if len(top) < num-1:
            top.append([seq, pi])
            ret.append(seq)
         #se sono al limite del top
         elif len(top) == num-1:
            top.append([seq, pi])
            ret.append(seq)
            teta = seqPIMin(top, num)
            print("new teta (==): " + str(teta))
         else:
            #se ho riempito tutto il top
            top.append([seq, pi])
            ret.append(seq)
            if pi > teta:
               teta = seqPIMin(top, num)
               print("new teta (>): " + str(teta))
               #cancello tutti i top con pi < teta
               for el in top:
                  if el[1] < teta:
                     #elimino il relativo sotto-albero alle sequenze eliminate
                     tree.deleteNode(el[0])
                     print("pi: " + str(el[1]))
                     top.remove(el)
               #end for
               #cancello tutti le seq con pi(seq) < teta dei candidates
               for elem in ret:
                  piRet = computePI(elem, tree)
                  if piRet is None:
                     continue
                  
                  if piRet < teta:
                     #elimino il relativo sotto-albero
                     tree.deleteNode(elem)
                     print("pi: " + str(piRet))
                     ret.remove(elem)
               #end for
            #end if
      else:
         #se il pi ha un teta mirore rispetto al limite
         #taglio l'albero relativo a questa computazione
         tree.deleteNode(seq)
         print("pi: " + str(pi))
   
   #return coppia di [lista dei canidati di lunghezza lun, [lista dei top, pi del relaivo]]
   return [ret, top]
#end verifyCandidates
   
################ stbfMiner Top ####################
#algroritmo STBF con il top e l'update della teta
def stbfMinerTop():
   #teta valore di threshold rispetto al pi
   #top è l'array in cui salvo i migliori risultati
   #num è il numero di risultati desiderati
   t_start = time.time()
   elapsed_t = t_start
   
   teta = 0.25 
   top = []
   num = 50
   #creo l'albero delle sequenze   
   tree = SPTree()   
   #prendo ciascun tipo di evento
   sql = "SELECT DISTINCT offence_code_group FROM " + table
   mycursor.execute(sql)
   
   types = []
   setTypes = []
   #inizializzo i tipi di eventi e i setD a loro legati
   #inserendo il primo layer di albero
   for tipo in mycursor:
      types.append(tipo[0])
   
   for el in types:
      s = setD(el)
      setTypes.append(s)

   i = 0
   for el in types:
      tree.insertNode(el, setTypes[i])
      i += 1
   #genero i pattern di lunghezza 2
   #per ora sono handmade (19 sequenze)
   seq2 = [["Aggravated Assault", "Auto Theft"], ["Commercial Burglary", "Homicide"], 
           ["Other Burglary", "Robbery"], ["Homicide", "Auto Theft"], 
           ["Larceny", "Residential Burglary"], ["Aggravated Assault", "Robbery"],
           ["Larceny From Motor Vehicle", "Homicide"],["Commercial Burglary", "Auto Theft"],
           ["Robbery", "Larceny"], ["Larceny From Motor Vehicle", "Commercial Burglary"],
           ["Auto Theft", "Residential Burglary"], ["Auto Theft", "Aggravated Assault"],
           ["Larceny", "Aggravated Assault"], ["Commercial Burglary", "Other Burglary"],
           ["Residential Burglary", "Auto Theft"],["Homicide", "Other Burglary"],
           ["Other Burglary", "Larceny"],["Larceny From Motor Vehicle", "Aggravated Assault"],
           ["Larceny", "Auto Theft"]]
   
      
   print("Livello 1:")
   for t in tree.root.children:
      print(str(t.value) + " - " + str(len(t.set)))
   
   
   
   print("... generating candidates(2)")
   c2 = candidateGen(seq2, tree)
   #faccio la verifyCandidates(2)
   #print(tree)
   print("\n... verifying candidates(2)")
   [l2, top] = verifyTopCandidates(c2, teta, top, num, tree)
   
   print("\nL2:")
   i = 0
   for el in l2:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
    
   print("\nTop(2):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
   
   print("\n" + str(tree))
   
   
   elapsed_t = round(time.time() - t_start)
   elapsed_min = round(elapsed_t/60, 3)
   print(time.ctime() + " : " + str(elapsed_t) + " sec - " + str(elapsed_min) + " min")
   
   print("\n... generating candidates(3)")
   c3 = candidateGenTree(l2, tree)
   print("\n... verifying candidates(3)")
   [l3, top] = verifyTopCandidates(c3, teta, top, num, tree)
   
   print("\nL3:")
   i = 0
   for el in l3:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
      
   print("\nTop(3):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
   
   print("\n" + str(tree))
   
   elapsed_t = time.time() - t_start
   elapsed_new_min = round(elapsed_t/60, 3)
   elapsed_lv = elapsed_new_min - elapsed_min
   elapsed_min = elapsed_new_min
   print("-- timer: " + str(elapsed_min) + " min, level: " + str(elapsed_lv) + " min --")
   
   print("\n... generating candidates(4)")
   c4 = candidateGenTree(l3, tree)
   print("\n... verifying candidates(4)")
   [l4, top] = verifyTopCandidates(c4, teta, top, num, tree)
   
    
   print("\nL4:")
   i = 0
   for el in l4:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
      
   print("\nTop(4):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
  
   elapsed_t = time.time() - t_start
   elapsed_new_min = round(elapsed_t/60, 3)
   elapsed_lv = elapsed_new_min - elapsed_min
   elapsed_min = elapsed_new_min
   print("-- timer: " + str(elapsed_min) + " min, level: " + str(elapsed_lv) + " min --")
   
   print("\n... generating candidates(5)")
   c5 = candidateGenTree(l4, tree)
   print("\n... verifying candidates(5)")
   [l5, top] = verifyTopCandidates(c5, teta, top, num, tree)
   
   print("\nL5:")
   i = 0
   for el in l5:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
      
   print("\nTop(5):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
   
   elapsed_t = time.time() - t_start
   elapsed_new_min = round(elapsed_t/60, 3)
   elapsed_lv = elapsed_new_min - elapsed_min
   elapsed_min = elapsed_new_min
   print("-- timer: " + str(elapsed_min) + " min, level: " + str(elapsed_lv) + " min --")
   
   print("\n... generating candidates(6)")
   c6 = candidateGenTree(l5, tree)
   print("\n... verifying candidates(6)")
   [l6, top] = verifyTopCandidates(c6, teta, top, num, tree)
    
   print("\nL6:")
   i = 0
   for el in l6:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
      
   print("\nTop(6):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
   
   elapsed_t = time.time() - t_start
   elapsed_new_min = round(elapsed_t/60, 3)
   elapsed_lv = elapsed_new_min - elapsed_min
   elapsed_min = elapsed_new_min
   print("-- timer: " + str(elapsed_min) + " min, level: " + str(elapsed_lv) + " min --")
  
   print("\n... generating candidates(7)")
   c7 = candidateGenTree(l6, tree)
   print("\n... verifying candidates(7)")
   [l7, top] = verifyTopCandidates(c7, teta, top, num, tree)
   
   print("\nL7:")
   i = 0
   for el in l7:
      i += 1
      print(str(i) + ". " + str(el) + " - " + str(computePI(el, tree)))
      
   print("\nTop(7):")
   i = 0
   for el in top:
      i += 1
      print(str(i) + ". " + str(el[0]) + " - " + str(el[1]))
  
   print("\n" + str(tree))
   
   elapsed_t = time.time() - t_start
   elapsed_new_min = round(elapsed_t/60, 3)
   elapsed_lv = elapsed_new_min - elapsed_min
   elapsed_min = elapsed_new_min
   print("-- timer: " + str(elapsed_min) + " min, level: " + str(elapsed_lv) + " min --")
   
##############################################################
   #TEST
      
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
      
def testPI() :
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
   i = 0
   for el in types:
      tree.insertNode(el, setTypes[i])
      i += 1
   
   candidateGen(seq2, tree) #inserisco sequenze di 2 elementi
   candidateGen(seq3, tree)
   i=1
   for seq in seq2:
      pi = computePI(seq, tree)
      print(str(i) + ". " + str(seq) + " - pi: " + str(pi))
      i += 1
   for seq in seq3:
      pi = computePI(seq, tree)
      print(str(i) + ". " + str(seq) + " - pi: " + str(pi))
      i += 1
#end  testPI
#############################
   #MAIN
if __name__ == "__main__":
   mydb = mysql.connector.connect(
         host = "localhost",
         user = "mysql.user",
         passwd = "aaaa",
         database = "bostoncrime"
         )
   table = "crimedata2018small"
   mycursor = mydb.cursor()

#   print("Testing testPR :")
#   testPR()
   
#   print("Testing testPI :")
#   testPI()

   print("Testing STBF Miner Top")
   stbfMinerTop()
   
   
   mycursor.close()