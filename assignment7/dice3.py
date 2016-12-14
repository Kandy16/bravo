# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 15:22:46 2016

@author: Daniel
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from pylab import xticks
import sys

def Roll(x) :
    
    min=1
    
    max=6
    
    roll = 0
    
    die1=list()
    die2=list()
    
    while (roll<x):
    
        die1.append(random.randint(min,max))
    
        die2.append(random.randint(min,max))
    
        roll += 1
        
    global Sum
        
    Sum = [x+y for x,y in zip(die1,die2)]

    return Sum
   
def Histogram(x):
   
    plt.figure(figsize=(8, 6), dpi=80)
    plt.hist(x, 60, alpha=0.85)
    plt.title('Histogram')
    plt.xlim(0,14)
    median =np.median(x)
    plt.axvline(median, color='r', linestyle='dashed', linewidth=3)
    xticks(range(2, 13))
    plt.grid(True)
    plt.show()
    
    
    
def Cumulative (x):
    
    sort = np.sort(x)
    
    global cdf
    
    cdf = np.cumsum(sort)
   # ncdf = 1.0/cdf[-1] * cdf

    median =np.median(x)
    #print(median)
    #print(x)
    plt.figure(figsize=(8, 6), dpi=80)
    #plt.plot(ncdf,c='b')

    num_bins = 10
    counts, bin_edges = np.histogram(x, bins=num_bins, normed=True)
    cdf = np.cumsum(counts)
    plt.plot(bin_edges[1:], cdf)
    
    #plt.plot(base[:1], x, c='blue')
    plt.ylabel('CDF')
    #plt.hist(x, 60, alpha=0.85)
    #xticks(range(2, 13))
    plt.grid(True)
    plt.axvline(median, color='r', linestyle='dashed', linewidth=3)
    plt.axvline(9, color='g', linewidth=3)
    #plt.xlim(0,1)
    plt.legend()
    plt.show()
    
    
        
#dist = np.linalg.norm(a-b)

Roll(1000)

Histogram(Sum)

Cumulative(Sum)

f=cdf

print('Probability of dice sum to be equal or less than 9 : ' ,cdf[6])

Roll(1000)

Histogram(Sum)

Cumulative(Sum)

g=cdf

#diff=list()
diff=abs(f-g)
print(diff)





