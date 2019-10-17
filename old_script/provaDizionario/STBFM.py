# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:55:14 2019

@author: fede9
"""

import time
import datetime
import math
import csv
from SPTreeD import SPTree

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
   
#input event (tupla dell'evento), type event
#output neigborhood event
def neighborhood(event, typeF) :
   #raggio spaziale della location (km)
   r = 0.2
   #raggio temporale
   t = 1
   #neighbothood with respect to event type
   nfe = dict()
   
   #cerco il dizionario che rispetta il typeF
   nType = tree.searchNode([typeF])
   if nType is None:
      print("ERRORE nType:" + str(typeF))
   dataType = nType.set
   valEv = event[1]
   for rec in dataType.items():
      val = rec[1]
      
      [late, longe] = parserLocation(valEv[2], valEv[3])
      [latp, longp] = parserLocation(val[2], val[3])
      #se è entro il raggio spaziale
      if distanceLocation(late, longe, latp, longp) <= r:
         timee = valEv[1]
         timep = val[1]
         diffDays = distanceTime(timee, timep)
         #se è entro il raggio temporale
         #escludo se stesso
         if diffDays <= t and event[0] != rec[0]:
            nfe[rec[0]] = rec[1]
   #end for
   return nfe
#end neighborhood
   
#input tipo di evento
#output insieme ti tutti gli eventi di quel tipo
def setD(typeD) :
   setReturn = dict()
   #print(typeD)
   for r in data.items():
      val = r[1]
      if val[0] == typeD:
         setReturn[r[0]] = val
   return setReturn
#end setD

#input insiemeSet precedente e tipo corrente
#output insieme di istanze associate
def setInstances(prevSet, currentType):
   set_return = dict()

   for event in prevSet.items():
      #la tupla che mi interessa
      #print(event)
      neig = neighborhood(event, currentType)
      #print(neig)
      set_return = unionDiz(set_return, neig)
   return set_return
#end setInstance

#funziona assumendo che la coppia chiave:valore sia uguale in tutti i dizionari
#input 2 dizionari
#output dizionario dato dall'unione dei 2 in input
def unionDiz(d1, d2):
   d3 = dict()
   d3.update(d1)
   d3.update(d2)
   return d3
#end unionDiz
   
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
   # print(ins)
   # print(d_set)
   pr = ins / d_set
   # print(pr)
   return pr
#end computePR
   
def computePI(seq, tree):
   length = len(seq)
   n = tree.searchNode(seq)
   #se il nodo non esiste allora lo segnalo in output
   if n is None:
      print("ERROR PI NODE NOT FOUND")
      return None
   if length <= 2: #caso base
      pr = computePR(n, tree)
      return pr
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
      # print(pi)
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
   num = 20
   
   #lista per scrivere i tempi nel csv
   ts = []
   #inizializzo i tipi di eventi
   types = ["Aggravated Assault", "Auto Theft", "Commercial Burglary", "Homicide",
            "Other Burglary", "Robbery", "Larceny", "Residential Burglary", 
            "Larceny From Motor Vehicle"]

#inserisco il primo livello   
   for el in types:
      s = setD(el) 
      tree.insertNode(el, s)
   # print(tree.root.children[1].value)
   # print(tree.root.children[1].set)
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
   
   #sono 26 sequenze
   # seq2 = [["Aggravated Assault", "Auto Theft"], ["Commercial Burglary", "Homicide"], 
   #         ["Other Burglary", "Robbery"], ["Homicide", "Auto Theft"], 
   #         ["Larceny", "Residential Burglary"], ["Aggravated Assault", "Robbery"],
   #         ["Larceny From Motor Vehicle", "Homicide"],["Commercial Burglary", "Auto Theft"],
   #         ["Robbery", "Larceny"], ["Larceny From Motor Vehicle", "Commercial Burglary"],
   #         ["Auto Theft", "Residential Burglary"], ["Auto Theft", "Aggravated Assault"],
   #         ["Larceny", "Aggravated Assault"], ["Commercial Burglary", "Other Burglary"],
   #         ["Residential Burglary", "Auto Theft"],["Homicide", "Other Burglary"],
   #         ["Other Burglary", "Larceny"],["Larceny From Motor Vehicle", "Aggravated Assault"],
   #         ["Larceny", "Auto Theft"], ["Aggravated Assault", "Larceny"], 
   #         ["Robbery", "Larceny From Motor Vehicle"], ["Robbery", "Homicide"], 
   #         ["Auto Theft", "Commercial Burglary"], ["Aggravated Assault", "Homicide"],
   #         ["Other Burglary", "Residential Burglary"], ["Residential Burglary", "Commercial Burglary"]]
   
   print("Livello 1:")
   for t in tree.root.children:
      print(str(t.value) + " - " + str(len(t.set)))
   
   print("... generating candidates(2)")
   c2 = candidateGen(seq2, tree)
   print(tree)
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
   
   
   elapsed_t = round(time.time() - t_start,0)
   elapsed_sec = elapsed_t
   elapsed_min = round(elapsed_t/60, 3)
   print(time.ctime() + " : " + str(elapsed_t) + " sec - " + str(elapsed_min) + " min")
   ts.append(elapsed_t)

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
   
   elapsed_t = round(time.time() - t_start,0)
   elapsed_lv = elapsed_t - elapsed_sec
   elapsed_sec = elapsed_t
   print("\n-- timer: " + str(elapsed_t) + " sec, level: " + str(elapsed_lv) + " sec --")
   ts.append(elapsed_lv)

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
  
   elapsed_t = round(time.time() - t_start,0)
   elapsed_lv = elapsed_t - elapsed_sec
   elapsed_sec = elapsed_t
   print("\n-- timer: " + str(elapsed_t) + " sec, level: " + str(elapsed_lv) + " sec --")
   ts.append(elapsed_lv)

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
   
   elapsed_t = round(time.time() - t_start,0)
   elapsed_lv = elapsed_t - elapsed_sec
   elapsed_sec = elapsed_t
   print("\n-- timer: " + str(elapsed_t) + " sec, level: " + str(elapsed_lv) + " sec --")
   ts.append(elapsed_lv)

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
   
   elapsed_t = round(time.time() - t_start,0)
   elapsed_lv = elapsed_t - elapsed_sec
   elapsed_sec = elapsed_t
   print("\n-- timer: " + str(elapsed_t) + " sec, level: " + str(elapsed_lv) + " sec --")
   ts.append(elapsed_lv)

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
   
   elapsed_t = round(time.time() - t_start,0)
   elapsed_lv = elapsed_t - elapsed_sec
   elapsed_sec = elapsed_t
   print("\n-- timer: " + str(elapsed_t) + " sec, level: " + str(elapsed_lv) + " sec --")
   ts.append(elapsed_lv)

   writer.writerow((file, 200, 1, num, teta, ts[0], ts[1], ts[2], ts[3], ts[4], ts[5], elapsed_t))
#############################
   #MAIN
if __name__ == "__main__":

   filesName = ["dataset2018_2_One.csv"]
   # , "dataset2018_One_4000.csv", "dataset2018_One_full.csv"]
   
   wr = open("results.csv", "a")
   writer = csv.writer(wr, dialect = 'excel', quoting= csv.QUOTE_MINIMAL)
   
   for file in filesName :
      data = {}
      with open(file) as filecsv:
         
         readData = csv.reader(filecsv, dialect = 'excel', delimiter = ";")
         
         recordData = [(col[0], col[1], col[2], col[4], col[5]) for col in readData]
         
         for record in recordData[1:]:
            data[record[0]] = [record[1], record[2], record[3], record[4]]
            
      #print(data)
      #inizializzo l'albero
      tree = SPTree()
      
      print("Testing STBF Miner Top")
      stbfMinerTop()
   
   wr.close()
