# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:06:10 2019

@author: fede9
"""

import time

print("L'ora è : " + time.ctime())
t1 = time.process_time()


print("differenza: " + str(t1))
print("L'ora è : " + time.ctime())