# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:20:44 2019

@author: fede9
"""

import csv

wr = open("test2018.csv", "a", newline="")

with open("dataset2018.csv", newline="", encoding="ISO-8859-1") as filecsv:
   
   try:
      lettore = csv.reader(filecsv, dialect = 'excel', delimiter= ";")
      writer = csv.writer(wr, dialect = 'excel', quoting= csv.QUOTE_MINIMAL)
      #header = next(lettore)
      #writer.writerow(header)
      #print(header)
      
      record = [(colon[0], colon[1], colon[2], colon[3], colon[4], colon[5]) for colon in lettore]
   
      for crime in record:
         #if crime[4] != "-100.000.000" and crime[4] != "" and crime[6] == "2018":
         if crime[3] == "Part One":
            #print(crime[5])
            writer.writerow((crime[0], crime[1], crime[2], crime[3], crime[4], crime[5]))
         
   finally:
      wr.close()