# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:20:44 2019

@author: fede9
"""

import csv

wr = open("test2.csv", "wt", newline="")

with open("./crime.csv", newline="", encoding="ISO-8859-1") as filecsv:
   
   try:
      lettore = csv.reader(filecsv, dialect = 'excel', delimiter= ";")
      writer = csv.writer(wr, dialect = 'excel', quoting= csv.QUOTE_MINIMAL)
      #header = next(lettore)
      #writer.writerow(header)
      #print(header)
      
      record = [(colon[0], colon[2], colon[3], colon[7], colon[12], colon[14], 
                 colon[15], colon[16]) for colon in lettore]
   
      for crime in record:
         #if crime[5] != "-100.000.000" and crime[5] != ""
         if crime[0] == "I182078936" or crime[0] == "I172003578":
            #print(crime[5])
            writer.writerow((crime[0], crime[1], crime[2], crime[3], crime[4], crime[5], crime[6], crime[7]))
         
   finally:
      wr.close()