# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:20:44 2019

@author: fede9
"""

import csv

wr = open("dataset2018_One_4000.csv", "a", newline="")

with open("test2018.csv", newline="", encoding="ISO-8859-1") as filecsv:
   
   try:
      lettore = csv.reader(filecsv, dialect = 'excel', delimiter= ";")
      writer = csv.writer(wr, dialect = 'excel', quoting= csv.QUOTE_MINIMAL)
      #header = next(lettore)
      #writer.writerow(header)
      #print(header)
      
      record = [(colon[0], colon[1], colon[2], colon[3], colon[4], colon[5]) for colon in lettore]
      i = 0
      for crime in record:
         i += 1
         if i % 3 == 0:
            
            writer.writerow((crime[0], crime[1], crime[2], crime[3], crime[4], crime[5]))
         
   finally:
      wr.close()