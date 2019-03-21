# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:34:17 2019

@author: fede9
"""

import datetime

today = datetime.date.today()
#print(today)
#d = today.day

d2 = datetime.date(2017, 6, 21)
d3 = datetime.date(2016, 2, 29)
diff = d2 - d3

giorni = diff.days

print(giorni)
