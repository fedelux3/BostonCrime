# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 16:23:50 2019

@author: fede9
"""

import random


def checkDouble(listE, el):
   
   listB = listE[:]
   listB.append(el)
   s = set(listB)
   l = len(listB)
   ls = len(s)
   if (l == ls):
      return True
   else:
      return False
   
list = [111,222,333,444,555]


l = []
while (len(l) < 2) :
   n = random.choice(list)
   if (checkDouble(l, n)):
      l.append(n)
      print(l)
   else:
      print("doppio: : " + str(n))
   
print(l)
