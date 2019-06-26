# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:12:58 2019

@author: fede9
"""

def elSort(val):
   return val[1]

if __name__ == "__main__":
   l = [['a', 0.5], ['b', 0.3], ['e', 0.68], ['d', 0.68], ['c', 0.4]]
   l2 = [1, 3, 2, 5, 3]
   
   print(l)
   l.sort(key = elSort, reverse = True)
   print(l)   
   
