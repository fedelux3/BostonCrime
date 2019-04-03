# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:28:40 2019

@author: fede9
"""

import partRatioSQL as pr
import mysql.connector
   
def test_setInstancesSQL():
   seq = ["Homicide", "Residential Burglary"]
   ins = pr.setInstances(seq)
   print(ins)
   for i in ins:
      sql = "SELECT * FROM crimedata2018 WHERE incident_num = \"" + i + "\""
      mycursor.execute(sql)
      row = mycursor.fetchone()
   print(row)

#
mydb = mysql.connector.connect(
   host = "localhost",
   user = "root",
   passwd = "fedeServer33",
   database = "bostoncrime"
   )

mycursor = mydb.cursor()

test_setInstancesSQL()
