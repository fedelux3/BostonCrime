# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:10:50 2019

@author: fede9
"""

from SPTree import SPTree
import mysql.connector
import computePI as compute

#input un insieme di sequenze significative
#assumo che l'input sia di una lista di sequenze (che a loro volta sono liste)
#output albero con set di candidati 

def candidateGen(setSeq, tree) :
   
   for seq in setSeq :
      tree.insertNode(seq)
   #print(tree)
#end caditateGen
   
def testPaper() :
   types = ["A", "B", "C", "D", "E", "F"]
   seq2 = [["A", "B"], ["B", "C"], ["B", "D"], ["C", "E"], ["C", "F"]]
   seq3 = [["A", "B", "C"], ["A", "B", "D"], ["B", "C", "E"], ["B", "C", "F"]]
   seq4 = [["A", "B", "C", "E"], ["A", "B", "C", "F"]]
   tree = SPTree(types)
   candidateGen(seq2, tree)
   candidateGen(seq3, tree)
   candidateGen(seq4, tree)
#end testPaper

def testDataset():
   types = []
   seq2 = [["Aggravated Assault", "Auto Theft"], ["Commercial Burglary", "Homicide"], 
           ["Other Burglary", "Robbery"], ["Homicide", "Auto Theft"], 
           ["Larceny", "Residential Burglary"], ["Aggravated Assault", "Robbery"],
           ["Larceny From Motor Vehicle", "Homicide"],["Commercial Burglary", "Auto Theft"]]
   
   sql = "SELECT DISTINCT offence_code_group FROM crimedata2018small"
   mycursor.execute(sql)
   
   for tipo in mycursor:
      types.append(tipo[0])

   tree = SPTree(types)
   candidateGen(seq2, tree)
   print(tree)
   
   ins = tree.candidates
   i = 0

   for seq in ins:
      i += 1
      pi = compute.computePI(seq)
      print(str(i) + ". " + str(seq) + ": " + str(pi))
   mycursor.close()
#end testDataset
   
if __name__ == "__main__" :
   mydb = mysql.connector.connect(
      host = "localhost",
      user = "root",
      passwd = "fedeServer33",
      database = "bostoncrime"
      )
   
   mycursor = mydb.cursor()

   testDataset()
   
   mycursor.close()