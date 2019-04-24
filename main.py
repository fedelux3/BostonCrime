# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:28:40 2019

@author: fede9
"""


import mysql.connector
from SPTree import SPTree 

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
if __name__ == "__main__":
   mydb = mysql.connector.connect(
      host = "localhost",
      user = "root",
      passwd = "fedeServer33",
      database = "bostoncrime"
      )
   
   mycursor = mydb.cursor()
   mycursor.close()
   #test_setInstancesSQL()
   
   t = SPTree(["ciao"])
   print(t)