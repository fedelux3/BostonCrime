# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:31:55 2019

@author: fede9
"""

import csv
import sys

f = open("prova.csv", 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ['Title 1', 'Title 2', 'Title 3'] )
    for i in range(10):
        writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
finally:
    f.close()

#print open("prova.txt", 'rt').read()